import pygame
from ... import support


class Font:
    def __init__(self, path):
        self.spacing = 1

        self.character_order = open("character_order.txt", "r").read()

        font_img = pygame.image.load(path).convert()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = support.clip(
                    font_img,
                    x - current_char_width,
                    0,
                    current_char_width,
                    font_img.get_height(),
                )
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters["A"].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != " ":
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing


small_font = Font("../../data/images/font/small_font.png")
large_font = Font("../../data/images/font/large_font.png")
