from dataclasses import dataclass
from entity import Entity
import pygame
import settings


@dataclass
class Item:
    name: str
    max_stack: int
    lore: str


class ItemSprite(Entity):
    def __init__(self, x, y, status):
        super().__init__("items", x, y)
        # graphic setup
        self.width, self.height = 16, 16
        self.change_path(status)
        self.image = self.get_image(00, 00)
        self.image.set_colorkey([0, 0, 0])

    def change_animation(self, name): pass

    def move_back(self): pass

    def give(self, player):
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sounds/coin.ogg"))

        for i in range(0, len(player.inventory)):
            if player.inventory[i]["type"] == self.status:
                if player.inventory[i]["number"] < settings.default_max_stack:
                    player.inventory[i]["number"] += 1
                    break
                # else:
                #     continue
            if i >= len(player.inventory) - 1:
                player.inventory.append({"type": self.status, "number": 1})

        self.kill()
