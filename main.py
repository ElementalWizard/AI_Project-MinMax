import pygame
from game.game import Game
from minimax import minimax

WIDTH = 400
HEIGHT = 400
COLUMNS = 8
ROWS = 8
SIZE = WIDTH // COLUMNS

# rgb
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers vs IA')
frames = 60


def main():
    gameOn = True
    clock = pygame.time.Clock()
    game = Game(display)

    while gameOn:
        # pygame.time.delay(500)
        clock.tick(frames)

        if game.turn == WHITE:
            value, new_board = minimax(game.getBoard(), 4, WHITE, game)
            game.moveFromIA(new_board)

        if game.winner() != None:
            print(game.winner())
            gameOn = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOn = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, column = get_pos(pos)
                game.select(row, column)

        game.update()

    pygame.quit()


def get_pos(pos):
    x, y = pos
    posy = y // SIZE
    posx = x // SIZE
    return posy, posx


main()
