import pygame
from src.Class.Drawable import Drawable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main
from src.Class.UiButton import UiButton
from src.calc import BUILDINGS, building_cost

class BuildingMenu(Drawable):
    def __init__(self, parent: 'main', *, button_scale: float = 0.5, uniform_size: tuple | None = None,
                 top_margin: int = 150, spacing: int = 12, margin_right: int = 20):
        self.Parent = parent
        self.font = pygame.font.SysFont('arial', 24)
        self.title_font = pygame.font.SysFont('arial', 32)
        self.buttons = []
        self.building_buttons = {}
        # layout: place buttons on the right side of the window
        self.button_scale = float(button_scale)
        self.uniform_size = tuple(uniform_size) if uniform_size is not None else None
        self.top_margin = int(top_margin)
        self.spacing = int(spacing)
        self.margin_right = int(margin_right)

        y_offset = self.top_margin
        win_w = parent.window.get_width() if hasattr(parent, 'window') else 800
        panel_x = win_w - self.margin_right

        # compute maximum allowed button height to avoid overly large images
        win_h = parent.window.get_height() if hasattr(parent, 'window') else 800
        max_btn_h = max(40, int((win_h - self.top_margin - 40) / max(1, len(BUILDINGS))))

        for building in BUILDINGS:
            icon = parent.assethandler.get(building.id)

            # Determine button size: uniform_size > scaled icon native size > fallback default
            if self.uniform_size:
                btn_w, btn_h = int(self.uniform_size[0]), int(self.uniform_size[1])
            elif icon:
                icon_w, icon_h = icon.get_size()
                btn_w = max(40, int(icon_w * self.button_scale))
                btn_h = max(30, int(icon_h * self.button_scale))
            else:
                btn_w, btn_h = 200, 70

            # Clamp height to avoid huge buttons
            if btn_h > max_btn_h:
                scale_down = max_btn_h / btn_h
                btn_h = max_btn_h
                btn_w = max(40, int(btn_w * scale_down))

            x_right = panel_x - btn_w

            button = UiButton(
                parent,
                x=x_right,
                y=y_offset,
                width=btn_w,
                height=btn_h,
                text=building.name,
                icon=icon,
                callback=lambda b_id=building.id: self.buy_building(b_id)
            )
            self.buttons.append(button)
            self.building_buttons[building.id] = button
            # increment y by button height + spacing
            y_offset += btn_h + self.spacing

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
        # draw title above the right-side panel
        win_w = surface.get_width()
        panel_x = win_w - self.margin_right
        title_x = panel_x - 160
        title_surf = self.title_font.render("Outils", True, (255, 255, 255))
        surface.blit(title_surf, (title_x, 110))

        for button in self.buttons:
            button.draw(surface)

        for building in BUILDINGS:
            button = self.building_buttons.get(building.id)
            if button:
                current_count = self.Parent.buildings.get(building.id, 0)
                cost = building_cost(building.id, current_count)

                count_text = f"x{current_count}"
                count_surf = self.font.render(count_text, True, (200, 200, 200))
                # place count at top-left of the button
                surface.blit(count_surf, (button.x + 6, button.y + 6))

                cost_text = f"{self._format_num(cost)}"
                cost_surf = self.font.render(cost_text, True, (255, 215, 0))
                # place cost at bottom-right of the button
                surface.blit(cost_surf, (button.x + button.width - cost_surf.get_width() - 6, button.y + button.height - cost_surf.get_height() - 6))

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
