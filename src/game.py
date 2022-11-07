import pygame
from settings import *
from map import MapManager
from entity import Player
from dialog import DialogBox
import random
import sys
import time
import math
from debug import debug


class Game:
    def __init__(self):
        # create a window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption('Evil')
        icon = pygame.image.load("../images/icon.png")
        pygame.display.set_icon(icon)

        self.fullscreen = False
        self.screen_shake = 0
        self.render_offset = [0, 0]

        # ASCII art
        print("_____            _ _")
        print("|      \      /   |     |")
        print("|___    \    /    |     |")
        print("|        \  /     |     |")
        print("|____     \/     _|_    |___")
        print('\n(*° ω °*)')

        # custom mouse cursor
        surf = pygame.image.load('../images/cursor.png').convert_alpha()
        cursor = pygame.cursors.Cursor((0, 0), surf)
        pygame.mouse.set_cursor(cursor)


        # generate a player
        self.player = Player()
        self.map_manager = MapManager(self.display, self.player)
        self.dialog_box = DialogBox(self.player)

        # Starting the mixer
        pygame.mixer.init()
        # Loading the song
        pygame.mixer.music.load("../sounds/inn.ogg")
        # Setting the volume
        pygame.mixer.music.set_volume(0.25)
        # Start playing the song
        pygame.mixer.music.play(-1, 0, 7500)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # movement
        if self.player.direction.magnitude() != 0:
            self.player.direction = self.player.direction.normalize()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.player.speed *= 2
        if keys[pygame.K_z] and not keys[pygame.K_s]:
            self.player.direction.y = -1
        elif keys[pygame.K_s] and not keys[pygame.K_z]:
            self.player.direction.y = 1
        else:
            self.player.direction.y = 0
        if keys[pygame.K_q] and not keys[pygame.K_d]:
            self.player.direction.x = -1
        elif keys[pygame.K_d] and not keys[pygame.K_q]:
            self.player.direction.x = 1
        else:
            self.player.direction.x = 0

        if keys[pygame.K_F4] or (keys[pygame.K_LALT] and keys[13]):
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                self.screen = pygame.display.set_mode(
                    (WIDTH, HEIGHT),
                    pygame.FULLSCREEN
                )
            else:
                self.screen = pygame.display.set_mode(
                    (WIDTH, HEIGHT),
                )

        self.player.move()

    def update(self):
        self.map_manager.update()

    def display_ui(self, fps):
        # display coins amount
        coin_amount = 0
        for slot in self.player.inventory:
            if slot["type"] == "coin":
                coin_amount += slot["number"]

        text = "Coins : " + str(coin_amount)
        self.display.blit(
            get_font(FONT_SIZE).render(text, False, "#f9c22b"),
            (WIDTH * 0.84, 10)
        )

        # display fps
        debug(self.display, str(math.ceil(fps)) + " fps", WIDTH * 0.08)

        # display current player's location
        player_x = str(math.ceil(self.player.position[0]))
        player_y = str(math.ceil(self.player.position[1]))
        debug(
            self.display,
            "X : " + player_x + " Y : " + player_y,
            WIDTH * 0.08,
            40
        )

        debug(
            self.display,
            str(pygame.mouse.get_pos()),
            pygame.mouse.get_pos()[0] + 16,
            pygame.mouse.get_pos()[1] + 16
        )

    def run(self):
        global clock
        clock = pygame.time.Clock()

        # game loop
        running = True
        while running:
            update_delta_time()
            mouse_pos = pygame.mouse.get_pos()
            self.player.save_location()
            self.handle_input()
            if not self.dialog_box.reading:
                self.player.speed = self.player.stats["speed"]
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.display)

            if self.screen_shake:
                self.screen_shake -= 1
                self.render_offset[0] = random.randint(0, 8) - 4
                self.render_offset[1] = random.randint(0, 8) - 4

            self.display_ui(clock.get_fps())

            self.screen.blit(
                pygame.transform.scale(self.display, (WIDTH, HEIGHT)),
                self.render_offset
            )

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.JOYAXISMOTION and not pygame.KEYDOWN:
                    print("JOYSTICK")
                    if event.axis < 2:
                        self.player.direction[event.axis] = event.value
                        self.player.move()
                        print('event axis', event.axis)
                        print('event value', event.value)
                        print("direction", self.player.direction)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == 13:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                    if event.key == pygame.K_i:
                        print(self.player.inventory, "\n")

            clock.tick(FPS)

        pygame.quit()
        sys.exit()
