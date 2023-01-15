from .. import support
import pygame

# import settings
options = support.import_json("options.txt")
for option in options:
    if "key_" in option:
        options[option] = eval(options[option])  # convert key values from string to int
