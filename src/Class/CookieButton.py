import pygame

class CookieButton:
    def __init__(self, center: tuple[int, int], radius: int):
        self.center = center
        self.radius = radius
        self.hover = False

    def contains(self, pos: tuple[int, int]) -> bool:
        dx = pos[0] - self.center[0]
        dy = pos[1] - self.center[1]
        return (dx * dx + dy * dy) <= (self.radius * self.radius)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.contains(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.contains(event.pos):
                return True
        return False

    def draw(self, screen: pygame.Surface):
        r = self.radius + (6 if self.hover else 0)
        pygame.draw.circle(screen, (70, 55, 35), self.center, r + 10)
        pygame.draw.circle(screen, (210, 160, 95), self.center, r)
        pygame.draw.circle(screen, (235, 195, 130), (self.center[0] - 14, self.center[1] - 10), r - 18)
        for off in ((-50, -10), (-10, 35), (35, -25), (55, 25), (10, -55), (-40, 45)):
            pygame.draw.circle(screen, (115, 80, 45), (self.center[0] + off[0], self.center[1] + off[1]), 8)
