# general setup
import pygame, pytmx, pyscroll, sys, math, src, pygame_shaders

pygame.init()

# import settings
from src.options.dictionary import option_dict as options

# initialize game controller
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

surf_size = (options["window_width"], options["window_height"])
window_size = (options["window_width"], options["window_height"])
display_size = (
    options["display_width"],
    options["display_height"],
)
monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

# setup a window and a rendering surface
if options.get("fullscreen", False):
    screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN | pygame.OPENGL)
else:
    screen = pygame.display.set_mode(surf_size, pygame.RESIZABLE | pygame.OPENGL)

display = pygame.Surface(display_size)
display.set_colorkey((0, 0, 0))

screen_shader = pygame_shaders.Shader(
    window_size,
    window_size,
    (0, 0),
    "shaders/vertex.glsl",
    "shaders/fragment.glsl",
    screen,
)

clock = pygame.time.Clock()

pygame.display.set_caption("Evil")  # set the window title

# set icon
icon = pygame.image.load("data/images/icon.png")
pygame.display.set_icon(icon)

# replace default mouse pointer by a custom one
cursor_img = pygame.image.load("data/images/cursor.png").convert_alpha()
cursor_img = pygame.transform.scale(cursor_img, (64, 64))
cursor = pygame.cursors.Cursor((0, 0), pygame.transform.scale(cursor_img, (32, 32)))
pygame.mouse.set_cursor(cursor)

# load map
map_data = src.map.load_map("data/map/village.tmx", display_size)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data, display_size)
map_layer.zoom = 2

group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)

# load fonts
# small_font = src.text.font.Font("data/images/font/small_font.png")
# large_font = src.text.font.Font("data/images/font/large_font.png")

# load player
player = src.entity.Player((100, 100), group)
# tmp :
entity = src.entity.Entity((100, 100), "data/images/sprite/player/moving.png", group)

running = True
while running:  # game loop
    src.utils.update_delta_time()
    mouse_pos = pygame.mouse.get_pos()

    # update
    for event in pygame.event.get():  # event loop
        if event.type is pygame.QUIT:  # check for window quit
            running = False  # stop game loop

        if event.type == pygame.JOYAXISMOTION:
            if event.axis < 2:
                player.direction[event.axis] = event.value
        if event.type == pygame.JOYDEVICEADDED:
            joysticks = [
                pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
            ]
        if event.type == pygame.JOYDEVICEREMOVED:
            joysticks = [
                pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())
            ]

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # stop game loop

            # if event.key == pygame.K_F11:
            #     fullscreen = not fullscreen
            # if fullscreen:
            #     screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            # else:
            #     screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        # if event.type is pygame.VIDEORESIZE:
        #     if not fullscreen:
        #         window_size = (event.w, event.h)
        #         screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    player.handle_input(src.utils.delta_time)

    # display stuff
    pygame_shaders.clear((options["background_color"]))
    screen.fill(options["background_color"])

    group.draw(display)
    # group.center(mouse_pos)
    group.center(player.rect)

    # large_font.render(display, "ABCD", (32, 32))
    # small_font.render(display, "ABCD", (48, 48))
    # pygame.draw.rect(display, "#ffffff", (64, 64, 1, 1))

    display_size = (
        screen.get_height() * (options["window_width"] / options["window_height"]),
        screen.get_height(),
    )
    display_pos = ((screen.get_width() - display_size[0]) / 2, 0)

    screen.blit(
        pygame.transform.scale(display, display_size),
        display_pos,
    )

    # show fps
    # sys_font = pygame.font.Font(None, 32)
    # debug_surf = sys_font.render(
    #     str(math.ceil(clock.get_fps())) + " FPS", False, (255, 255, 255)
    # )
    # debug_rect = debug_surf.get_rect(topleft=(10, 10))
    # pygame.draw.rect(screen, "#2e222f", debug_rect, 0, 4)
    # screen.blit(debug_surf, debug_rect)
    pygame.display.set_caption(
        "Evil" + " - " + str(math.ceil(clock.get_fps())) + " FPS"
    )

    screen_shader.render(screen)

    pygame.display.flip()  # update screen
    clock.tick()

pygame.quit()  # stop pygame
sys.exit()  # exit
