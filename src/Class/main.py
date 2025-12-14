import pygame
import time
from typing import TYPE_CHECKING
from src.Class.Drawable import Drawable

class main:
    def __init__(self, window, assethandler):
        self.window = window
        self.assethandler = assethandler
        self.drawables = []
        self.events = []
        self.running = True
        self.money = 0.0
        self.click_power = 1.0
        self.buildings = {}
        self.upgrade_manager = None
        self.currency_name = "Cookies"
        self.last_update = 0
        self.auto_click_timer = 0
        self.auto_click_interval = 0.1

    def add_event(self, eventFunc):
        self.events.append(eventFunc)

    def add_drawable(self, drawable: Drawable):
        self.drawables.append(drawable)

    def get_element_by_name(self, name: str):
        for drawable in self.drawables:
            if hasattr(drawable, 'name') and drawable.name == name:
                return drawable
        return None

    def run(self):
        clock = pygame.time.Clock()
        self.last_update = time.time()

        while self.running:
            current_time = time.time()
            dt = current_time - self.last_update
            self.last_update = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return

                for event_func in self.events:
                    event_func(event)

            self.update_passive_income(dt)

            self.window.fill((0, 0, 0))

            for drawable in self.drawables:
                drawable.draw(self.window)

            pygame.display.flip()
            clock.tick(60)

    def update_passive_income(self, dt):
        from src.calc import calc_cps
        cps = calc_cps({"buildings": self.buildings}, self.upgrade_manager)
        self.money += cps * dt

        cursor_count = self.buildings.get("cursor", 0)
        if cursor_count > 0:
            self.auto_click_timer += dt
            if self.auto_click_timer >= self.auto_click_interval:
                clicks = int(self.auto_click_timer / self.auto_click_interval)
                self.auto_click_timer -= clicks * self.auto_click_interval

                click_value = self.click_power * cursor_count * clicks
                if self.upgrade_manager:
                    effects = self.upgrade_manager.apply_upgrades({"buildings": self.buildings})
                    click_value *= effects.get("click_multiplier", 1.0)
                self.money += click_value
