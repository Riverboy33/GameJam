import pygame

TEXT = (235, 235, 240)
MUTED = (170, 170, 180)

class UiButton:
    def __init__(self, rect: pygame.Rect, text: str):
        self.rect = rect
        self.text = text
        self.enabled = True
        self.hover = False

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        base = (50, 50, 62)
        if self.enabled and self.hover:
            base = (70, 70, 88)
        if not self.enabled:
            base = (40, 40, 48)

        pygame.draw.rect(screen, base, self.rect, border_radius=10)
        pygame.draw.rect(screen, (90, 90, 110), self.rect, width=2, border_radius=10)
        surf = font.render(self.text, True, TEXT if self.enabled else MUTED)
        screen.blit(surf, surf.get_rect(center=self.rect.center))
