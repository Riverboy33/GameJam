import pygame
import sys

from src.utils.Vector2 import Vector2
from src.Class.asset import assethandler

from src.Class.BackgroundInterface import BackgroundInterface
from src.Class.FondBackground import FondBackground
from src.Class.main import main
from src.Class.TreeDisplay import TreeDisplay
from src.Class.BuildingMenu import BuildingMenu
from src.Class.ScoreDisplay import ScoreDisplay

pygame.init()

# Create the display first so surfaces can be converted safely by asset loader
screen = pygame.display.set_mode((800, 800))

ASSET_HANDLER = assethandler().init()

GAME = main(screen, ASSET_HANDLER)

GAME.add_drawable(FondBackground(GAME, Vector2(x=250, y=400), max_size=700))

GAME.add_drawable(BackgroundInterface(GAME))

GAME.add_drawable(TreeDisplay(GAME, Vector2(x=250, y=450), max_size=1000))

GAME.add_drawable(BuildingMenu(GAME))

GAME.add_drawable(ScoreDisplay(GAME))

GAME.run()
