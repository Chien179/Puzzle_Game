import pygame
from text import Text

TEXT_FONT = '../fonts/OdibeeSans-Regular.ttf'

class Messagebox:
    def __init__(self, surface):
        self.__surface = surface
        self.__title = Text(font=TEXT_FONT, fontSize=40, content='CONGRATULATIONS!!!', color='#FFFFFF')
        self.__win = Text(font=TEXT_FONT, fontSize=40, content='YOU WIN', color='#FFFFFF')
        self.playAgain = Text(font=TEXT_FONT, fontSize=30, content='Play Again', color='#FFFFFF')
        self.quit = Text(font=TEXT_FONT, fontSize=30, content='Quit', color='#FFFFFF')
        self.title_rect = self.__title.text.get_rect(midleft=(220, 240))
        self.win_rect = self.__win.text.get_rect(midleft=(300, 280))
        self.playAgain_rect = self.playAgain.text.get_rect(midleft=(280, 330))
        self.quit_rect = self.quit.text.get_rect(midleft=(420, 330))

    def create(self):
        #display messagebox
        pygame.draw.rect(self.__surface, '#CEACA3', pygame.Rect(200, 180, 340, 200))
        self.__surface.blit(self.__title.text, self.title_rect)
        self.__surface.blit(self.__win.text, self.win_rect)
        self.__surface.blit(self.playAgain.text, self.playAgain_rect)
        self.__surface.blit(self.quit.text, self.quit_rect)
