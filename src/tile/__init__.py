import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(topleft=pos)
