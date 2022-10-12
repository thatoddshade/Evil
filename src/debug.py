import pygame
import settings

pygame.init()


def debug(surf, info, x=10, y=10):
    display_surf = surf

    # get the font
    font = settings.get_font(settings.FONT_SIZE)
    font.bold = True

    # create some text
    debug_surf = font.render(str(info), False, (255, 255, 255))

    # create a rect with a pos
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    # blit all of that
    pygame.draw.rect(display_surf, '#2e222f', debug_rect, 0, 4)
    display_surf.blit(
        debug_surf,
        debug_rect
    )
