import pygame

COLOR_BG = (10, 14, 23)
COLOR_GRID = (18, 24, 38)
COLOR_WALL = (25, 35, 58)
COLOR_WALL_OUTLINE = (0, 229, 255)
COLOR_TERMINAL = (255, 215, 0)
COLOR_TEXT = (180, 210, 245)
COLOR_ALERT = (255, 60, 80)
COLOR_SUCCESS = (0, 255, 170)

class Renderer:
    def __init__(self, surface: pygame.Surface, width: int, height: int, tile_size: int = 40):
        self.surface = surface
        self.w = width
        self.h = height
        self.tile_size = tile_size
        self.font_hud = pygame.font.SysFont("Consolas", 16, bold=True)
        self.font_title = pygame.font.SysFont("Consolas", 32, bold=True)

    def draw_world(self, walls: list[pygame.Rect], target: pygame.Rect):
        self.surface.fill(COLOR_BG)

        for x in range(0, self.w, self.tile_size):
            pygame.draw.line(self.surface, COLOR_GRID, (x, 0), (x, self.h))
        for y in range(0, self.h, self.tile_size):
            pygame.draw.line(self.surface, COLOR_GRID, (0, y), (self.w, y))

        for w in walls:
            pygame.draw.rect(self.surface, COLOR_WALL, w)
            pygame.draw.rect(self.surface, COLOR_WALL_OUTLINE, w, 1)

        t_glow = pygame.Surface((52, 52), pygame.SRCALPHA)
        pygame.draw.rect(t_glow, (255, 215, 0, 75), t_glow.get_rect(), border_radius=8)
        self.surface.blit(t_glow, (target.x - 8, target.y - 8))
        pygame.draw.rect(self.surface, COLOR_TERMINAL, target, border_radius=6)

    def draw_hud(self, level: int, max_level: int, guards_count: int):
        hud_bg = pygame.Surface((self.w, 36), pygame.SRCALPHA)
        hud_bg.fill((10, 14, 23, 210))
        self.surface.blit(hud_bg, (0, 0))
        info = f"SECTOR: {level:03d} / {max_level:03d}  |  ACTIVE GUARDS: {guards_count}  |  STATUS: NORMAL"
        self.surface.blit(self.font_hud.render(info, True, COLOR_TEXT), (20, 10))

    def draw_overlay(self, state: str, level: int, max_level: int):
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        if state == "BUSTED":
            overlay.fill((25, 0, 10, 185))
            self.surface.blit(overlay, (0, 0))
            t1 = self.font_title.render("INTRUSION DETECTED // SECTOR LOCKED", True, COLOR_ALERT)
            t2 = self.font_hud.render("Press [R] to Retry Sector", True, (255, 255, 255))
        elif state == "CLEARED":
            overlay.fill((0, 25, 15, 185))
            self.surface.blit(overlay, (0, 0))
            title = "SYSTEM OVERRIDDEN // EXTRACTION SUCCESS" if level < max_level else "ALL PROTOCOLS COMPLETED // MASTER AGENT"
            sub = "Press [SPACE] to Access Next Sector" if level < max_level else "You beat all 100 levels!"
            t1 = self.font_title.render(title, True, COLOR_SUCCESS)
            t2 = self.font_hud.render(sub, True, (255, 255, 255))

        self.surface.blit(t1, t1.get_rect(center=(self.w // 2, self.h // 2 - 15)))
        self.surface.blit(t2, t2.get_rect(center=(self.w // 2, self.h // 2 + 30)))