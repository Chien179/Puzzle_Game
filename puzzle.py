import random
import numpy
import pygame


class Puzzle:
    def __init__(self, image, blankColor, width, height, size):
        self.__image = image
        self.imgPieces, self.imgRect = [], []
        self.__width, self.__height = width, height
        self.__size = size
        self.imgNum = [[]]
        self.__createPuzzle(blankColor)

    def __createPuzzle(self, blankColor):
        img = pygame.image.load(self.__image).convert_alpha()
        img = pygame.transform.smoothscale(img, (self.__width, self.__height))

        x, y = 0, 0
        for _ in range(0, self.__size):
            imgTemp = []
            for j in range(0, self.__size):
                imgTemp.append(img.subsurface(x, y, self.__width / self.__size, self.__height / self.__size))
                x += self.__width / self.__size
                if j == 2:
                    x = 0
                    y += self.__height / self.__size
            self.imgPieces.append(imgTemp)

        blank = pygame.Surface((self.__width / self.__size, self.__height / self.__size))
        blank.fill(blankColor)
        self.imgPieces[self.__size - 1][self.__size - 1] = blank

    def shuffle(self):
        imgTemp = []
        for i in range(0, self.__size):
            imgTemp.append(self.imgPieces[i].copy())
        Num = [i for i in range(1, 10)]
        n = -1

        while n % 2 != 0:
            random.shuffle(Num)
            n = check_state(Num)
        self.imgNum = numpy.reshape(Num, (3, 3))

        for i in range(0, 3):
            for j in range(0, 3):
                row = int((self.imgNum[i][j] - 1) / 3)
                col = int((self.imgNum[i][j] - 1) % 3)
                self.imgPieces[i][j] = imgTemp[row][col]

    def control(self, numPieceX, numPieceY):
        if numPieceX > 0:
            if self.imgNum[numPieceX - 1][numPieceY] == 9:
                self.__swap_row(numPieceX, numPieceX - 1, numPieceY)
        if numPieceX < 3 - 1:
            if self.imgNum[numPieceX + 1][numPieceY] == 9:
                self.__swap_row(numPieceX, numPieceX + 1, numPieceY)
        if numPieceY > 0:
            if self.imgNum[numPieceX][numPieceY - 1] == 9:
                self.__swap_col(numPieceX, numPieceY, numPieceY - 1)
        if numPieceY < 3 - 1:
            if self.imgNum[numPieceX][numPieceY + 1] == 9:
                self.__swap_col(numPieceX, numPieceY, numPieceY + 1)

    def __swap_row(self, row, rowb, col):
        imgtemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[rowb][col]
        self.imgPieces[rowb][col] = imgtemp
        numtemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[rowb][col]
        self.imgNum[rowb][col] = numtemp

    def __swap_col(self, row, col, colb):
        imgtemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[row][colb]
        self.imgPieces[row][colb] = imgtemp
        numtemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[row][colb]
        self.imgNum[row][colb] = numtemp

    def displayImage(self):
        return pygame.image.load(self.__image).convert_alpha()


def check_state(num):
    n = 0
    for i in range(0, 9):
        sum = 0
        for j in range(i + 1, 9):
            if num[j] < num[i] and num[i] != 9:
                sum += 1
        n += sum

    return n
