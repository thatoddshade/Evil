

class Button:
    def __init__(
        self, image, pos, text_input, font, base_color, hovering_color
    ):
        self.image = image
        self.position = pos
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(
            self.text_input,
            True,
            self.base_color
        )
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        x_alignment = position[0] in range(self.rect.left, self.rect.right)
        y_alignment = position[1] in range(self.rect.top, self.rect.bottom)
        if x_alignment and y_alignment:
            return True
        return False

    def changeColor(self, position):
        x_alignment = position[0] in range(self.rect.left, self.rect.right)
        y_alignment = position[1] in range(self.rect.top, self.rect.bottom)
        if x_alignment and y_alignment:
            self.text = self.font.render(
                self.text_input, True, self.hovering_color
            )
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color
            )

    def main_menu(self):
        print("menu open")

        mouse_pos = pygame.mouse.get_pos()

        menu_rect = pygame.Rect(
            WIDTH / 6, HEIGHT / 4, WIDTH / 1.5, HEIGHT / 1.5
        )
        menu_surf = pygame.Surface(
            pygame.Rect(menu_rect).size, pygame.SRCALPHA
        )
        pygame.draw.rect(
            menu_surf, (
                DIALOG_BOX_COLOR[0], DIALOG_BOX_COLOR[1], DIALOG_BOX_COLOR[2],
                128
            ), menu_surf.get_rect(), 0, 15)
        self.screen.blit(menu_surf, menu_rect)

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#f79617")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            image=None, pos=(640, 250), text_input="PLAY",
            font=get_font(75), base_color=FONT_COLOR,
            hovering_color=HOVERING_FONT_COLOR
        )

        OPTIONS_BUTTON = Button(
            image=None, pos=(640, 400),
            text_input="OPTIONS", font=get_font(75),
            base_color=FONT_COLOR, hovering_color=HOVERING_FONT_COLOR
        )

        QUIT_BUTTON = Button(
            image=None, pos=(640, 550),
            text_input="QUIT", font=get_font(75), base_color=FONT_COLOR,
            hovering_color=HOVERING_FONT_COLOR
        )

        self.screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(mouse_pos)
            button.update(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(mouse_pos):
                    self.open_menu = not self.open_menu
                if OPTIONS_BUTTON.checkForInput(mouse_pos):
                    print("options")
                if QUIT_BUTTON.checkForInput(mouse_pos):
                    pygame.quit()
                    sys.exit()
