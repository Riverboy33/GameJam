import pygame.image
from pygame import Vector3

class Drawable:
    def __init__(self, Name,Parent ,Func):
        self.draw = Func
        self.Parent = Parent
        self.Name = Name

    def Draw(self):
        if callable(self.draw):
            print("Inside self.draw detected")
            self.draw(self.Parent.window)
