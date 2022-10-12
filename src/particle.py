from animation import AnimateSprite
import pygame
import settings
import time


class Particle(AnimateSprite):
    def __init__(self, x, y, status):
        super().__init__("particles", x, y)
        # graphic setup
        self.width, self.height = 16, 16
        self.change_status(status)
        self.image = self.get_image(00, 00).convert_alpha()
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.sprite_sheet = pygame.image.load(
            f'../images/sprites/{self.name}/{"dust"}.png'
        ).convert()

        self.image.set_alpha(100)
        self.opacity = self.image.get_alpha()

        # movement & hitboxes
        self.position = [x, y]
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.appearance_time = time.time()

    def update(self):
        self.change_layer(4)
        self.change_animation("down")
        self.rect.topleft = self.position
        self.hitbox.midbottom = self.rect.midbottom
        # self.opacity -= settings.delta_time ** 10
        # self.image.set_alpha(
        #     self.opacity
        # )
        if time.time() - self.appearance_time >= 0.5:
            self.kill()
