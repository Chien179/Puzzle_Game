import pygame

class Button:
    def __init__(self, font, fontSize, content, color, isBold = False, isSys = False):
        self.__font = font
        self.__fontSize = fontSize
        self.__content = content
        self.__color = color
        self.__isBold = isBold
        self.__isSys = isSys
        if self.__isSys:
            self.text = self.__create_Sysfont()
        else:
            self.text = self.__create_Font()

    def __create_Sysfont(self):
        f = pygame.font.SysFont(self.__font, self.__fontSize, self.__isBold, False)
        text = f.render(self.__content, True, self.__color)
        return text

    def __create_Font(self):
        f = pygame.font.Font(self.__font, self.__fontSize)
        text = f.render(self.__content, True, self.__color)

        return text

    def set_color_hovered(self, color):
        self.__color = color #hovered

    def set_color_left(self, color):
        self.__color = color #mouse leave

    def update(self):
        if self.__isSys:
            self.text = self.__create_Sysfont()
        else:
            self.text = self.__create_Font()