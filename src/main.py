__author__ = "Shad0w_57"
__copyright__ = ""
__credits__ = {"Shad0w_57": "Programming and Graphics", "Omegatomic": "Music & Sound effects"}
__license__ = "MPL"
__version__ = "0.0a3"
__maintainer__ = "Shad0w_57"
__email__ = ""
__status__ = "Production"

# general setup
import pygame
from game import Game

if __name__ == '__main__':
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        print(joystick.get_name())
    pygame.init()
    game = Game()
    game.run()
