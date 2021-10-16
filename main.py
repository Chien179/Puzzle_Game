from game import Game

WIDTH = 800
HEIGHT = 600
IMGWIDTH = 480
IMGHEIGHT = 480
SIZE = 3


if __name__ == '__main__':
    game = Game(WIDTH, HEIGHT, IMGWIDTH, IMGHEIGHT, SIZE)
    game.game_loop()
