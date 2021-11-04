import pygame

from text import Text

class Toolbar():
    def __init__(self, width, height): #And other customisation options
        self.image = pygame.Surface((width, height))
        self.image.fill("#ceaca3")
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        # self.__fileButton = Button(font='fonts/OdibeeSans-Regular.ttf', fontSize=20, content='File', color='#FFFFFF')
        # self.__aboutButton = Button(font='fonts/OdibeeSans-Regular.ttf', fontSize=20, content='About', color='#FFFFFF')
        # self.__helpButton = Button(font='fonts/OdibeeSans-Regular.ttf', fontSize=20, content='Help', color='#FFFFFF')
        self.__fileHover = False 
        self.__aboutHover = False
        self.__helpHover = False

    def toolBarHover(self, pos):
        if self.__fileButton_rect.collidepoint(pos):
            self.__fileHover = True
        elif self.__aboutButton_rect.collidepoint(pos):
            self.__aboutHover = True
        elif self.__helpButton_rect.collidepoint(pos):
            self.__helpHover = True
        else:
            self.__fileHover = False 
            self.__aboutHover = False
            self.__helpHover = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        self.__fileButton = Text(font='../fonts/OdibeeSans-Regular.ttf', fontSize=20, content='File', color=self.__getColor(self.__fileHover))
        self.__aboutButton = Text(font='../fonts/OdibeeSans-Regular.ttf', fontSize=20, content='About', color=self.__getColor(self.__aboutHover))
        self.__helpButton = Text(font='../fonts/OdibeeSans-Regular.ttf', fontSize=20, content='Help', color=self.__getColor(self.__helpHover))

        self.__fileButton_rect = self.__fileButton.text.get_rect(midleft=(10, 12))
        screen.blit(self.__fileButton.text, self.__fileButton_rect)

        self.__aboutButton_rect = self.__aboutButton.text.get_rect(midleft=(50, 12))
        screen.blit(self.__aboutButton.text, self.__aboutButton_rect)
        
        self.__helpButton_rect = self.__helpButton.text.get_rect(midleft=(100, 12))
        screen.blit(self.__helpButton.text, self.__helpButton_rect)

    def __getColor(self, hovered):
        if hovered:
            return (230, 230, 230)
        else:
            return (250, 250, 250)