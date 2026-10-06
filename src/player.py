import pygame

CHARACTERS = {
    "Specter": {
        "color": (0, 255, 170),
        "speed": 3.6,
        "size": 18,
        "cost": 0,
        "ability": "None",
        "desc": "Balanced Infiltrator (Default)",
    },
    "Phantom": {
        "color": (170, 70, 255),
        "speed": 4.6,
        "size": 14,
        "cost": 15,
        "ability": "Agile",
        "desc": "High Speed & Micro Hitbox",
    },
    "Juggernaut": {
        "color": (255, 145, 0),
        "speed": 3.0,
        "size": 22,
        "cost": 30,
        "ability": "Energy Shield",
        "desc": "Absorbs 1 detection per sector",
    },
    "Glitch": {
        "color": (0, 229, 255),
        "speed": 3.4,
        "size": 18,
        "cost": 45,
        "ability": "EMP Jammer [SPACE]",
        "desc": "Stuns all guards for 3.5s (8s CD)",
    },
    "Blink": {
        "color": (255, 0, 128),
        "speed": 3.5,
        "size": 16,
        "cost": 60,
        "ability": "Phase Dash [SPACE]",
        "desc": "Instant directional teleport (4s CD)",
    },
}


class Coin:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x - 6, y - 6, 12, 12)
        self.color = (255, 230, 0)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.rect.center, 6)
        glow = pygame.Surface((18, 18), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 230, 0, 75), (9, 9), 9)
        surface.blit(glow, (self.rect.centerx - 9, self.rect.centery - 9))


class Player:
    def __init__(self, x: int, y: int, char_name: str = "Specter"):
        self.char_name = char_name
        data = CHARACTERS[char_name]
        self.speed = data["speed"]
        self.color = data["color"]
        self.size = data["size"]
        self.ability = data["ability"]
        self.rect = pygame.Rect(x, y, self.size, self.size)

        # Karakteristik Spesial
        self.shield_available = char_name == "Juggernaut"
        self.ability_cooldown = 0.0
        self.last_move_dir = (1, 0)

    def move(self, dx: float, dy: float, walls: list[pygame.Rect]):
        if dx != 0 or dy != 0:
            self.last_move_dir = (dx, dy)
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071

        self.rect.x += int(dx * self.speed)
        for w in walls:
            if self.rect.colliderect(w):
                if dx > 0: self.rect.right = w.left
                if dx < 0: self.rect.left = w.right

        self.rect.y += int(dy * self.speed)
        for w in walls:
            if self.rect.colliderect(w):
                if dy > 0: self.rect.bottom = w.top
                if dy < 0: self.rect.top = w.bottom

    def update_cooldown(self, dt: float):
        if self.ability_cooldown > 0:
            self.ability_cooldown = max(0.0, self.ability_cooldown - dt)

    def trigger_ability(self, guards: list, walls: list[pygame.Rect]) -> bool:
        if self.ability_cooldown > 0:
            return False

        if self.char_name == "Glitch":
            self.ability_cooldown = 8.0
            for g in guards:
                g.apply_emp(3.5)
            return True

        elif self.char_name == "Blink":
            self.ability_cooldown = 4.0
            step = 85
            mx, my = self.last_move_dir
            new_x = self.rect.x + int(mx * step)
            new_y = self.rect.y + int(my * step)
            test_rect = pygame.Rect(new_x, new_y, self.size, self.size)
            if not any(test_rect.colliderect(w) for w in walls):
                self.rect.topleft = (new_x, new_y)
            return True

        return False

    def draw(self, surface: pygame.Surface):
        glow_size = self.size + 14
        glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*self.color, 60), glow.get_rect(), border_radius=6)
        surface.blit(glow, (self.rect.x - 7, self.rect.y - 7))
        pygame.draw.rect(surface, self.color, self.rect, border_radius=4)

        if self.char_name == "Juggernaut" and self.shield_available:
            pygame.draw.rect(surface, (0, 229, 255), self.rect.inflate(8, 8), 2, border_radius=6)