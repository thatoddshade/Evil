# general setup
import pygame
import src

clock = pygame.time.Clock()
pygame.init()  # initiate pygame

# import settings
from src.options.dictionary import options

# make a window
window_size = (options["window_width"], options["window_height"])
screen = pygame.display.set_mode(window_size, 0, 32)  # initiate the window

# make a surface used for rendering
display_size = (
    options["display_width"],
    options["display_height"],
)
display = pygame.Surface(display_size)

pygame.display.set_caption("Evil")  # set the window title

# replace default mouse pointer by a custom one
cursor_img = pygame.image.load("data/images/cursor.png").convert_alpha()
cursor = pygame.cursors.Cursor((0, 0), cursor_img)
pygame.mouse.set_cursor(cursor)


running = True
while running:  # game loop
    display.fill(options["background_color"])  # fill screen

    for event in pygame.event.get():  # event loop
        if event.type is pygame.QUIT:  # check for window quit
            running = False  # stop game loop

    # display stuff
    pygame.draw.circle(display, "#c7dcd0", (16, 16), 16)  # show a circle

    src.text.font.large_font.render(display, "ABCD", (32, 32))
    src.text.font.small_font.render(display, "ABCD", (48, 48))
    pygame.draw.rect(display, "#ffffff", (64, 64, 1, 1))

    screen.blit(pygame.transform.scale(display, window_size), (0, 0))
    pygame.display.update()  # update screen
    clock.tick(60)

pygame.quit()  # stop pygame
