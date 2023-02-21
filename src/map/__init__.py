import pygame, pytmx, pyscroll

def load_map(path, display_size):
    tmx_data = pytmx.util_pygame.load_pygame(path)
    map_data = pyscroll.data.TiledMapData(tmx_data)
    return map_data
