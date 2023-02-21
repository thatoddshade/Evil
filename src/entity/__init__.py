import pygame
from ..options.dictionary import option_dict as options

# from ..utils import delta_time


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, img_path, groups):
        super().__init__(groups)
        # graphic setup
        self.image = pygame.image.load(img_path)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.math.Vector2()

    def move(self, delta_time):
        # if self.direction.magnitude() != 0:
        #     self.direction = self.direction.normalize()

        if abs(self.direction[0]) < 0.1:
            self.direction[0] = 0
        if abs(self.direction[1]) < 0.1:
            self.direction[1] = 0

        # print(delta_time)
        # print(self.direction)

        # print(delta_time)

        # print(self.direction.x * self.speed * delta_time, self.direction.y * self.speed * delta_time)

        self.rect[0] += self.direction.x * self.speed * delta_time
        self.rect[1] += self.direction.y * self.speed * delta_time


class Player(Entity):
    def __init__(self, pos, groups):
        img_path = "data/images/icon.png"
        super().__init__(pos, img_path, groups)

        # graphic setup
        self.image = pygame.image.load(img_path)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)

        # statistics
        self.speed = 2

    def get_key(self, key: str) -> int:
        return eval(options.get(key, 0))

    def is_pressed(self, key: str) -> bool:
        keys = pygame.key.get_pressed()
        return keys[self.get_key(key)]

    def handle_input(self, delta_time):
        # print(self.rect)

        # print(pygame.joystick)
        # for event in pygame.event.get():
        #     if event.type == pygame.JOYAXISMOTION:
        #         if event.axis < 2:
        #             print("joystick event")
        #             self.direction[event.axis] = event.value

        # if self.is_pressed("key_left"):
        #     # print("left key pressed")
        #     self.direction.x -= 1

        # if self.is_pressed("key_right"):
        #     self.direction.x += 1

        # if not (self.is_pressed("key_right") or self.is_pressed("key_left")) and self.no_input:
        #     self.direction.x = 0

        # if self.is_pressed("key_up"):
        #     self.direction.y -= 1

        # if self.is_pressed("key_down"):
        #     self.direction.y += 1

        # if not (self.is_pressed("key_down") or self.is_pressed("key_up")) and self.no_input:
        #     self.direction.y = 0

        self.move(delta_time)
