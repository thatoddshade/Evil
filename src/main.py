__author__ = "Shad0w_57"
__copyright__ = ""
__credits__ = ["Shad0w_57", "Omegatomic"]
__license__ = "MPL"
__version__ = "0.0a1"
__maintainer__ = "Shad0w_57"
__email__ = ""
__status__ = "Production"

import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
