import pygame

from src.Class.objet import Drawable


class main:
    def __init__(self, assethandler):
        """"SERVICE"""
        self.assethandler = assethandler
        self.window = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.events = []
        self.drawable = []

        """Value"""
        self.money = 0
        self.FPS = 60
        self.isRunning = True
        self.clickButton = None
        self.upgradeMenu = None
        self.dt = 0

    def add_event(self, eventFunc):
        if callable(eventFunc):
            self.events.append(eventFunc)
        else:
            print("Cannot add event : ", eventFunc)

    def handle_event(self, events):
        for eventConnected in self.events:
            eventConnected(events)

    def rendering(self):
        self.window.fill((0, 0, 0))
        for drawable  in self.drawable:
            drawable.Draw()
            print(drawable.Name)
        pygame.display.flip()

    def add_drawable(self, obj):
        if isinstance(obj, Drawable):
            self.drawable.append(obj)

    def quit(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.isRunning = False

    def get_element_by_name(self, name : str) -> Drawable | None:
        for element in self.drawable:
            if element.name == name:
                return element
        return None

    def get_element_by_id(self, id : None) -> Drawable | None:
        for i in range(len(self.drawable)):
            if i == id:
                return self.drawable[i]
        return None


