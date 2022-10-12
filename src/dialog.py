import pygame
from pygame import mixer

class DialogBox:

    X_POSITION = 350
    Y_POSITION = 650

    def __init__(self, player):
        self.player = player
        self.box = pygame.image.load('..\dialogs\dialog_box.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.texts = []
        self.text_index = 0
        self.letter_index = 0
        self.font = pygame.font.Font("..\dialogs\dialog_font.ttf", 18)
        self.reading = False

    def execute(self, dialog=[]):
        if self.reading:
            self.next_text()
        else:
            self.player.speed = 0
            self.reading = True
            self.text_index = 0
            self.texts = dialog

    def render(self, screen):
        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (255, 255, 255))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 42))



    def next_text(self):
        self.text_index +=1
        self.letter_index = 0


        if self.text_index >= len(self.texts):
            # close dialog
            self.reading = False
            self.player.speed = self.player.old_speed
