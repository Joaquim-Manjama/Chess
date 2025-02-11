import pygame, sys
from Board import Board
from Pieces import Pieces

pygame.init()

class Game:
    def __init__(self):

        #SCREEN
        self.width = 800
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("JmD' Chess Game")

        #FOREIGNER
        self.board = Board()
        self.pieces = Pieces()
        #GAME VARIABLES
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            self.board.render(self.screen)
            self.board.hover(self.screen)
            self.board.draw_lines(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if self.board.is_clicking_one_potential_square(x, y):
                        self.board.turn = -(self.board.turn - 1) 
                    self.board.select_square(x, y)
                
            self.pieces.render(self.screen, self.board.map)
            
            self.clock.tick(30)
            pygame.display.update()

Game().run()