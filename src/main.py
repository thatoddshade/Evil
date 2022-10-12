# general setup
import pygame
from game import Game

if __name__ == '__main__':
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(
        pygame.joystick.get_count()
    )]
    for joystick in joysticks:
        print(joystick.get_name())
    pygame.init()
    game = Game()
    game.run()
