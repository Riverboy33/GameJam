import pygame
from typing import TYPE_CHECKING, Callable, Optional
if TYPE_CHECKING:
    from src.Class.main import main

class UiButton:
    def __init__(self, parent: 'main', x: int, y: int, width: int, height: int,
                 text: str = "", icon: Optional[pygame.Surface] = None,
                 callback: Optional[Callable] = None):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.icon = icon
        self.callback = callback
        self.hovered = False
        self.font = pygame.font.SysFont('arial', 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            self.hovered = self.is_over(mouse_pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.is_over(mouse_pos) and self.callback:
                self.callback()

    def is_over(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

    def draw(self, surface):
        # If an icon is provided, use it as the button background (scaled to button size)
        rect = (self.x, self.y, self.width, self.height)

        if self.icon:
            try:
                bg = pygame.transform.smoothscale(self.icon, (self.width, self.height))
            except Exception:
                bg = pygame.transform.scale(self.icon, (self.width, self.height))
            surface.blit(bg, (self.x, self.y))

            # hover overlay
            if self.hovered:
                overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, 40))
                surface.blit(overlay, (self.x, self.y))

            # draw border
            pygame.draw.rect(surface, (200, 200, 200), rect, 2, border_radius=5)

            # draw text centered on the image
            if self.text:
                text_surf = self.font.render(self.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
                surface.blit(text_surf, text_rect)
        else:
            # No icon provided: do not draw a rectangle fallback — buttons must be images.
            # Optionally show text if present (not as a button background).
            if self.text:
                text_surf = self.font.render(self.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(topleft=(self.x, self.y))
                surface.blit(text_surf, text_rect)
