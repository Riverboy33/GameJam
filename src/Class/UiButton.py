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
        color = (100, 100, 100) if not self.hovered else (150, 150, 150)
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=5)
        pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 2, border_radius=5)

        if self.icon:
            icon_rect = self.icon.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            surface.blit(self.icon, icon_rect)

        if self.text:
            text_surf = self.font.render(self.text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            surface.blit(text_surf, text_rect)
