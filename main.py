import pygame
from settings import *
from level import Level
import sys

class Game:
    def __init__(self):
        
        # initializing Game window
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        self.level_number = 0

        #death screen setup
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.restart_text_surf = self.font.render("Haha loser", False, TEXT_COLOR)
        self.restart_text_rect = self.text_surf.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        self.restart_message = self.font.render("Press Enter to restart", False, TEXT_COLOR)
        self.restart_rect = self.restart_message.get_rect(center = (WIDTH / 2, HEIGHT - 100))

        #Level victory setup

        #Game victory setup

    def run(self):
        
        #The game loop that continues so long as the user does not die
        #or click on the exit button
        while True:
            self.level = Level(self.level_number) 
            self.would_like_to_continue = False

            while not self.level.player_dead and not self.level.won_level:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            self.level.toggle_menu()

                self.screen.fill(WATER_COLOR)
                self.level.run()
                pygame.display.update()
                self.clock.tick(FPS)

            if self.level.player_dead:
                # loop runs after player dies and has not reset or exited
                while not self.would_like_to_continue:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_KP_ENTER:
                                self.would_like_to_continue = True
                    
                    self.screen.fill('Blue')
                    self.screen.blit(self.restart_text_surf, self.restart_text_rect)
                    self.screen.blit(self.restart_message, self.restart_rect)
                    pygame.display.update()
                    self.clock.tick(FPS)

            # Increase level and show level win screen
            elif self.level.won_level:
                self.level_number += 1


            if self.level_number > TOTAL_LEVEL_NUMBER:
                break

        #create game win screen

if __name__ == "__main__":
    game = Game()
    game.run()