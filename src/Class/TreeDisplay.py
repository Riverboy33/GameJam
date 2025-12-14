import pygame
from src.Class.Drawable import Drawable
from src.utils.Vector2 import Vector2
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main

class TreeDisplay(Drawable):
    def __init__(self, parent: 'main', position: Vector2, max_size=300):
        self.Parent = parent
        self.position = position
        self.scale = 1.0
        self.target_scale = 1.0
        self.animation_speed = 10.0

        tree_original = parent.assethandler.get("arbre1")
        if tree_original:
            original_width = tree_original.get_width()
            original_height = tree_original.get_height()

            scale_factor = max_size / max(original_width, original_height)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)

            self.tree_asset = pygame.transform.scale(tree_original, (new_width, new_height))
            self.base_width = new_width
            self.base_height = new_height
        else:
            self.tree_asset = None
            self.base_width = 0
            self.base_height = 0

        super().__init__("tree_display", parent, self._draw_tree)
        parent.add_event(self._handle_event)

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.tree_asset:
                rect = self.tree_asset.get_rect(center=(self.position.x, self.position.y))
                if rect.collidepoint(mouse_pos):
                    self.on_click()

    def on_click(self):
        click_value = self.Parent.click_power
        if hasattr(self.Parent, 'upgrade_manager') and self.Parent.upgrade_manager:
            effects = self.Parent.upgrade_manager.apply_upgrades({"buildings": self.Parent.buildings})
            click_value *= effects.get("click_multiplier", 1.0)

        self.Parent.money += click_value
        self.target_scale = 0.9
        self.scale = 0.9

    def _draw_tree(self, surface):
        if self.tree_asset:
            if self.scale < self.target_scale:
                self.scale = min(self.scale + self.animation_speed * 0.016, self.target_scale)
            elif self.scale > self.target_scale:
                self.scale = max(self.scale - self.animation_speed * 0.016, self.target_scale)

            if self.scale < 1.0:
                self.target_scale = 1.0

            scaled_width = int(self.base_width * self.scale)
            scaled_height = int(self.base_height * self.scale)
            scaled_tree = pygame.transform.scale(self.tree_asset, (scaled_width, scaled_height))

            rect = scaled_tree.get_rect(center=(self.position.x, self.position.y))
            surface.blit(scaled_tree, rect)
