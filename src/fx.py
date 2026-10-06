import random
import pygame

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x: float, y: float, color: tuple, count: int = 6, speed_range=(1.0, 3.5), life_range=(0.2, 0.6)):
        for _ in range(count):
            ang = random.uniform(0, 6.28)
            spd = random.uniform(*speed_range)
            vx = spd * 1.5 * (1 if random.random() > 0.5 else -1)
            vy = spd * 1.5 * (1 if random.random() > 0.5 else -1)
            life = random.uniform(*life_range)
            size = random.uniform(2.0, 4.5)
            self.particles.append({"x": x, "y": y, "vx": vx, "vy": vy, "life": life, "max_life": life, "color": color, "size": size})

    def update(self, dt: float):
        for p in self.particles[:]:
            p["life"] -= dt
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["size"] = max(0.5, p["size"] - (dt * 3))
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        ox, oy = offset
        for p in self.particles:
            alpha = int(255 * (p["life"] / p["max_life"]))
            p_surf = pygame.Surface((int(p["size"] * 2), int(p["size"] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*p["color"][:3], alpha), (int(p["size"]), int(p["size"])), int(p["size"]))
            surface.blit(p_surf, (p["x"] - p["size"] + ox, p["y"] - p["size"] + oy))


class ScreenShake:
    def __init__(self):
        self.trauma = 0.0

    def add_trauma(self, amount: float):
        self.trauma = min(1.0, self.trauma + amount)

    def update(self, dt: float):
        if self.trauma > 0:
            self.trauma = max(0.0, self.trauma - dt * 1.8)

    def get_offset(self) -> tuple[int, int]:
        if self.trauma <= 0:
            return 0, 0
        shake_mag = (self.trauma ** 2) * 14
        ox = int(random.uniform(-shake_mag, shake_mag))
        oy = int(random.uniform(-shake_mag, shake_mag))
        return ox, oy