import pygame

WIDTH = 800
HEIGHT = 600

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width, self.height = width,height
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption('Puzzle')

    def create_font(self, font, fontSize, content, color):
        f = pygame.font.SysFont(font, fontSize, False, False)
        text = f.render(content, False, color)
        return text

    def draw(self):
        #white screen
        surface = self.screen
        surface.fill('#8AAAE5')
        
        #text
        shuffle_text = self.create_font(font='Arial', fontSize=30, content='Shuffle', color='#FFFFFF')
        shuffle_text_rect = shuffle_text.get_rect(midleft=(650, 350))

        title_text = self.create_font(font='Arial', fontSize=35, content='PUZZLE', color='#FFFFFF')
        title_text_rect = title_text.get_rect(center=(WIDTH/2, 50))

        surface.blit(title_text, title_text_rect)
        surface.blit(shuffle_text, shuffle_text_rect)

    def update(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def game_loop(self):
        while True:
            self.update()
            self.draw()
            pygame.display.update()

if __name__ == '__main__':
    game = Game(WIDTH,HEIGHT)
    game.game_loop()