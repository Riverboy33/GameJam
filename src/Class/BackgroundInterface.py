import pygame
from src.Class.Drawable import Drawable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main

class BackgroundInterface(Drawable):
    def __init__(self, parent: 'main'):
        self.Parent = parent

        interface_original = parent.assethandler.get("newinterface")
        window_width = parent.window.get_width()
        window_height = parent.window.get_height()

        self.interface_asset = pygame.transform.scale(interface_original, (window_width, window_height))

        super().__init__("background_interface", parent, self._draw_interface)

    def _draw_interface(self, surface):
        surface.blit(self.interface_asset, (0, 0))
