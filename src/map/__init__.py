# import pygame, sys

# from pytmx.util_pygame import load_pygame

# from .. import tile

# pygame.init()

# tile_size = 16


# def load_map(map_path, groups):
#     tmx_data = load_pygame(map_path)
#     for layer in tmx_data.visible_layers:
#         if hasattr(layer, "data"):
#             for x, y, surf in layer.tiles():
#                 pos = x * tile_size, y * tile_size
#                 tile.Tile(pos=pos, surf=surf, groups=groups)
#             for obj in tmx_data.objects:
#                 pos = obj.x, obj.y
#                 if obj.image:
#                     tile.Tile(pos=pos, surf=obj.image, groups=groups)
#     return tmx_data


import pytmx, pyscroll, pygame

# pygame.init()

# tmx_data = pytmx.util_pygame.load_pygame("data/map/village.tmx")


# def get_data():
#     map_data = pyscroll.data.TiledMap(tmx_data)
#     return map_data


# def get_layer(map_data, size):
#     map_layer = pyscroll.orthographic.BufferedRenderer(map_data, size)
#     return map_layer
