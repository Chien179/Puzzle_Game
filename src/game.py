import pygame
from pygame.time import delay
from file import File
from puzzle import Puzzle
from display import Display
from algorithm import AStar

class Game:

    def __init__(self, width, height, imgWidth, imgHeight, size):
        self.__display = Display(size,
                                 width, height,
                                 imgWidth, imgHeight)

    def __animationPuzzle(self, current, nextNode):
        if current[0] == nextNode[0] and current[1] != nextNode[1]:
            self.__display.puzzle.swap_col(current[0], current[1], nextNode[1])
        elif current[1] == nextNode[1] and current[0] != nextNode[0]:
            self.__display.puzzle.swap_row(current[0], nextNode[0], current[1])

    def __solve(self, start, goal):
        solve = AStar(start, self.__display.size, goal)
        result = solve.solve()
        for i in result:
            current = self.__getIndexMatrix(self.__display.puzzle.imgNum, self.__display.size)
            nextNode = self.__getIndexMatrix(i, self.__display.size)
            self.__animationPuzzle(current, nextNode)
            self.__display.setPuzzle()
            pygame.display.update()
            delay(200)

    def __hint(self):
        self.__display.checkHint = True
        solve = AStar(self.__display.puzzle.imgNum, self.__display.size, self.__display.goal)
        result = solve.solve()
        nextNode = self.__getIndexMatrix(result[1], self.__display.size)
        self.__display.drawHint(nextNode)

    def __solveAndHint(self, mousePos):
        if self.__display.hint_text_rect.collidepoint(mousePos):
            self.__hint()

        if self.__display.solve_text_rect.collidepoint(mousePos):
            self.__solve(self.__display.puzzle.imgNum, self.__display.goal)

    def __playBackgroundMusic(self):
        pygame.mixer.music.load("../sounds/bgmusic1.mp3")
        pygame.mixer.music.play(loops = 0, start = 0.0)
        pygame.mixer.music.set_volume(0.2)
        self.__currentVolume = pygame.mixer.music.get_volume()

    def __volumeSetting(self, mousePos):
        if self.__display.musicImg_rect.collidepoint(mousePos):
            if pygame.mixer.music.get_busy():  # if music is played
                self.__display.musicPlaying = False
                pygame.mixer.music.pause()
                self.__display.musicIcon('../icons/play.png')
            else:
                self.__display.musicPlaying = True
                pygame.mixer.music.unpause()
                self.__display.musicIcon()

        if self.__display.volumeDown_text_rect.collidepoint(mousePos):
            if self.__currentVolume > 0:
                self.__currentVolume -= 0.1
                self.__setVolume(self.__currentVolume)
        if self.__display.volumeUp_text_rect.collidepoint(mousePos):
            if self.__currentVolume < 1:
                self.__currentVolume += 0.1
                self.__setVolume(self.__currentVolume)

    def __shuffle(self):
        self.__display.puzzle.imgPieces.clear()
        self.__display.puzzle = Puzzle(self.__display.image, self.__display.imgWidth, self.__display.imgHeight, self.__display.size, self.__display.goal)
        self.__display.puzzle.shuffle()
        self.__display.setPuzzle()
        self.__start = True
        self.__display.start = True

    def __controlPuzzle(self, mousePos):
        for i in range(0, self.__display.size):
            for j in range(0, self.__display.size):
                if self.__display.puzzle.imgRect[i][j].collidepoint(mousePos):
                    self.__display.puzzle.control(i, j)

    def __winState(self):
        if self.__display.puzzle.win() and self.__start:
            self.__display.checkWin = True
            self.__display.checkHint = False
            self.__start = False
            self.__display.start = False

    def __update(self):
        self.__display.draw()
        self.__display.drawText()
        if self.__display.checkWin:
            delay(500)

        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.__display.checkWin:
                    if self.__display.mess.quit_rect.collidepoint(mousePos):
                        pygame.quit()
                        exit()
                    if self.__display.mess.playAgain_rect.collidepoint(mousePos):
                        self.__display.checkWin = False
                        self.__display.draw()
                        self.__display.drawText()
                        self.__game_loop()
                else:
                    if not self.__display.start:
                        if self.__display.toolBar.fileButton_rect.collidepoint(mousePos):
                            path = File().file()
                            if path != '':
                                self.__display.image = path
                                self.__display.puzzle = Puzzle(self.__display.image,
                                                       self.__display.imgWidth, self.__display.imgHeight,
                                                       self.__display.size, self.__display.goal)
                    if self.__display.shuffle_text_rect.collidepoint(mousePos):
                        self.__shuffle()
                    elif self.__display.start:
                        self.__solveAndHint(mousePos)
                        self.__controlPuzzle(mousePos)
                    self.__volumeSetting(mousePos)

        self.__display.hoverButton(mousePos)
        self.__winState()
        if self.__display.start:
            self.__display.hoverPuzzleArea(mousePos)

    def __game_loop(self):
        while True:
            self.__update()
            pygame.display.update()
            pygame.time.Clock().tick(60)

    def startGame(self):
        self.__playBackgroundMusic()
        self.__display.draw()
        self.__game_loop()

    @staticmethod
    def __setVolume(vol):
        pygame.mixer.music.set_volume(vol)

    @staticmethod
    def __getIndexMatrix(matrix, size):
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == size ** 2:
                    return [i, j]
