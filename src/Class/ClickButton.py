import pygame
from pygame import Vector2
from src.Class.objet import Drawable
from src.Class.main import main

class ClickButton(Drawable):
    def __init__(self, parent : main, position : Vector2):
        self.Parent = parent
        self.asset = parent.assethandler.tree_test
        self.Position = position
        self.rect = self.asset.get_rect(center=(position.x, position.y))
        super().__init__("click_button", parent, lambda surface: surface.blit(self.asset, self.rect))