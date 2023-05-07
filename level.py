import pygame
from settings import *
from support import *
from debug import debug
from tile import Tile
from player import Player

class Level:
    def __init__(self, level_number: int):

        self.level_file = "../levels/level_" + str(level_number)
        self.won_level = False
        self.player_dead = False

        self.turn_number = 0

        #get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprite
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):
        
        # loads all map files for spawn locations and ground
        layouts = {
            'boundary': import_csv_layout(self.level_file + 'map_FloorBlocks.csv'),
            'grass': import_csv_layout(self.level_file + 'map_Grass.csv'),
            'object': import_csv_layout(self.level_file + 'map_Objects.csv'),
            'entities': import_csv_layout(self.level_file + 'map_Entities.csv')
        }

        # loads images for grass and stationary objects 
        # TODO organize files
        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects'),
        }

        # loops go through each square in each map table
        # and spawn in the apropriate tile or entity
        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # creates boundary around areas the player can not cross
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')

                        # spawns non interactable objects 
                        if style == 'object':
                            object_surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object', object_surf)
                        
                        # spawns the player and enemies
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites], 
                                    self.obstacle_sprites, 
                                    self.create_attack, 
                                    self.destroy_attack, 
                                    self.create_magic)

    def player_turn(self):
        self.turn_number += 1

    def run(self):
        self.player_turn()
        self.visible_sprites.custom_draw(self.player)

# to help control the camera
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):
        """
        moves the camera via offsets and draws the floor
        """

        #getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        """
        updates enemies
        """

        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']

        for enemy in enemy_sprites:
            enemy.enemy_update(player)
