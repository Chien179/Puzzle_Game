import pygame
import numpy
from puzzle import Puzzle
from text import Text
from toolbar import Toolbar
from messagebox import Messagebox

TEXT_FONT = '../fonts/OdibeeSans-Regular.ttf'
BACKGROUND_COLOR = '#A2C6F0'
GAME_ICON = '../icons/puzzle.png'

class Display:
    def __init__(self, size, width, height, imgWidth, imgHeight):
        pygame.init()
        pygame.display.set_caption('Puzzle')
        gameIcon = pygame.image.load(GAME_ICON)
        pygame.display.set_icon(gameIcon)

        self.width = width
        self.height = height
        self.imgWidth = imgWidth
        self.imgHeight = imgHeight
        self.size = size

        self.__screen = pygame.display.set_mode((self.width, self.height))

        self.image = '../images/paris.png'
        end = [i for i in range(1, self.size ** 2 + 1)]
        self.goal = numpy.reshape(end, (self.size, self.size)).tolist()
        self.puzzle = Puzzle(self.image, self.imgWidth, self.imgHeight, self.size, self.goal)

        self.__title_text = Text(font=TEXT_FONT, fontSize=40, content='PUZZLE', color='#FFFFFF')
        self.__music_text = Text(font=TEXT_FONT, fontSize=30, content='Pause', color='#FFFFFF')
        self.__volumeUp_text = Text(font='Times New Roman', fontSize=35, content='+', color='#FFFFFF',
                                    isBold=False, isSys=True)
        self.__volumeDown_text = Text(font='Times New Roman', fontSize=35, content='-', color='#FFFFFF',
                                      isBold=False, isSys=True)
        self.__shuffle_text = Text(font=TEXT_FONT, fontSize=40, content='Shuffle', color='#FFFFFF')
        self.__hint_text = Text(font=TEXT_FONT, fontSize=40, content='Hint', color='#FFFFFF')
        self.__solve_text = Text(font=TEXT_FONT, fontSize=40, content='Solve', color='#FFFFFF')
        self.__puzzleRect = pygame.draw.rect(self.__screen, '#CEACA3',
                                             pygame.Rect(19, 99, self.imgWidth + 1, self.imgHeight + 1), 1)

        self.toolBar = Toolbar(TEXT_FONT, 800, 25)

        self.mess = Messagebox(self.__screen)

        self.__musicImg = pygame.image.load('../icons/pause.png')
        self.__musicImg = pygame.transform.scale(self.__musicImg, (24, 24))

        self.checkWin = False
        self.start = False
        self.checkHint = False
        self.musicPlaying = True

        self.__createRect()

    def musicIcon(self, icon = '../icons/pause.png'):
        self.__musicImg = pygame.image.load(icon)
        self.__musicImg = pygame.transform.scale(self.__musicImg, (24, 24))

    def __createRect(self):
        self.musicImg_rect = self.__musicImg.get_rect(midleft=(51, 60))
        self.__title_text_rect = self.__title_text.text.get_rect(center=(self.width / 2, 60))
        self.volumeUp_text_rect = self.__volumeUp_text.text.get_rect(midleft=(85, 60))
        self.volumeDown_text_rect = self.__volumeDown_text.text.get_rect(midleft=(30, 57))
        self.shuffle_text_rect = self.__shuffle_text.text.get_rect(midleft=(600, 350))
        self.hint_text_rect = self.__hint_text.text.get_rect(midleft=(620, 410))
        self.solve_text_rect = self.__solve_text.text.get_rect(midleft=(612, 470))

        self.__rect_list = [self.__hint_text,
                            self.__shuffle_text,
                            self.__solve_text,
                            self.__volumeDown_text,
                            self.__volumeUp_text,
                            self.toolBar.fileButton,
                            self.toolBar.aboutButton,
                            self.__music_text]

    def draw(self):
        # white screen
        surface = self.__screen
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.puzzle.image, (20, 100))
        image = self.puzzle.displayImage()
        showImg = pygame.transform.scale(image,(200,200))
        surface.blit(showImg, (550,100))

    def drawText(self):
        if self.checkWin:
            self.mess.create()
        self.toolBar.draw(self.__screen)
        surface = self.__screen
        surface.blit(self.__title_text.text, self.__title_text_rect)
        surface.blit(self.__hint_text.text, self.hint_text_rect)
        surface.blit(self.__volumeUp_text.text, self.volumeUp_text_rect)
        surface.blit(self.__shuffle_text.text, self.shuffle_text_rect)
        surface.blit(self.__volumeDown_text.text, self.volumeDown_text_rect)
        surface.blit(self.__solve_text.text, self.solve_text_rect)
        surface.blit(self.__musicImg, self.musicImg_rect)

    def hoverButton(self, mousePos):
        if not self.checkWin:
            if self.toolBar.fileButton_rect.collidepoint(mousePos) and not self.start:
                self.__buttonHover(self.toolBar.fileButton)
            elif self.toolBar.aboutButton_rect.collidepoint(mousePos):
                self.__buttonHover(self.toolBar.aboutButton)
            elif self.musicImg_rect.collidepoint(mousePos) and self.musicPlaying:
                pass
            elif self.musicImg_rect.collidepoint(mousePos) and not self.musicPlaying:
                pass
            elif self.volumeUp_text_rect.collidepoint(mousePos):
                self.__buttonHover(self.__volumeUp_text)
            elif self.volumeDown_text_rect.collidepoint(mousePos):
                self.__buttonHover(self.__volumeDown_text)
            elif self.shuffle_text_rect.collidepoint(mousePos):
                self.__buttonHover(self.__shuffle_text)
            elif self.solve_text_rect.collidepoint(mousePos):
                self.__buttonHover(self.__solve_text)
            elif self.hint_text_rect.collidepoint(mousePos):
                self.__buttonHover(self.__hint_text)
            elif self.__puzzleRect.collidepoint(mousePos) and self.start:
                pygame.mouse.set_cursor(pygame.cursors.diamond)
            else:
                for text in self.__rect_list:
                    self.__buttonLeft(text)
        else:
            if self.mess.playAgain_rect.collidepoint(mousePos):
                self.__buttonHover(self.mess.playAgain)
            elif self.mess.quit_rect.collidepoint(mousePos):
                self.__buttonHover(self.mess.quit)
            else:
                self.__buttonLeft(self.mess.playAgain)
                self.__buttonLeft(self.mess.quit)

    def setPuzzle(self):
        self.drawText()
        imgPieceWidth = self.imgWidth / self.size
        x, y = 20, 100
        for i in range(0, self.size):
            imgTemp = []
            for j in range(0, self.size):
                imgTemp.append(self.puzzle.imgPieces[i][j].get_rect(left=x, top=y)) # create rectangle to move image pieces
                self.__drawRect(self.puzzle.imgPieces[i][j], imgPieceWidth) # draw rectangle around image piece
                self.__screen.blit(self.puzzle.imgPieces[i][j], imgTemp[j])
                x += imgPieceWidth
                if j == self.size - 1:
                    x = 20
                    y += imgPieceWidth
            self.puzzle.imgRect.append(imgTemp)

    def drawHint(self, nextNode):
        imgPieceWidth = self.imgWidth / self.size
        x, y = 20, 100
        for i in range(0, self.size):
            imgTemp = []
            for j in range(0, self.size):
                imgTemp.append(self.puzzle.imgPieces[i][j].get_rect(left=x, top=y))
                if i == nextNode[0] and j == nextNode[1]:
                    # draw rectangle around image piece of next step
                    self.__drawRect(self.puzzle.imgPieces[i][j], imgPieceWidth, (220, 20, 60))
                self.__screen.blit(self.puzzle.imgPieces[i][j], imgTemp[j])
                x += imgPieceWidth
                if j == self.size - 1:
                    x = 20
                    y += imgPieceWidth

    def hoverPuzzleArea(self, mousePos):
        self.__screen.blit(self.puzzle.image, (20, 100))
        imgPieceWidth = self.imgWidth / self.size
        x, y = 20, 100
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.puzzle.imgRect[i][j].collidepoint(mousePos):
                    self.checkHint = False
                    self.__drawRect(self.puzzle.imgPieces[i][j], imgPieceWidth, (250, 250, 250))
                elif not self.checkHint:
                    self.__drawRect(self.puzzle.imgPieces[i][j], imgPieceWidth)
                self.__screen.blit(self.puzzle.imgPieces[i][j], self.puzzle.imgRect[i][j])
                x += imgPieceWidth
                if j == self.size - 1:
                    x = 20
                    y += imgPieceWidth

    @staticmethod
    def __drawRect(image, imgPieceWidth, color=(0, 0, 0)):
        pygame.draw.rect(image, color, pygame.Rect(0, 0, imgPieceWidth, imgPieceWidth), 1)

    @staticmethod
    def __buttonLeft(text):
        text.set_color_hovered((250, 250, 250))
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        text.update()

    @staticmethod
    def __buttonHover(text):
        text.set_color_hovered((230, 230, 230))
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        text.update()