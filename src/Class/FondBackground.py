import pygame
from src.Class.Drawable import Drawable
from src.utils.Vector2 import Vector2
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main

class FondBackground(Drawable):
    def __init__(self, parent: 'main', position: Vector2, max_size=300):
        self.Parent = parent
        self.position = position

        fond_original = parent.assethandler.get("fond")
        if fond_original:
            original_width = fond_original.get_width()
            original_height = fond_original.get_height()

            scale_factor = max_size / max(original_width, original_height)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            self.fond_asset = pygame.transform.scale(fond_original, (new_width, new_height))
        else:
            self.fond_asset = None

        super().__init__("fond_background", parent, self._draw_fond)

    def _draw_fond(self, surface):
        if self.fond_asset:
            rect = self.fond_asset.get_rect(center=(self.position.x, self.position.y))
            surface.blit(self.fond_asset, rect)
