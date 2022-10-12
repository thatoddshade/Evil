import pygame
from pygame import mixer
import pytmx, pyscroll
from settings import *
from map import MapManager
from entity import Player, Item
from dialog import DialogBox

class Game:
    def __init__(self):
        # create a window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Evil')
        print("\n_____            _ _\n|      \      /   |     |\n|___    \    /    |     |\n|        \  /     |     |\n|____     \/     _|_    |___")
        print('\n(*° ω °*)')

        # hide mouse pointer
        pygame.mouse.set_visible(False)

        # generate a player
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = DialogBox(self.player)

        # Starting the mixer
        mixer.init()
        # Loading the song
        mixer.music.load("../sounds/inn.ogg")
        # Setting the volume
        mixer.music.set_volume(1)
        # Start playing the song
        mixer.music.play(-1, 0, 7500)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # movement
        if self.player.direction.magnitude() != 0:
            self.player.direction = self.player.direction.normalize()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.speed *= 2
        if keys[pygame.K_UP]:
            self.player.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.player.direction.y = 1
        else:
            self.player.direction.y = 0
        if keys[pygame.K_LEFT]:
            self.player.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.player.direction.x = 1
        else:
            self.player.direction.x = 0

        if keys[103]:
            self.map_manager.current_map = "anoying_room"
            self.map_manager.teleport_player("spawn_anoying_room")

        self.player.move()

    def update(self):
        self.map_manager.update()

    def display_ui(self):
        # display coins amount
        self.screen.blit(pygame.font.Font("../fonts/default_font.ttf", FONT_SIZE).render("Coins : " + str(self.player.inventory['coin']), True, (255, 255, 128)), (WIDTH * 0.84, 10))


    def run(self):

     clock = pygame.time.Clock()

     # game loop
     running = True
     while running:

        self.player.save_location()
        self.handle_input()
        if self.dialog_box.reading is False:
             self.player.speed = self.player.stats["speed"]
        self.update()
        self.map_manager.draw()
        self.dialog_box.render(self.screen)

        # display GUI
        self.display_ui()

        # display custom mouse pointer
        self.screen.blit(pygame.transform.scale(pygame.image.load('..\images\cursor.png').convert_alpha(), (32, 32)), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.JOYAXISMOTION:
                if event.axis < 2:
                    self.player.direction[event.axis] = event.value
                    self.player.move()
                    print('event axis', event.axis)
                    print('event value', event.value)
                    print("direction", self.player.direction)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == 13:
                    self.map_manager.check_npc_collisions(self.dialog_box)



        clock.tick(FPS)

    pygame.quit()
