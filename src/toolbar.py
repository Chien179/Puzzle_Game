import pygame
from text import Text

class Toolbar:
    def __init__(self, font, width, height): #And other customisation options
        self.image = pygame.Surface((width, height))
        self.image.fill("#CEACA3")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.fileButton = Text(font=font, fontSize=20, content='File', color='#FFFFFF')
        self.aboutButton = Text(font=font, fontSize=20, content='About', color='#FFFFFF')
        self.aboutButton_rect = self.aboutButton.text.get_rect(midleft=(50, 12))
        self.fileButton_rect = self.fileButton.text.get_rect(midleft=(10, 12))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.fileButton.text, self.fileButton_rect)
        screen.blit(self.aboutButton.text, self.aboutButton_rect)