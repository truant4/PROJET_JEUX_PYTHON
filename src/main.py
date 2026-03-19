import pygame
import sys
from game import Game
from menu import Menu

if __name__ == "__main__":
    pygame.init()

    # Get the actual display resolution, then create a fullscreen window
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    # Or, if you prefer a resizable windowed mode instead:
    # screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)

    pygame.display.set_caption("The Legend of JAY")

    while True:
        menu = Menu(screen, title="The Legend of JAY", background_image="background.jpg")
        action = menu.run()
        if action == "quit":
            pygame.quit()
            sys.exit()
        if action == "play":
            game = Game(screen)
            game.run()