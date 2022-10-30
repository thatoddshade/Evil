__author__ = "Shad0w_57"
__copyright__ = ""
__credits__ = {
    "Shad0w_57": "Programming, Designing and Graphics",
    "Omegatomic": "Music",
    "Guytou": "kind of weird but inspiring ideas..."
}
__version__ = "0.0a3"


# general setup
import pygame
import math
import time
import random

last_time = time.time()


def get_font(size, font="../fonts/default_font.ttf"):
    return pygame.font.Font(font, size)


def random_sys_font(size):
    return pygame.font.SysFont(random.choice(pygame.font.get_fonts()), size)


def update_delta_time():
    global delta_time, last_time
    delta_time = time.time() - last_time
    delta_time *= 60
    last_time = time.time()


# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60

ZOOM = ((WIDTH + HEIGHT) / 1000)
DEFAULT_SPRITE_LAYER = 5

# text and GUI
DIALOG_BOX_WIDTH = ((WIDTH / 1.28) * 7) / 10
DIALOG_BOX_HEIGHT = HEIGHT / 7.2

DIALOG_BOX_X_POSITION = (DIALOG_BOX_WIDTH / 2)
DIALOG_BOX_Y_POSITION = (HEIGHT - DIALOG_BOX_HEIGHT)

DIALOG_PORTRAIT_X_POSITION = DIALOG_BOX_X_POSITION - DIALOG_BOX_HEIGHT
DIALOG_PORTRAIT_Y_POSITION = DIALOG_BOX_Y_POSITION

DIALOG_BOX_COLOR = (19.2, 21.2, 22)

FONT_SIZE = math.ceil((WIDTH + HEIGHT) / (2000 / 18))

FONT_COLOR = "#fbff86"
HOVERING_FONT_COLOR = "#ffffff"

# sprites
sprite_data = {
    'player': {
        'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 2,
        'portrait': 1,
        "idle_animation": 1
    },
    "aiko": {
        "health": 75, 'energy': 55, 'attack': 4, 'magic': 1, 'speed': 2,
        "idle_animation": 0
    },
    "allein": {
        "health": 48, 'energy': 30, 'attack': 3, 'magic': 3, 'speed': 0.75,
        "idle_animation": 0
    },
    "boss": {
        "health": 84, 'energy': 64, 'attack': 6, 'magic': 0, 'speed': 2,
        "idle_animation": 0
    },
    "cooper": {
        "health": 75, 'energy': 59, 'attack': 5, 'magic': 2, 'speed': 2.1,
        "idle_animation": 0
    },
    "dustan": {
        "health": 100, 'energy': 60, 'attack': 9, 'magic': 0, 'speed': 2,
        "idle_animation": 0
    },
    "faster": {
        "health": 75, 'energy': 60, 'attack': 5, 'magic': 0, 'speed': 4,
        "idle_animation": 0
    },
    "gunvald": {
        "health": 84, 'energy': 60, 'attack': 10, 'magic': 5, 'speed': 1.75,
        "idle_animation": 0
    },
    "helma": {
        "health": 80, 'energy': 60, 'attack': 5, 'magic': 1, 'speed': 2,
        "idle_animation": 0
    },
    "john_doe": {
        "health": 65, 'energy': 50, 'attack': 6, 'magic': 0, 'speed': 2,
        "idle_animation": 0
    },
    "umbra": {
        "health": 96, 'energy': 90, 'attack': random.randint(7, 666),
        'magic': 5, 'speed': 3, "portrait": 1,
        "idle_animation": 1
    },
    "liam": {
        "health": 65, "energy": 64, "attack": random.randint(1, 5), "magic": 2,
        "speed": 2,
        "idle_animation": 0
    },
    "wassa": {
        "health": 52, "energy": random.randint(64, 96), "attack": 3,
        "magic": 2, "speed": 3, "portrait": 1,
        "idle_animation": 0
    },
    "items": {
        "portrait": 0, "idle_animation": 0
    }
}

