from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main

class Drawable:
    def __init__(self, name: str, parent: 'main', draw_func):
        self.name = name
        self.Parent = parent
        self.draw_func = draw_func

    def draw(self, surface):
        if self.draw_func:
            self.draw_func(surface)
