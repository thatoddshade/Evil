import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name, speed=2):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'..\images\sprites\{name}\spritesheet.png').convert_alpha()
        self.status = "spritesheet"
        self.name = name
        self.animation_index = 0
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }
        self.speed = speed

    def change_status(self, status):
        self.sprite_sheet = pygame.image.load(f'..\images\sprites\{self.name}\{status}.png').convert_alpha()
        self.status = status

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 6

        if self.clock >= 100:

            self.animation_index += 1 # skip to the next image

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0

            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i*32
            image = self.get_image(x, y)
            images.append(image)

        images.append(self.get_image(32, y))
        return images


    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
