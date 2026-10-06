import math
import random
import pygame

COLOR_VISION_NORMAL = (255, 60, 80, 45)
COLOR_VISION_ALERT = (255, 170, 0, 60)
COLOR_VISION_STUN = (0, 229, 255, 30)


class Guard:
    def __init__(self, guard_type: str, waypoints: list[tuple[int, int]], speed: float, view_dist: float):
        self.type = guard_type  # 'PATROL', 'TURRET', 'STALKER'
        self.waypoints = waypoints
        self.current_wp = 0
        self.x, self.y = float(waypoints[0][0]), float(waypoints[0][1])
        self.rect = pygame.Rect(int(self.x) - 10, int(self.y) - 10, 20, 20)
        self.speed = speed
        self.view_distance = view_dist
        self.angle = random.uniform(0, 360)
        self.fov = 80 if self.type == "TURRET" else 60

        # State Machine AI
        self.state = "PATROL"  # PATROL, SUSPICIOUS, STUNNED
        self.investigate_target = None
        self.investigate_timer = 0.0
        self.stun_timer = 0.0

    def apply_emp(self, duration: float):
        self.state = "STUNNED"
        self.stun_timer = duration

    def update(self, dt: float, player_rect: pygame.Rect, walls: list[pygame.Rect]):
        if self.state == "STUNNED":
            self.stun_timer -= dt
            if self.stun_timer <= 0:
                self.state = "PATROL"
            return

        if self.type == "TURRET":
            # Berputar rotasi kontinu di tempat
            self.angle = (self.angle + 65 * dt) % 360
            return

        if self.state == "SUSPICIOUS":
            self.investigate_timer -= dt
            if self.investigate_timer <= 0:
                self.state = "PATROL"
            else:
                tx, ty = self.investigate_target
                dx, dy = tx - self.x, ty - self.y
                dist = math.hypot(dx, dy)
                if dist > 6.0:
                    self.angle = math.degrees(math.atan2(dy, dx))
                    self.x += (dx / dist) * (self.speed * 1.25)
                    self.y += (dy / dist) * (self.speed * 1.25)
                    self.rect.center = (int(self.x), int(self.y))
            return

        # Patrol Waypoint standar
        tx, ty = self.waypoints[self.current_wp]
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)

        if dist < 4.0:
            self.current_wp = (self.current_wp + 1) % len(self.waypoints)
        else:
            self.angle = math.degrees(math.atan2(dy, dx))
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
            self.rect.center = (int(self.x), int(self.y))

        # Stalker: cek area peripheral untuk trigger investigasi
        if self.type == "STALKER" and self.state == "PATROL":
            px, py = player_rect.center
            p_dist = math.hypot(px - self.x, py - self.y)
            if p_dist < self.view_distance * 1.3:
                self.state = "SUSPICIOUS"
                self.investigate_target = (px, py)
                self.investigate_timer = 2.5

    def can_see(self, player_rect: pygame.Rect, walls: list[pygame.Rect]) -> bool:
        if self.state == "STUNNED":
            return False

        px, py = player_rect.center
        gx, gy = self.rect.center
        dx, dy = px - gx, py - gy
        dist = math.hypot(dx, dy)

        if dist > self.view_distance:
            return False

        angle_to_target = math.degrees(math.atan2(dy, dx))
        diff = (angle_to_target - self.angle + 180) % 360 - 180
        if abs(diff) > (self.fov / 2):
            return False

        steps = int(dist / 8)
        for i in range(1, steps):
            cx = gx + (dx * i / steps)
            cy = gy + (dy * i / steps)
            for w in walls:
                if w.collidepoint(cx, cy):
                    return False
        return True

    def draw(self, surface: pygame.Surface, screen_w: int, screen_h: int):
        gx, gy = self.rect.center
        color_vision = (
            COLOR_VISION_STUN if self.state == "STUNNED" else
            (COLOR_VISION_ALERT if self.state == "SUSPICIOUS" else COLOR_VISION_NORMAL)
        )

        cone_surf = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        start_ang = self.angle - self.fov / 2
        end_ang = self.angle + self.fov / 2

        points = [(gx, gy)]
        for i in range(13):
            ang = math.radians(start_ang + (i / 12) * (end_ang - start_ang))
            points.append((gx + math.cos(ang) * self.view_distance, gy + math.sin(ang) * self.view_distance))

        pygame.draw.polygon(cone_surf, color_vision, points)
        surface.blit(cone_surf, (0, 0))

        # Render Core Guard
        guard_color = (255, 60, 80) if self.type == "PATROL" else ((255, 170, 0) if self.type == "TURRET" else (200, 30, 220))
        pygame.draw.circle(surface, guard_color, (gx, gy), 11)
        ex = gx + math.cos(math.radians(self.angle)) * 14
        ey = gy + math.sin(math.radians(self.angle)) * 14
        pygame.draw.line(surface, (255, 255, 255), (gx, gy), (ex, ey), 2)