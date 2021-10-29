import random
import numpy
import pygame


class Puzzle:
    def __init__(self, image, width, height, size):
        self.image = pygame.image.load(image).convert_alpha()
        self.imgPieces, self.imgRect = [], []
        self.__width, self.__height = width, height
        self.__size = size
        self.imgNum = []
        self.__createPuzzle()

    def __createPuzzle(self):
        if self.image.get_width() > self.__width and self.image.get_height() > self.__height:
            x = int((self.image.get_width() - self.__width) / 2)
            y = int((self.image.get_height() - self.__height) / 2)
            self.image = self.image.subsurface((x, y, self.__width, self.__height))

        x, y = 0, 0
        for _ in range(0, self.__size):
            imgTemp = []
            for j in range(0, self.__size):
                imgTemp.append(self.image.subsurface(x, y, self.__width / self.__size, self.__height / self.__size).convert_alpha())
                x += self.__width / self.__size
                if j == 2:
                    x = 0
                    y += self.__height / self.__size
            self.imgPieces.append(imgTemp)

        blank = pygame.Surface((self.__width / self.__size, self.__height / self.__size))
        blank = blank.convert_alpha()
        blank.fill('black')
        blank.set_alpha(220)
        self.imgPieces[self.__size - 1][self.__size - 1] = blank

    def shuffle(self):
        imgTemp = []
        for i in range(0, self.__size):
            imgTemp.append(self.imgPieces[i].copy())
        num = [i for i in range(1, (self.__size**2) + 1)]
        n = -1

        while n % 2 != 0:
            random.shuffle(num)
            n = self.__check_state(num)
        self.imgNum = numpy.reshape(num, (3, 3)).tolist()

        for i in range(0, 3):
            for j in range(0, 3):
                row = int((self.imgNum[i][j] - 1) / 3)
                col = int((self.imgNum[i][j] - 1) % 3)
                self.imgPieces[i][j] = imgTemp[row][col]

    def control(self, numPieceX, numPieceY):
        if numPieceX > 0:
            if self.imgNum[numPieceX - 1][numPieceY] == self.__size ** 2:
                self.swap_row(numPieceX, numPieceX - 1, numPieceY)
        if numPieceX < 3 - 1:
            if self.imgNum[numPieceX + 1][numPieceY] == self.__size ** 2:
                self.swap_row(numPieceX, numPieceX + 1, numPieceY)
        if numPieceY > 0:
            if self.imgNum[numPieceX][numPieceY - 1] == self.__size ** 2:
                self.swap_col(numPieceX, numPieceY, numPieceY - 1)
        if numPieceY < 3 - 1:
            if self.imgNum[numPieceX][numPieceY + 1] == self.__size ** 2:
                self.swap_col(numPieceX, numPieceY, numPieceY + 1)

    def swap_row(self, row, rowb, col):
        imgtemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[rowb][col]
        self.imgPieces[rowb][col] = imgtemp
        numtemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[rowb][col]
        self.imgNum[rowb][col] = numtemp

    def swap_col(self, row, col, colb):
        imgtemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[row][colb]
        self.imgPieces[row][colb] = imgtemp
        numtemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[row][colb]
        self.imgNum[row][colb] = numtemp

    def displayImage(self):
        return pygame.image.load(self.image).convert_alpha()


    def __check_state(self, num):
        n = 0
        for i in range(0, self.__size ** 2):
            sum = 0
            for j in range(i + 1, self.__size ** 2):
                if num[j] < num[i] != self.__size ** 2:
                    sum += 1
            n += sum

        return n
