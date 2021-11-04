import pygame
import numpy
from pygame.time import delay
from puzzle import Puzzle
from text import Text
from algorithm import AStar
from messagebox import Messagebox

TEXT_FONT = 'fonts/OdibeeSans-Regular.ttf'
BACKGROUND_COLOR = '#A2C6F0'

class Game:

    def __init__(self, width, height, imgWidth, imgHeight, size):
        pygame.init()
        self.__width, self.__height = width, height
        self.__imgWidth, self.__imgHeight = imgWidth, imgHeight
        self.__size = size
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        end = [i for i in range(1, self.__size ** 2 + 1)]
        self.__goal = numpy.reshape(end, (self.__size, self.__size)).tolist()
        self.__puzzle = Puzzle('images/1.jpg', self.__imgWidth, self.__imgHeight, self.__size, self.__goal)
        self.__start = False
        self.__checkHint = False
        self.__title_text = Text(font=TEXT_FONT, fontSize=40, content='PUZZLE', color='#FFFFFF')
        self.__music_text = Text(font=TEXT_FONT, fontSize=30, content='Pause', color='#FFFFFF')
        self.__volumeup_text = Text(font='Times New Roman', fontSize=35, content='+', color='#FFFFFF',
                                      isBold=False, isSys=True)
        self.__volumedown_text = Text(font='Times New Roman', fontSize=35, content='-', color='#FFFFFF',
                                        isBold=False, isSys=True)
        self.__shuffle_text = Text(font=TEXT_FONT, fontSize=40, content='Shuffle', color='#FFFFFF')
        self.__hint_text = Text(font=TEXT_FONT, fontSize=40, content='Hint', color='#FFFFFF')
        self.__solve_text = Text(font=TEXT_FONT, fontSize=40, content='Solve', color='#FFFFFF')

        self.__mess = Messagebox(self.__screen)
        self.__checkMess = False

        pygame.display.set_caption('Puzzle')

    def __draw(self):
        # white screen
        surface = self.__screen
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.__puzzle.image, (20, 100))

    def __drawText(self):
        self.__title_text_rect = self.__title_text.text.get_rect(center=(self.__width / 2, 50))
        self.__music_text_rect = self.__music_text.text.get_rect(midleft=(20, 25))
        self.__volumeup_text_rect = self.__volumeup_text.text.get_rect(midleft=(45, 55))
        self.__volumedown_text_rect = self.__volumedown_text.text.get_rect(midleft=(20, 53))
        self.__shuffle_text_rect = self.__shuffle_text.text.get_rect(midleft=(625, 350))
        self.__hint_text_rect = self.__hint_text.text.get_rect(midleft=(625, 410))
        self.__solve_text_rect = self.__solve_text.text.get_rect(midleft=(625, 470))

        self.__rect_list = [self.__hint_text,
                            self.__shuffle_text,
                            self.__solve_text,
                            self.__music_text,
                            self.__volumedown_text,
                            self.__volumeup_text]

        surface = self.__screen
        # draw text
        surface.blit(self.__title_text.text, self.__title_text_rect)
        surface.blit(self.__music_text.text, self.__music_text_rect)
        surface.blit(self.__hint_text.text, self.__hint_text_rect)
        surface.blit(self.__volumeup_text.text, self.__volumeup_text_rect)
        surface.blit(self.__shuffle_text.text, self.__shuffle_text_rect)
        surface.blit(self.__volumedown_text.text, self.__volumedown_text_rect)
        surface.blit(self.__solve_text.text, self.__solve_text_rect)

    def __setPuzzle(self):
        self.__screen.blit(self.__puzzle.image, (20, 100))
        imgPieceWidth = self.__imgWidth / self.__size
        x, y = 20, 100
        for i in range(0, self.__size):
            imgTemp = []
            for j in range(0, self.__size):
                imgTemp.append(self.__puzzle.imgPieces[i][j].get_rect(left=x, top=y)) # create rectangle to move image pieces
                self.__drawRect(self.__puzzle.imgPieces[i][j], imgPieceWidth) # draw rectangle around image piece
                self.__screen.blit(self.__puzzle.imgPieces[i][j], imgTemp[j])
                x += imgPieceWidth
                if j == self.__size - 1:
                    x = 20
                    y += imgPieceWidth
            self.__puzzle.imgRect.append(imgTemp)

    def __drawHint(self, nextNode):
        imgPieceWidth = self.__imgWidth / self.__size
        x, y = 20, 100
        for i in range(0, self.__size):
            imgTemp = []
            for j in range(0, self.__size):
                imgTemp.append(self.__puzzle.imgPieces[i][j].get_rect(left=x, top=y))
                if i == nextNode[0] and j == nextNode[1]:
                    # draw rectangle around image piece of next step
                    self.__drawRect(self.__puzzle.imgPieces[i][j], imgPieceWidth, (220, 20, 60))
                self.__screen.blit(self.__puzzle.imgPieces[i][j], imgTemp[j])
                x += imgPieceWidth
                if j == self.__size - 1:
                    x = 20
                    y += imgPieceWidth

    def __playBackgroundMusic(self):
        pygame.mixer.music.load("sounds/bgmusic1.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)
        pygame.mixer.music.set_volume(0.2)
        self.__currentVolume = pygame.mixer.music.get_volume()

    def __animationPuzzle(self, current, nextNode):
        if current[0] == nextNode[0] and current[1] != nextNode[1]:
            self.__puzzle.swap_col(current[0], current[1], nextNode[1])
        elif current[1] == nextNode[1] and current[0] != nextNode[0]:
            self.__puzzle.swap_row(current[0], nextNode[0], current[1])

    def __Astar(self, start, goal):
        solve = AStar(start, self.__size, goal)
        result = solve.solve()
        for i in result:
            current = self.__getIndexMatrix(self.__puzzle.imgNum, self.__size)
            nextNode = self.__getIndexMatrix(i, self.__size)
            self.__animationPuzzle(current, nextNode)
            self.__setPuzzle()
            pygame.display.update()
            delay(100)

    def __hint(self):
        self.__checkHint = True
        solve = AStar(self.__puzzle.imgNum, self.__size, self.__goal)
        result = solve.solve()
        nextNode = self.__getIndexMatrix(result[1], self.__size)
        self.__drawHint(nextNode)

    def __volumeSetting(self, mousePos):
        if self.__music_text_rect.collidepoint(mousePos):
            if pygame.mixer.music.get_busy():  # if music is played
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

        if self.__volumedown_text_rect.collidepoint(mousePos):
            if self.__currentVolume > 0:
                self.__currentVolume -= 0.1
                self.__setVolume(self.__currentVolume)
        if self.__volumeup_text_rect.collidepoint(mousePos):
            if self.__currentVolume < 1:
                self.__currentVolume += 0.1
                self.__setVolume(self.__currentVolume)

    def __solveAndHint(self, mousePos):
        if self.__hint_text_rect.collidepoint(mousePos):
            self.__hint()

        if self.__solve_text_rect.collidepoint(mousePos):
            self.__Astar(self.__puzzle.imgNum, self.__goal)

    def __shuffle(self):
        self.__puzzle.imgPieces.clear()
        self.__puzzle = Puzzle('images/1.jpg', self.__imgWidth, self.__imgHeight, self.__size, self.__goal)
        self.__puzzle.shuffle()
        self.__setPuzzle()
        self.__start = True

    def __controlPuzzle(self, mousePos):
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                if self.__puzzle.imgRect[i][j].collidepoint(mousePos):
                    self.__puzzle.control(i, j)

    def __hoverPuzzleArea(self, mousePos):
        self.__screen.blit(self.__puzzle.image, (20, 100))
        imgPieceWidth = self.__imgWidth / self.__size
        x, y = 20, 100
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                if self.__puzzle.imgRect[i][j].collidepoint(mousePos):
                    self.__checkHint = False
                    self.__drawRect(self.__puzzle.imgPieces[i][j], imgPieceWidth, (250, 250, 250))
                elif not self.__checkHint:
                    self.__drawRect(self.__puzzle.imgPieces[i][j], imgPieceWidth)
                self.__screen.blit(self.__puzzle.imgPieces[i][j], self.__puzzle.imgRect[i][j])
                x += imgPieceWidth
                if j == self.__size - 1:
                    x = 20
                    y += imgPieceWidth

    def __hoverButton(self, mousePos):
        if self.__music_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__music_text)
        elif self.__volumeup_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__volumeup_text)
        elif self.__volumedown_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__volumedown_text)
        elif self.__shuffle_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__shuffle_text)
        elif self.__solve_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__solve_text)
        elif self.__hint_text_rect.collidepoint(mousePos):
            self.__buttonHover(self.__hint_text)
        elif self.__mess.playAgain_rect.collidepoint(mousePos) and self.__checkMess:
                self.__buttonHover(self.__mess.playAgain)
        elif self.__mess.quit_rect.collidepoint(mousePos) and self.__checkMess:
            self.__buttonHover(self.__mess.quit)
        elif self.__puzzleRect.collidepoint(mousePos) and self.__start:
            pygame.mouse.set_cursor(pygame.cursors.diamond)
        else:
            for text in self.__rect_list:
                self.__buttonLeft(text)
            self.__buttonLeft(self.__mess.playAgain)
            self.__buttonLeft(self.__mess.quit)

    def __winState(self):
        if self.__puzzle.win() and self.__start:
            self.__checkMess = True
            self.__checkHint = False
            self.__start = False
            self.__mess.create()
            # self.__draw()
            # self.__drawText()

    def __update(self):
        self.__drawText()
        self.__puzzleRect = pygame.draw.rect(self.__screen,'#CEACA3', pygame.Rect(19, 99, self.__imgWidth + 1, self.__imgHeight + 1), 1)

        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.__checkMess:
                    if self.__mess.quit_rect.collidepoint(mousePos):
                        pygame.quit()
                        exit()
                    if self.__mess.playAgain_rect.collidepoint(mousePos):
                        self.__checkMess = False
                        self.__draw()
                        self.__drawText()
                        self.__game_loop()
                else:
                    if self.__shuffle_text_rect.collidepoint(mousePos):
                        self.__shuffle()
                    elif self.__start:
                        self.__solveAndHint(mousePos)
                        self.__controlPuzzle(mousePos)
                self.__volumeSetting(mousePos)
        self.__hoverButton(mousePos)

        self.__winState()
        if self.__start:
            self.__hoverPuzzleArea(mousePos)
        # if self.__checkMess:
        #     self.__draw()
        #     self.__drawText()

    def __game_loop(self):
        while True:
            self.__update()
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def startGame(self):
        self.__playBackgroundMusic()
        self.__draw()
        self.__game_loop()

    @staticmethod
    def __getIndexMatrix(matrix, size):
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == size ** 2:
                    return [i, j]

    @staticmethod
    def __setVolume(vol):
        pygame.mixer.music.set_volume(vol)

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