import json, pygame
import time


# data manipulation
def import_json(path):
    with open(path) as json_file:
        return json.load(json_file)


# graphic manipulation
def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_r = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_r)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()


previous_time = time.time()
def update_delta_time():
    global delta_time, previous_time
    delta_time = time.time() - previous_time
    delta_time *= 60
    previous_time = time.time()

update_delta_time()