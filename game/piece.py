import pygame


WIDTH = 400
HEIGHT = 400
COLUMNS = 8
ROWS = 8
SIZE = WIDTH // COLUMNS

# rgb
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

Black_Piece = pygame.transform.scale(pygame.image.load('resources/black.png'), (50, 50))
BlackQueen = pygame.transform.scale(pygame.image.load('resources/blackqueen.png'), (50, 50))
White_Piece = pygame.transform.scale(pygame.image.load('resources/white.png'), (50, 50))
WhiteQueen = pygame.transform.scale(pygame.image.load('resources/whitequeen.png'), (50, 50))

class Piece:

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.queen = False
        self.x = 0
        self.y = 0
        self.position()

    def position(self):
        self.x = SIZE * self.column + SIZE // 2
        self.y = SIZE * self.row + SIZE // 2

    def createQueen(self):
        self.queen = True
    
    def draw(self, display):
        if self.color == BLACK:
            display.blit(Black_Piece, (self.x - Black_Piece.get_width() // 2, self.y - Black_Piece.get_height() // 2))
        elif self.color == WHITE:
            display.blit(White_Piece, (self.x - White_Piece.get_width() // 2, self.y - White_Piece.get_height() // 2))

        if self.queen:
            if self.color == BLACK:
                display.blit(BlackQueen, (self.x - BlackQueen.get_width() // 2, self.y - BlackQueen.get_height() // 2))
            else:
                display.blit(WhiteQueen, (self.x - WhiteQueen.get_width() // 2, self.y - WhiteQueen.get_height() // 2))


    def move(self, row, column):
        self.row = row
        self.column = column
        self.position()