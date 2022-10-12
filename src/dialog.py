import pygame
from pygame import mixer
from settings import *

class DialogBox:

    DIALOG_BOX_X_POSITION = DIALOG_BOX_X_POSITION
    DIALOG_BOX_Y_POSITION = DIALOG_BOX_Y_POSITION

    def __init__(self, player):
        self.player = player
        self.box = pygame.Rect(self.DIALOG_BOX_X_POSITION, self.DIALOG_BOX_Y_POSITION, DIALOG_BOX_WIDTH, DIALOG_BOX_HEIGHT)
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("../fonts/default_font.ttf", FONT_SIZE)
        self.reading = False
        self.npc_name = ""
        self.has_a_portrait = False

    def execute(self, npc, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.player.speed = 0
            self.reading = True
            self.text_index = 0
            self.texts = dialog
        self.npc_name = npc.name
        self.has_a_portrait = npc.has_a_portrait


    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            # display the portrait if the character has one
            if self.has_a_portrait:
                pygame.draw.rect(screen, DIALOG_BOX_COLOR, pygame.Rect(DIALOG_PORTRAIT_X_POSITION, DIALOG_PORTRAIT_Y_POSITION, DIALOG_BOX_HEIGHT, DIALOG_BOX_HEIGHT), 0, 15)
                screen.blit(pygame.transform.scale(pygame.image.load(f'..\images\sprites\{self.npc_name}\portrait.png'), (DIALOG_BOX_HEIGHT * 0.96, DIALOG_BOX_HEIGHT * 0.96)), (self.DIALOG_BOX_X_POSITION - DIALOG_BOX_HEIGHT * 0.96, HEIGHT - DIALOG_BOX_HEIGHT * 0.96))

            # display the dialog box
            pygame.draw.rect(screen, DIALOG_BOX_COLOR, self.box, 0, 15)

            # display the previous text
            if self.text_index > 0:
                previous_text = self.font.render(self.texts[self.text_index - 1], False, (255, 255, 255))
                screen.blit(previous_text, (self.DIALOG_BOX_X_POSITION + (DIALOG_BOX_HEIGHT / 2), self.DIALOG_BOX_Y_POSITION + (DIALOG_BOX_HEIGHT / 3)))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (255, 255, 255))
            screen.blit(text, (self.DIALOG_BOX_X_POSITION + (DIALOG_BOX_HEIGHT / 2), self.DIALOG_BOX_Y_POSITION + (DIALOG_BOX_HEIGHT / 2)))



    def next_text(self):
        self.text_index +=1
        self.letter_index = 0


        if self.text_index >= len(self.texts):
            # close dialog
            self.reading = False
            self.player.speed = self.player.stats["speed"]
