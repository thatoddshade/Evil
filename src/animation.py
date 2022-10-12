import pygame
import settings


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name, width=32, height=32, speed=2):
        super().__init__()
        self.status = "moving"
        self.sprite_sheet = pygame.image.load(
            f'../images/sprites/{name}/{self.status}.png'
        ).convert()
        self.name = name
        self.animation_index = 0
        self.clock = 0
        self.width, self.height = width, height
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(self.height),
            'right': self.get_images(self.height * 2),
            'up': self.get_images(self.height * 3)
        }
        self.speed = speed
        # self.current_animation = "down"

    def change_layer(self, layer):
        for group in self.groups():
            group.change_layer(self, layer)

    def change_status(self, status):
        self.sprite_sheet = pygame.image.load(
            f'../images/sprites/{self.name}/{status}.png'
        )
        self.status = status

        # update animation frames
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(self.height),
            'right': self.get_images(self.height * 2),
            'up': self.get_images(self.height * 3)
        }

    def change_animation(self, name):
        # self.current_animation = name
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 6 * settings.delta_time

        if self.clock >= 100:

            self.animation_index += 1  # skip to the next image

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * self.width
            image = self.get_image(x, y)
            images.append(image)

        images.append(self.get_image(self.width, y))
        return images

    def get_image(self, x, y):
        image = pygame.Surface([self.width, self.height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, self.width, self.height))
        return image
