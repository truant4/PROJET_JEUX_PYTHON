import pygame
import sys
from game import Game
from menu import Menu

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1920, 1200))
    pygame.display.set_caption("The Legend of JAY")

    while True:
        menu = Menu(screen, title=" The Legend of JAY", background_image="background.jpg")
        action = menu.run()

        if action == "quit":
            pygame.quit()
            sys.exit()

        if action == "play":
            game = Game(screen)
            game.run()
            