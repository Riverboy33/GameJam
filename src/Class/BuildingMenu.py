import pygame
from src.Class.Drawable import Drawable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main
from src.Class.UiButton import UiButton
from src.calc import BUILDINGS, building_cost

class BuildingMenu(Drawable):
    def __init__(self, parent: 'main'):
        self.Parent = parent
        self.font = pygame.font.SysFont('arial', 24)
        self.title_font = pygame.font.SysFont('arial', 32)
        self.buttons = []
        self.building_buttons = {}

        y_offset = 200
        for building in BUILDINGS:
            icon = parent.assethandler.get(building.id)
            if icon:
                icon = pygame.transform.scale(icon, (50, 50))

            button = UiButton(
                parent,
                x=650,
                y=y_offset,
                width=120,
                height=60,
                text=building.name,
                icon=icon,
                callback=lambda b_id=building.id: self.buy_building(b_id)
            )
            self.buttons.append(button)
            self.building_buttons[building.id] = button
            y_offset += 80

        super().__init__("building_menu", parent, self._draw_menu)
        parent.add_event(self._handle_event)

    def _handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def buy_building(self, building_id: str):
        current_count = self.Parent.buildings.get(building_id, 0)
        cost = building_cost(building_id, current_count)

        if self.Parent.money >= cost:
            self.Parent.money -= cost
            self.Parent.buildings[building_id] = current_count + 1

    def _draw_menu(self, surface):
        title_surf = self.title_font.render("Buildings", True, (255, 255, 255))
        surface.blit(title_surf, (620, 150))

        for button in self.buttons:
            button.draw(surface)

        for building in BUILDINGS:
            button = self.building_buttons.get(building.id)
            if button:
                current_count = self.Parent.buildings.get(building.id, 0)
                cost = building_cost(building.id, current_count)

                count_text = f"x{current_count}"
                count_surf = self.font.render(count_text, True, (200, 200, 200))
                surface.blit(count_surf, (button.x - 40, button.y + 15))

                cost_text = f"{self._format_num(cost)}"
                cost_surf = self.font.render(cost_text, True, (255, 215, 0))
                surface.blit(cost_surf, (button.x + 10, button.y + 65))

    def _format_num(self, x: float) -> str:
        if x >= 1e12:
            return f"{x / 1e12:.2f}T"
        elif x >= 1e9:
            return f"{x / 1e9:.2f}B"
        elif x >= 1e6:
            return f"{x / 1e6:.2f}M"
        elif x >= 1e3:
            return f"{x / 1e3:.2f}K"
        else:
            return f"{x:.0f}"
