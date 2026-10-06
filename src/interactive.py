import math
import pygame

COLOR_LASER = (255, 20, 70)
COLOR_HACK = (0, 229, 255)

class LaserTripwire:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, cycle_speed: float = 2.0):
        self.p1 = (x1, y1)
        self.p2 = (x2, y2)
        self.cycle_speed = cycle_speed
        self.timer = 0.0
        self.is_active = True

    def update(self, dt: float):
        self.timer += dt * self.cycle_speed
        # Berdenyut on/off secara berkala
        self.is_active = (math.sin(self.timer) > -0.3)

    def collides_with(self, rect: pygame.Rect) -> bool:
        if not self.is_active:
            return False
        return rect.clipline(self.p1, self.p2) != ()

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        if not self.is_active:
            return
        ox, oy = offset
        p1 = (self.p1[0] + ox, self.p1[1] + oy)
        p2 = (self.p2[0] + ox, self.p2[1] + oy)
        pygame.draw.line(surface, (255, 50, 100), p1, p2, 4)
        pygame.draw.line(surface, (255, 255, 255), p1, p2, 1)


class HackTerminal:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 26, 26)
        self.interact_zone = self.rect.inflate(30, 30)
        self.is_hacked = False
        self.hack_progress = 0.0
        self.hack_duration = 1.8

    def try_hack(self, player_rect: pygame.Rect, dt: float) -> bool:
        if self.is_hacked:
            return False
        if self.interact_zone.colliderect(player_rect):
            self.hack_progress += dt
            if self.hack_progress >= self.hack_duration:
                self.is_hacked = True
                return True
        else:
            self.hack_progress = max(0.0, self.hack_progress - dt * 2)
        return False

    def draw(self, surface: pygame.Surface, offset=(0, 0)):
        ox, oy = offset
        r = self.rect.move(ox, oy)
        color = (100, 100, 120) if self.is_hacked else COLOR_HACK
        pygame.draw.rect(surface, color, r, border_radius=4)

        if not self.is_hacked and self.hack_progress > 0:
            prog_w = int((self.hack_progress / self.hack_duration) * 26)
            pygame.draw.rect(surface, (0, 255, 170), (r.x, r.y - 8, prog_w, 4))