default_max_stack = 64
item_data = {
    "coin": {
        "name": "Coin", "max_stack": default_max_stack, "lore":
        """This small piece of a copper and gold alloy is the official Pecunia
currency."""
    },

    "oak_log": {
        "name": "Oak Log", "max_stack": default_max_stack, "lore":
            'The trunk of a tree called "Oak".'
    },
    "spruce_log": {
        "name": "Spruce Log", "max_stack": default_max_stack, "lore":
        """Spruce = Christmas Tree"""
    },
    "birch_log": {
        "name": "Birch Log", "max_stack": default_max_stack, "lore":
        """This a white thing with black dots."""
    },

    "iron_ingot": {
        "name": "Iron Ingot", "max_stack": default_max_stack, "lore":
        """Iron is used in the manufacture of many objects,
it is most often drawn from the subsoil in the form of ore."""
    },
    "raw_iron": {
        "name": "Raw Iron", "max_stack": default_max_stack, "lore":
        """It's a useful pebble."""
    },

    "gold_ingot": {
        "name": "Gold Ingot", "max_stack": default_max_stack, "lore":
        """Gold is a precious metal.
It is rare and naturally has a golden yellow color."""
    },
    "raw_gold": {
        "name": "Raw Gold", "max_stack": default_max_stack, "lore":
        """That is a really precious pebble."""
    },

    "copper_ingot": {
        "name": "Copper Ingot", "max_stack": default_max_stack, "lore":
        """Golden red metal, very good conductor of electricity."""
    },
    "raw_copper": {
        "name": "Raw Copper", "max_stack": default_max_stack, "lore":
        """To Minecraft players:
Copper is far more useful than you think."""
    },

    "dark_steel_ingot": {
        "name": "Dark Steel Ingot", "max_stack": default_max_stack, "lore":
        """This weird gloomy ingot is really hard..."""
    },
    "raw_dark_steel": {
        "name": "Raw Sark Steel", "max_stack": default_max_stack, "lore":
        """It is not a regular pebble at all."""
    },

    "potato": {
        "name": "Potato", "max_stack": default_max_stack, "lore":
        """Solanum tuberosum bonum est."""
    },
    "poisonous_potato": {
        "name": "Jacket Potato", "max_stack": default_max_stack, "lore":
        "THIS IS not DELICIOUS."
    },
    "jacket_potato": {
        "name": "Jacket Potato", "max_stack": default_max_stack, "lore":
        "THIS IS DELICIOUS."
    },

    "apple": {
        "name": "Apple", "max_stack": default_max_stack, "lore":
        "That is a fruit."
    },

    "blueberry": {
        "name": "Blue Berry", "max_stack": default_max_stack, "lore":
        "Blue and sweet."
    },
    "purpleberry": {
        "name": "Purple Berry", "max_stack": default_max_stack, "lore":
        """Açai Berries ? Black Currants ? Blackberries ? Elderberries ?
Gooseberries ? Huckleberries ? Jamun Berries ? Luma Berries ? Maqui Berries ?
Mulberries ? Olallieberries ? Riberries ? Salal Berries ? Serviceberries ?
Sherbet Berries ?"""
    },
    "redberry": {
        "name": "Red Berry", "max_stack": default_max_stack, "lore":
        "Blue Berry but it's red."
    },

    "bread": {
        "name": "Bread", "max_stack": default_max_stack, "lore":
        "Bread is Pain."
    },

    "carrot": {
        "name": "Carrot", "max_stack": default_max_stack, "lore":
        "Bread is Pain."
    },

    "chicken": {
        "name": "Raw Chicken", "max_stack": default_max_stack, "lore":
        "Don not eat raw meat."
    },
    "cooked_chicken": {
        "name": "Raw Chicken", "max_stack": default_max_stack, "lore":
        "Cooked chicken is more nutritious and tastes better than raw chicken."
    },

    "beef": {
        "name": "Raw Beef", "max_stack": default_max_stack, "lore":
        "Cow cruelly eliminated in an atrocious way."
    },
    "cooked_beef": {
        "name": "Steak", "max_stack": default_max_stack, "lore":
        "Cow cooked mercilessly in fiery flames."
    },

    "mutton": {
        "name": "Raw Mutton", "max_stack": default_max_stack, "lore":
        "Mutton = Dead Sheep"
    },
    "cooked_mutton": {
        "name": "Cooked Mutton", "max_stack": default_max_stack, "lore":
        "A kind of food from a sheep."
    },

    "fish": {
        "name": "Fish", "max_stack": default_max_stack, "lore":
        "Aquatic steak."
    },
}
