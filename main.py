# general setup
import pygame
import support
import settings
import code

clock = pygame.time.Clock()
pygame.init()  # initiate pygame

# import settings
options = support.import_json("options.txt")
for option in options:
    if "key_" in option:
        options[option] = eval(options[option])  # convert key values from string to int

window_size = (options["window_width"], options["window_height"])
screen = pygame.display.set_mode(window_size)  # initiate the window

pygame.display.set_caption("Evil")  # set the window title

display_size = (
    options["display_width"],
    options["display_height"],
)
display = pygame.Surface(
    display_size
)  # used as the surface for rendering, which is scaled

# replace default mouse pointer by a custom one
cursor_img = pygame.image.load("data/images/cursor.png").convert_alpha()
cursor = pygame.cursors.Cursor((0, 0), cursor_img)
pygame.mouse.set_cursor(cursor)

running = True
while running:  # game loop
    display.fill(settings.BACKGROUND_COLOR)  # clean screen

    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False

    # display stuff
    pygame.draw.circle(display, "#000000", (24, 16), 16)
    code.text.font.small_font.render(display, "hello, world", (32, 48))

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
