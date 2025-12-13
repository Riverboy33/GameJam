#Game handler
import pygame.display
from pygame import Vector2

from Class.text import game_text
from src.Class.ClickButton import ClickButton
from src.Class.main import main
from src.Class.asset import assethandler, fonthandler
from src.Class.text import game_text, format_num

pygame.init()
pygame.font.init()

Window = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Tree clicker")
ASSET_HANDLER = assethandler().init()
FONT_HANDLER = fonthandler()
GAME = main(ASSET_HANDLER, FONT_HANDLER)

GAME.add_event(GAME.quit)
GAME.add_drawable(ClickButton(GAME, Vector2(x=400, y=400)))
GAME.add_text(game_text("money",GAME, Vector2(x=100, y=0),"money: " +  format_num(GAME.money)))

while GAME.isRunning:
    dt = GAME.clock.tick(GAME.FPS) / 1000.0

    events = pygame.event.get()
    GAME.handle_event(events)
    GAME.rendering()

pygame.quit()
