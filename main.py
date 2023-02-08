# general setup
import pygame, pytmx, pyscroll, sys
import src

clock = pygame.time.Clock()
pygame.init()  # initiate pygame

# import settings
from src.options.dictionary import options

surf_size = (options["window_width"], options["window_height"])
window_size = (options["window_width"], options["window_height"])
display_size = (
    options["display_width"],
    options["display_height"],
)
monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

# make a window
screen = pygame.display.set_mode(surf_size, pygame.RESIZABLE)
pygame.display.set_caption("Evil")  # set the window title

# make a surface used for rendering
display = pygame.Surface(display_size)

fullscreen = False

# set icon
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)

# replace default mouse pointer by a custom one
cursor_img = pygame.image.load("data/images/cursor.png").convert_alpha()
cursor_img = pygame.transform.scale(cursor_img, (64, 64))
cursor = pygame.cursors.Cursor((0, 0), pygame.transform.scale(cursor_img, (32, 32)))
pygame.mouse.set_cursor(cursor)

# load map
tmx_data = pytmx.util_pygame.load_pygame("data/map/village.tmx")
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, display_size)
map_layer.zoom = 2

group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)


small_font = src.text.font.Font("data/images/font/small_font.png")
large_font = src.text.font.Font("data/images/font/large_font.png")

# player = src.entity.Player("data/images/sprite/player/moving.png", (100, 100, group))

running = True
while running:  # game loop
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():  # event loop
        if event.type is pygame.QUIT:  # check for window quit
            running = False  # stop game loop

        if event.type == pygame.KEYDOWN:
            print(event.key)
            if event.key == pygame.K_ESCAPE:
                running = False  # stop game loop

            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        if event.type is pygame.VIDEORESIZE:
            if not fullscreen:
                window_size = (event.w, event.h)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    # display stuff
    display.fill(options["background_color"])  # fill screen

    group.draw(display)
    group.center(mouse_pos)

    # large_font.render(display, "ABCD", (32, 32))
    # small_font.render(display, "ABCD", (48, 48))
    # pygame.draw.rect(display, "#ffffff", (64, 64, 1, 1))

    display_size = (
        screen.get_height() * 2,
        screen.get_height(),
    )
    display_pos = ((screen.get_width() - (screen.get_height() * 2)) / 2, 0)

    screen.blit(
        pygame.transform.scale(display, display_size),
        display_pos,
    )
    pygame.display.update()  # update screen
    clock.tick(60)

pygame.quit()  # stop pygame
sys.exit()  # exit
