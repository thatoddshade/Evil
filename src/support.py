import json, pygame


# data manipulation
def import_json(path):
    with open(path) as json_file:
        dict = json.load(json_file)
    return dict


# graphic manipulation
def clip(surf, x, y, x_size, y_size):
    handle_surf = surf.copy()
    clip_r = pygame.Rect(x, y, x_size, y_size)
    handle_surf.set_clip(clip_r)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()
