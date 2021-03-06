import pygame
import sys
from pathlib import Path
from typing import Any

pygame.init()
pygame.mixer.init()

DEBUG = "-d" in sys.argv or "--debug" in sys.argv
DEBUG_FREEZE = False
PATH = Path(__file__).parent.parent
window = pygame.display.set_mode((620, 620), pygame.RESIZABLE)
pygame.display.set_caption("ParaPac - Loading...")
clock = pygame.time.Clock()
font = pygame.font.Font(PATH / "assets/VT323.ttf", 24)
font2 = pygame.font.Font(PATH / "assets/VT323.ttf", 20)
font64 = pygame.font.Font(PATH / "assets/VT323.ttf", 64)
fps = 0

maps = []
map_area_x, map_area_y = 0, 0
map_area_width, map_area_height = 1, 1
map_area_ratio = 1

# Uses Any to make PyCharm shut up
player: Any = None
dashboard = None
active_map: Any = None
game_loop: Any = None
active_map_id: int = 0
alpha: int = 255

score: int = 0
coins: int = 0


class Transition:
    """Enum for the transition"""
    NOT_TRANSITIONING = 0
    FADING = 1
    REAPPEARING = 2


transitioning_mode = Transition.NOT_TRANSITIONING
transition_timer = -25
