import pygame

class Level:
    def __init__(self, level_number: int):

        self.level_file = "../levels/level_" + str(level_number)
        self.won_level = False
        self.player_dead = False
