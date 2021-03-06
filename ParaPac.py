import time

import pygame
import os
import sys

from src import common, powerup
from src.world import World
from src.interrupt import *
from src.player import Player
from src.gui import Dashboard
from src.states import MainGameState, MenuState, GameOverState, GameFinishedState


class GameLoop:
    def __init__(self):
        self.state = MenuState()

    def run(self):
        self.setup()
        while True:
            try:
                self.state.run()
                for event in pygame.event.get():
                    self.handle_event(event)

                if self.state.__class__ != self.state.next_state:
                    if self.state.__class__ == MenuState and self.state.next_state == MainGameState:
                        powerup.add_powerup(powerup.PowerUp.IMMUNITY, 12)
                        common.player.immune = True
                        common.player.immunity_duration = powerup.powerups[powerup.PowerUp.IMMUNITY][1]
                        common.player.immunity_timer = time.perf_counter()

                    self.state = self.state.next_state()
            except GameExit:
                sys.exit(0)
            except GameOver:
                self.setup()
                self.state = GameOverState()
                self.state.next_state = GameOverState
            except GameFinish:
                self.setup()
                self.state = GameFinishedState()
                self.state.next_state = GameFinishedState

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            raise GameExit
        self.state.handle_event(event)

    @staticmethod
    def setup():
        pygame.display.set_caption("ParaPac - Pygame Community Summer Team Jam")
        pygame.display.set_icon(pygame.image.load(common.PATH / "assets/logo.png"))

        common.maps = [
            [World(os.path.join("maps", "map_a.txt")), (8, 8, 32), "map_a.txt"],
            [World(os.path.join("maps", "map_b.txt")), (64, 0, 32), "map_b.txt"],
            [World(os.path.join("maps", "map_c.txt")), (0, 64, 32), "map_c.txt"],
            [World(os.path.join("maps", "map_d.txt")), (64, 32, 0), "map_d.txt"],
            [World(os.path.join("maps", "map_e.txt")), (16, 128, 16), "map_e.txt"],
            [World(os.path.join("maps", "map_f.txt")), (216, 216, 216), "map_f.txt"]
        ]

        common.player = Player(19, 30)
        common.active_map_id = 0
        common.active_map = common.maps[common.active_map_id][0]
        common.dashboard = Dashboard()
        for dimension, _bg, _file in common.maps:
            dimension.entities.append(common.player)


if __name__ == "__main__":
    game_loop = GameLoop()
    common.game_loop = game_loop
    game_loop.run()
