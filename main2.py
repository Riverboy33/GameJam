#Game handler
import pygame.display
from pygame import Vector2

from src.Class.ClickButton import ClickButton
from src.Class.main import main
from src.Class.asset import assethandler

Window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tree clicker")
ASSET_HANDLER = assethandler().init()
GAME = main(ASSET_HANDLER)

def format_num(x: float) -> str:
    if x < 1000:
        return f"{x:.0f}"
    for suffix, div in (("K", 1e3), ("M", 1e6), ("B", 1e9), ("T", 1e12)):
        if x < div * 1000:
            return f"{x / div:.2f}{suffix}"
    return f"{x:.2e}"

GAME.add_event(GAME.quit)
GAME.add_drawable(ClickButton(GAME, Vector2(x=400, y=400)))

while GAME.isRunning:
    dt = GAME.clock.tick(GAME.FPS) / 1000.0

    events = pygame.event.get()
    GAME.handle_event(events)
    GAME.rendering()

pygame.quit()
