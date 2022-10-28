import pygame
import math
import settings


class DialogBox:
    def __init__(self, player):
        self.player = player
        self.box = pygame.image.load("../images/gui/dialog_box.png")
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = settings.get_font(settings.FONT_SIZE)
        self.reading = False

    def write(self, surf, x, y, text, color=(255, 255, 255)):
        text = self.font.render(text, False, color)
        surf.blit(text, (x, y))

    def execute(self, npc, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.player.speed = 0
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen):
        if self.reading:
            self.letter_index += math.ceil(1 * settings.delta_time)
            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(
                pygame.transform.scale(
                    self.box,
                    (
                        settings.DIALOG_BOX_WIDTH, settings.DIALOG_BOX_HEIGHT
                    ),
                ),
                (
                    settings.DIALOG_BOX_X_POSITION * 0.75,
                    settings.DIALOG_BOX_Y_POSITION
                )
            )
            # display the portrait, if the character has one
            if "portrait" in settings.sprite_data[self.texts[self.text_index][0]]:
                if settings.sprite_data[self.texts[self.text_index][0]]["portrait"]:
                    screen.blit(
                        pygame.transform.scale(
                            pygame.image.load(
                                f'../images/sprites/{self.texts[self.text_index][0]}/portrait.png'
                            ),
                            (
                                settings.DIALOG_BOX_HEIGHT * 0.96,
                                settings.DIALOG_BOX_HEIGHT * 0.96
                            )
                        ),
                        (
                            settings.DIALOG_BOX_X_POSITION -
                            settings.DIALOG_BOX_HEIGHT * 0.96,
                            settings.HEIGHT - settings.DIALOG_BOX_HEIGHT * 0.96
                        )
                    )

            # display the previous text
            if self.text_index > 0:
                self.write(
                    screen,
                    settings.DIALOG_BOX_X_POSITION + (
                        settings.DIALOG_BOX_HEIGHT / 2),
                    settings.DIALOG_BOX_Y_POSITION + (
                        settings.DIALOG_BOX_HEIGHT / 3),
                    self.texts[self.text_index - 1][1]
                )

            # display npc name
            self.write(
                screen,
                settings.DIALOG_BOX_X_POSITION + (
                    settings.DIALOG_BOX_HEIGHT / 4),
                settings.DIALOG_BOX_Y_POSITION,
                self.texts[self.text_index][0].replace("_", " ").upper() + " :")

            # display the current text
            self.write(
                screen,
                settings.DIALOG_BOX_X_POSITION + (
                    settings.DIALOG_BOX_HEIGHT / 2),
                settings.DIALOG_BOX_Y_POSITION + (
                    settings.DIALOG_BOX_HEIGHT / 2),
                self.texts[self.text_index][1][0:self.letter_index]
            )

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            # close dialog
            self.reading = False
            self.player.speed = self.player.stats["speed"]
