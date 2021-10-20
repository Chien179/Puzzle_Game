import pygame
from puzzle import Puzzle

class Game:
    def __init__(self, width, height, imgWidth, imgHeight, size):
        pygame.init()
        self.__backgroundColor = '#8AAAE5'
        self.__width, self.__height = width, height
        self.__imgWidth, self.__imgHeight = imgWidth, imgHeight
        self.__size = size
        self.__screen = pygame.display.set_mode((self.__width,self.__height))
        self.__puzzle = Puzzle('images/1.jpg', self.__backgroundColor, self.__imgWidth, self.__imgHeight, self.__size)
        self.__start = False
        pygame.display.set_caption('Puzzle')


    def __create_font(self, font, fontSize, content, color, isBold):
        f = pygame.font.SysFont(font, fontSize, isBold, False)
        text = f.render(content, False, color)
        return text

    def __draw(self):
        # white screen
        surface = self.__screen
        surface.fill(self.__backgroundColor)
        
        # text
        shuffle_text = self.__create_font(font='Arial', fontSize=30, content='Shuffle', color='#FFFFFF', isBold=False)
        self.__shuffle_text_rect = shuffle_text.get_rect(midleft=(650, 350))

        title_text = self.__create_font(font='Times New Roman', fontSize=35, content='PUZZLE', color='#FFFFFF', isBold=True)
        self.__title_text_rect = title_text.get_rect(center=(self.__width/2, 50))

        surface.blit(title_text, self.__title_text_rect)
        surface.blit(shuffle_text, self.__shuffle_text_rect)


        music_text = self.__create_font(font='Arial', fontSize=20, content='MUTE', color='#FFFFFF', isBold=False)
        self.__music_text_rect = music_text.get_rect(midleft=(20, 20))
        surface.blit(music_text, self.__music_text_rect)

    def __drawPuzzle(self):
        x, y = 20, 100
        for i in range(0, 3):
            imgTemp = []
            for j in range(0, 3):
                # creat rect to move image pieces
                imgTemp.append(self.__puzzle.imgPieces[i][j].get_rect(left=x, top=y))
                self.__screen.blit(self.__puzzle.imgPieces[i][j], imgTemp[j])
                x += 480 / 3
                if j == 2:
                    x = 20
                    y += 480 / 3
            self.__puzzle.imgRect.append(imgTemp)

    def __update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.__shuffle_text_rect.collidepoint(pygame.mouse.get_pos()):
                    self.__puzzle.imgPieces.clear()
                    self.__puzzle = Puzzle('images/1.jpg', self.__backgroundColor, self.__imgWidth, self.__imgHeight, self.__size)
                    self.__puzzle.shuffle()
                    self.__drawPuzzle()
                    self.__start = True
                elif self.__start is True:
                    for i in range(0, self.__size):
                        for j in range(0, self.__size):
                            if self.__puzzle.imgRect[i][j].collidepoint(pygame.mouse.get_pos()):
                                self.__puzzle.control(i, j)
                            self.__drawPuzzle()
                elif self.__music_text_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.__isPlayingMusic == True:
                        pygame.mixer.music.pause()
                        self.__isPlayingMusic = False
                    else:
                        pygame.mixer.music.unpause()
                        self.__isPlayingMusic = True

    def __playBackgroundMusic(self):
        self.__isPlayingMusic = True
        pygame.mixer.music.unload()
        pygame.mixer.music.load("sounds/bgmusic1.mp3")
        pygame.mixer.music.play(loops=0, start=0.0)

    def game_loop(self):
        self.__playBackgroundMusic()
        while True:
            self.__update()
            self.__draw()
            self.__drawPuzzle()
            pygame.display.update()
            pygame.time.Clock().tick(60)