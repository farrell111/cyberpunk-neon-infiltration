import sys
import pygame
from src.map import generate_level
from src.player import CHARACTERS, Player
from src.renderer import Renderer
from src.fx import ParticleSystem, ScreenShake
from src.storage import load_game_data, save_game_data

SCREEN_WIDTH, SCREEN_HEIGHT = 960, 640
FPS = 60
MAX_LEVEL = 100

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Neon Infiltration // Cyberpunk Stealth Core v2.0")
clock = pygame.time.Clock()
font_ui = pygame.font.SysFont("Consolas", 15, bold=True)
font_big = pygame.font.SysFont("Consolas", 26, bold=True)

renderer = Renderer(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
particles = ParticleSystem()
shaker = ScreenShake()

# Inisialisasi Save Data
save_data = load_game_data()
current_level = save_data.get("highest_level", 1)
total_credits = save_data.get("credits", 0)
unlocked_chars = save_data.get("unlocked_chars", ["Specter"])
active_char = save_data.get("active_char", "Specter")

walls, player, target, guards, coins, lasers, terminal = generate_level(
    current_level, SCREEN_WIDTH, SCREEN_HEIGHT, active_char
)
game_state = "PLAYING"

def sync_save():
    save_data["credits"] = total_credits
    save_data["highest_level"] = current_level
    save_data["unlocked_chars"] = unlocked_chars
    save_data["active_char"] = active_char
    save_game_data(save_data)

while True:
    dt = clock.tick(FPS) / 1000.0
    shaker.update(dt)
    particles.update(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sync_save()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_state == "PLAYING":
                if event.key == pygame.K_c:
                    game_state = "SHOP"
                elif event.key == pygame.K_SPACE:
                    if player.trigger_ability(guards, walls):
                        shaker.add_trauma(0.35)
                        particles.emit(player.rect.centerx, player.rect.centery, player.color, count=25, speed_range=(2, 6))

            elif game_state == "SHOP":
                if event.key in (pygame.K_c, pygame.K_ESCAPE):
                    game_state = "PLAYING"
                char_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]
                for idx, k in enumerate(char_keys):
                    if event.key == k and idx < len(CHARACTERS):
                        c_name = list(CHARACTERS.keys())[idx]
                        c_data = CHARACTERS[c_name]
                        if c_name in unlocked_chars:
                            active_char = c_name
                            player = Player(player.rect.x, player.rect.y, active_char)
                            sync_save()
                        elif total_credits >= c_data["cost"]:
                            total_credits -= c_data["cost"]
                            unlocked_chars.append(c_name)
                            active_char = c_name
                            player = Player(player.rect.x, player.rect.y, active_char)
                            sync_save()

            elif game_state == "BUSTED" and event.key == pygame.K_r:
                walls, player, target, guards, coins, lasers, terminal = generate_level(
                    current_level, SCREEN_WIDTH, SCREEN_HEIGHT, active_char
                )
                game_state = "PLAYING"

            elif game_state == "CLEARED" and event.key == pygame.K_SPACE:
                current_level = min(MAX_LEVEL, current_level + 1)
                sync_save()
                walls, player, target, guards, coins, lasers, terminal = generate_level(
                    current_level, SCREEN_WIDTH, SCREEN_HEIGHT, active_char
                )
                game_state = "PLAYING"

    if game_state == "PLAYING":
        player.update_cooldown(dt)
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        
        if dx != 0 or dy != 0:
            particles.emit(player.rect.centerx, player.rect.centery, player.color, count=1, speed_range=(0.2, 0.8), life_range=(0.15, 0.3))
        player.move(dx, dy, walls)

        # Update Lasers
        for laser in lasers:
            laser.update(dt)
            if laser.collides_with(player.rect):
                shaker.add_trauma(0.8)
                game_state = "BUSTED"

        # Update Hack Terminal
        if terminal.try_hack(player.rect, dt):
            shaker.add_trauma(0.4)
            particles.emit(terminal.rect.centerx, terminal.rect.centery, (0, 229, 255), count=30, speed_range=(3, 7))
            for g in guards:
                g.apply_emp(4.5)  # Peretasan melumpuhkan semua sensor musuh

        # Koleksi Koin
        for c in coins[:]:
            if player.rect.colliderect(c.rect):
                coins.remove(c)
                total_credits += 1
                particles.emit(c.rect.centerx, c.rect.centery, (255, 230, 0), count=12)
                sync_save()

        # Update Patrol Guard & Line of Sight
        for g in guards:
            g.update(dt, player.rect, walls)
            if g.can_see(player.rect, walls):
                if player.char_name == "Juggernaut" and player.shield_available:
                    player.shield_available = False
                    shaker.add_trauma(0.6)
                    particles.emit(player.rect.centerx, player.rect.centery, (0, 229, 255), count=25)
                    g.apply_emp(2.5)
                else:
                    shaker.add_trauma(0.9)
                    game_state = "BUSTED"

        if player.rect.colliderect(target):
            shaker.add_trauma(0.3)
            game_state = "CLEARED"

    # Render Pipeline dengan Screen Shake Offset
    offset = shaker.get_offset()
    render_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    renderer.draw_world(walls, target)
    terminal.draw(screen, offset)
    for laser in lasers:
        laser.draw(screen, offset)
    for c in coins:
        c.draw(screen)
    for g in guards:
        g.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    player.draw(screen)
    particles.draw(screen, offset)

    # HUD Elements
    renderer.draw_hud(current_level, MAX_LEVEL, len(guards))
    cd_status = f"{player.ability_cooldown:.1f}s" if player.ability_cooldown > 0 else "READY"
    status_bar = font_ui.render(f"CREDITS: {total_credits} | AGENT: {active_char.upper()} | ABILITY: {cd_status} | [C] ROSTER", True, (255, 230, 0))
    screen.blit(status_bar, (SCREEN_WIDTH - 580, 10))

    if game_state == "SHOP":
        menu_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        menu_surf.fill((10, 14, 23, 240))
        screen.blit(menu_surf, (0, 0))
        title = font_big.render("TACTICAL ROSTER // OPERATIVE DATABASE", True, (0, 229, 255))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 45)))

        for i, (name, data) in enumerate(CHARACTERS.items()):
            status_text = "EQUIPPED" if name == active_char else ("UNLOCKED" if name in unlocked_chars else f"LOCKED ({data['cost']} CR)")
            card_rect = pygame.Rect(140, 90 + (i * 95), 680, 80)
            pygame.draw.rect(screen, (18, 24, 40), card_rect, border_radius=6)
            pygame.draw.rect(screen, data["color"], card_rect, 2, border_radius=6)
            screen.blit(font_big.render(f"[{i+1}] {name}", True, data["color"]), (card_rect.x + 18, card_rect.y + 10))
            screen.blit(font_ui.render(f"Skill: {data['ability']} | {data['desc']}", True, (180, 210, 245)), (card_rect.x + 18, card_rect.y + 38))
            screen.blit(font_ui.render(f"Status: {status_text}", True, (255, 230, 0) if "LOCKED" in status_text else (0, 255, 170)), (card_rect.x + 18, card_rect.y + 58))

        close_tip = font_ui.render("Press [1-5] to Equip/Buy  |  Press [C] / [ESC] to Resume Mission", True, (160, 180, 200))
        screen.blit(close_tip, close_tip.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)))

    elif game_state in ("BUSTED", "CLEARED"):
        renderer.draw_overlay(game_state, current_level, MAX_LEVEL)

    pygame.display.flip()