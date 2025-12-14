import pygame
from src.Class.Drawable import Drawable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Class.main import main
from src.calc import calc_cps

class ScoreDisplay(Drawable):
    def __init__(self, parent: 'main'):
        self.Parent = parent
        self.font_large = pygame.font.SysFont('arial', 48)
        self.font_medium = pygame.font.SysFont('arial', 32)
        self.font_small = pygame.font.SysFont('arial', 24)

        self.money_icon = parent.assethandler.get("argent")

        super().__init__("score_display", parent, self._draw_score)

    def _draw_score(self, surface):
        background_rect = pygame.Rect(20, 20, 450, 120)
        pygame.draw.rect(surface, (0, 0, 0, 180), background_rect, border_radius=10)

        score_text = f"{self._format_num(self.Parent.money)}"
        score_surf = self.font_large.render(score_text, True, (255, 215, 0))
        surface.blit(score_surf, (30, 30))
        currency_name = getattr(self.Parent, 'currency_name', 'Cookies')
        currency_surf = self.font_medium.render(currency_name, True, (200, 200, 200))
        surface.blit(currency_surf, (30, 75))
        cps = calc_cps({"buildings": self.Parent.buildings},
                       getattr(self.Parent, 'upgrade_manager', None))
        cps_text = f"par seconde: {self._format_num(cps)}"
        cps_surf = self.font_small.render(cps_text, True, (150, 255, 150))
        surface.blit(cps_surf, (30, 110))
        click_power = self.Parent.click_power
        if hasattr(self.Parent, 'upgrade_manager') and self.Parent.upgrade_manager:
            effects = self.Parent.upgrade_manager.apply_upgrades({"buildings": self.Parent.buildings})
            click_power *= effects.get("click_multiplier", 1.0)

        click_text = f"par clic: {self._format_num(click_power)}"
        click_surf = self.font_small.render(click_text, True, (255, 200, 100))
        surface.blit(click_surf, (250, 110))

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
            return f"{x:.1f}"
