import random
import numpy
import pygame

class Puzzle:
    def __init__(self, image, width, height, size, goal):
        self.image = pygame.image.load(image).convert_alpha()
        self.imgPieces, self.imgRect = [], []
        self.__width, self.__height = width, height
        self.__size = size
        self.imgNum = []
        self.__createPuzzle()
        self.__goal = goal

    def __createPuzzle(self):
        # if images size bigger then imgWidth and Height, cut image
        if self.image.get_width() > self.__width and self.image.get_height() > self.__height:
            x = int((self.image.get_width() - self.__width) / 2)
            y = int((self.image.get_height() - self.__height) / 2)
            self.image = self.image.subsurface((x, y, self.__width, self.__height))
        #if images size bigger then imgWidth and Height, resize image
        elif self.image.get_width() < self.__width and self.image.get_height() < self.__height:
            self.image = pygame.transform.scale(self.image, (self.__width, self.__height))

        x, y = 0, 0
        for _ in range(0, self.__size):
            imgTemp = []
            for j in range(0, self.__size):
                #create subsurface for image pieces
                imgTemp.append(self.image.subsurface(x, y, self.__width / self.__size, self.__height / self.__size).convert_alpha())
                x += self.__width / self.__size
                if j == self.__size - 1:
                    x = 0
                    y += self.__height / self.__size
            self.imgPieces.append(imgTemp)
        #creat image pieces 9
        blank = pygame.Surface((self.__width / self.__size, self.__height / self.__size))
        blank = blank.convert_alpha()
        blank.fill('black')
        blank.set_alpha(200)
        self.imgPieces[self.__size - 1][self.__size - 1] = blank


    def shuffle(self):
        imgTemp = []
        for i in range(0, self.__size):
            imgTemp.append(self.imgPieces[i].copy())
        num = [i for i in range(1, (self.__size**2) + 1)]
        n = -1

        #check goal state can reverse to start state
        while n % 2 != 0:
            random.shuffle(num)
            n = self.__check_state(num)
        self.imgNum = numpy.reshape(num, (self.__size, self.__size)).tolist()

        #make imgPieces state like imgNum
        for i in range(0, self.__size):
            for j in range(0, self.__size):
                row = int((self.imgNum[i][j] - 1) / self.__size)
                col = int((self.imgNum[i][j] - 1) % self.__size)
                self.imgPieces[i][j] = imgTemp[row][col]

    def control(self, numPieceX, numPieceY):
        if numPieceX > 0:
            if self.imgNum[numPieceX - 1][numPieceY] == self.__size ** 2:
                self.swap_row(numPieceX, numPieceX - 1, numPieceY)
        if numPieceX < self.__size - 1:
            if self.imgNum[numPieceX + 1][numPieceY] == self.__size ** 2:
                self.swap_row(numPieceX, numPieceX + 1, numPieceY)
        if numPieceY > 0:
            if self.imgNum[numPieceX][numPieceY - 1] == self.__size ** 2:
                self.swap_col(numPieceX, numPieceY, numPieceY - 1)
        if numPieceY < self.__size - 1:
            if self.imgNum[numPieceX][numPieceY + 1] == self.__size ** 2:
                self.swap_col(numPieceX, numPieceY, numPieceY + 1)

    #move imgPiece row
    def swap_row(self, row, rowb, col):
        imgTemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[rowb][col]
        self.imgPieces[rowb][col] = imgTemp
        numTemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[rowb][col]
        self.imgNum[rowb][col] = numTemp

    # move imgPiece col
    def swap_col(self, row, col, colb):
        imgTemp = self.imgPieces[row][col]
        self.imgPieces[row][col] = self.imgPieces[row][colb]
        self.imgPieces[row][colb] = imgTemp
        numTemp = self.imgNum[row][col]
        self.imgNum[row][col] = self.imgNum[row][colb]
        self.imgNum[row][colb] = numTemp

    def displayImage(self):
        return self.image

    def win(self):
        return self.imgNum == self.__goal

    def __check_state(self, num):
        n = 0
        for i in range(0, self.__size ** 2):
            sum = 0
            for j in range(i + 1, self.__size ** 2):
                if num[j] < num[i] != self.__size ** 2:
                    sum += 1
            n += sum

        return n
