from pygame import Vector3


class Drawable:
    def __init__(self, Position : Vector3, DrawMethode, DrawObject):
        self.Position = Position
        self.obj = DrawObject
        self.draw_methode = DrawMethode

    def Draw(self):
        if callable(self.draw_methode):
            self.draw_methode(self.obj)
