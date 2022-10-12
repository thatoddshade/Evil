import pygame
from pygame import mixer
import pytmx
import pyscroll

from map import MapManager
from player import Player
from dialog import DialogBox

class Game:
    def __init__(self):
        # create a window
        self.screen = pygame.display.set_mode((1300, 800))
        pygame.display.set_caption('Evil')

        # generate a player
        print('Displaying the player character...')
        self.player = Player()
        print('(*° ω °*)')
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox(self.player)

        # Starting the mixer
        mixer.init()
        #  Loading the song
        mixer.music.load("../mus/town.ogg")
        # Setting the volume
        mixer.music.set_volume(0.075)
        # Start playing the song
        mixer.music.play(-1, 0, 7500)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
            self.player.speed *= 2
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        if pressed[116]:
            print('Teleporting to anoying room...')
            self.map_manager.current_map = "anoying_room"
            self.map_manager.teleport_player("spawn_anoying_room")

    def update(self):
        self.map_manager.update()

    def run(self):

     clock = pygame.time.Clock()

     # game loop
     running = True
     while running:

        self.player.save_location()
        self.handle_input()
        if self.dialog_box.reading is False:
            self.player.speed = self.player.old_speed
        self.update()
        self.map_manager.draw()
        self.dialog_box.render(self.screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == 13:
                    self.map_manager.check_npc_collisions(self.dialog_box)

        clock.tick(60)

    pygame.quit()
