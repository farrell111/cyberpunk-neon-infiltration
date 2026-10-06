import math
import random
import pygame
from src.player import Player, Coin
from src.enemy import Guard
from src.interactive import LaserTripwire, HackTerminal

def generate_level(level_num: int, screen_w: int, screen_h: int, active_char: str = "Specter", tile_size: int = 40):
    rng = random.Random(level_num * 73939)
    cols = screen_w // tile_size
    rows = screen_h // tile_size

    guard_count = min(13, 2 + level_num // 7)
    guard_speed = min(3.5, 1.4 + (level_num * 0.022))
    view_dist = min(250, 140 + (level_num * 1.1))
    wall_density = min(0.24, 0.10 + (level_num * 0.0015))

    walls = [
        pygame.Rect(0, 0, screen_w, 12),
        pygame.Rect(0, screen_h - 12, screen_w, 12),
        pygame.Rect(0, 0, 12, screen_h),
        pygame.Rect(screen_w - 12, 0, 12, screen_h),
    ]

    for c in range(2, cols - 2, 2):
        for r in range(2, rows - 2, 2):
            if rng.random() < wall_density:
                w_len = rng.choice([2, 3])
                if rng.random() > 0.5:
                    walls.append(pygame.Rect(c * tile_size, r * tile_size, w_len * tile_size, 20))
                else:
                    walls.append(pygame.Rect(c * tile_size, r * tile_size, 20, w_len * tile_size))

    player = Player(40, 40, active_char)
    target = pygame.Rect(screen_w - 70, screen_h - 70, 36, 36)

    # Spawn Guards
    guards = []
    attempts = 0
    guard_types = ["PATROL", "TURRET", "STALKER"]
    while len(guards) < guard_count and attempts < 220:
        attempts += 1
        gx = rng.randint(4, cols - 4) * tile_size
        gy = rng.randint(4, rows - 4) * tile_size
        candidate = pygame.Rect(gx, gy, 20, 20)
        if any(candidate.colliderect(w) for w in walls) or math.hypot(gx - 40, gy - 40) < 180:
            continue
        g_type = rng.choices(guard_types, weights=[0.55, 0.25, 0.20])[0]
        offset = rng.randint(80, 190)
        p2 = (min(screen_w - 40, gx + offset), gy) if rng.random() > 0.5 else (gx, min(screen_h - 40, gy + offset))
        guards.append(Guard(g_type, [(gx, gy), p2], guard_speed, view_dist))

    # Spawn Koin
    coins = []
    coin_attempts = 0
    num_coins = rng.randint(3, 6)
    while len(coins) < num_coins and coin_attempts < 100:
        coin_attempts += 1
        cx = rng.randint(2, cols - 2) * tile_size + (tile_size // 2)
        cy = rng.randint(2, rows - 2) * tile_size + (tile_size // 2)
        c_rect = pygame.Rect(cx - 8, cy - 8, 16, 16)
        if not any(c_rect.colliderect(w) for w in walls):
            coins.append(Coin(cx, cy))

    # Spawn Laser Tripwires (muncul mulai level 2)
    lasers = []
    if level_num >= 2:
        num_lasers = min(4, 1 + level_num // 8)
        for _ in range(num_lasers):
            lx = rng.randint(5, cols - 5) * tile_size
            ly = rng.randint(3, rows - 3) * tile_size
            orientation = rng.choice(["H", "V"])
            span = rng.randint(2, 4) * tile_size
            if orientation == "H":
                lasers.append(LaserTripwire(lx, ly, min(screen_w - 40, lx + span), ly, rng.uniform(1.8, 3.2)))
            else:
                lasers.append(LaserTripwire(lx, ly, lx, min(screen_h - 40, ly + span), rng.uniform(1.8, 3.2)))

    # Spawn 1 Hackable Console per stage
    hx = rng.randint(5, cols - 5) * tile_size + 6
    hy = rng.randint(5, rows - 5) * tile_size + 6
    terminal = HackTerminal(hx, hy)

    return walls, player, target, guards, coins, lasers, terminal