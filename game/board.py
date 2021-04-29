import pygame
from game.piece import Piece

WIDTH = 400
HEIGHT = 400
COLUMNS = 8
ROWS = 8
SIZE = WIDTH // COLUMNS


# rgb
RED = pygame.Color(255, 0, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
TIE = pygame.Color(255,0,100)
BROWN = pygame.Color(162,42,42)


class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.createBoard()
    
    def drawBoard(self, display):
        display.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(display, WHITE, (row * SIZE, col * SIZE, SIZE, SIZE))

    def utilityValue(self):
        return self.white_left - self.black_left + (self.white_kings  - self.black_kings )

    def getAllPiecesByColor(self, color):
        piecelist = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    piecelist.append(piece)
        return piecelist

    def move(self, piece, row, column):
        self.board[piece.row][piece.column], self.board[row][column] = self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        if row == ROWS - 1 or row == 0:
            piece.createQueen()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def getPiece(self, row, col):
        return self.board[row][col]

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for column in range(COLUMNS):
                if column % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, column, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, column, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, display):
        self.drawBoard(display)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(display)

    def eating(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == BLACK:
                    self.black_left -= 1
                else:
                    self.white_left -= 1


    def noMoveLeft(self, listPieces):
        notMoving = False
        lenPiece = len(listPieces)
        count = 0
        for piece in listPieces:
            lenght = len(self.getValidMove(piece))
            if lenght == 0:
                count = count + 1

        if count == lenPiece:
            notMoving = True

        return notMoving

    def winner(self):
        pieceBlack = self.getAllPiecesByColor(BLACK)
        pieceWhite = self.getAllPiecesByColor(WHITE)

        if self.black_left <= 0 or self.noMoveLeft(pieceBlack):
            print("THE WINNER IS WHITE: ")
            return WHITE
        elif self.white_left <= 0 or self.noMoveLeft(pieceWhite):
            print("THE WINNER IS BLACK: ")
            return BLACK

        elif self.black_left == 1 and self.white_left == 1:
            print("TIE")
            return TIE

        return None
    
    def getValidMove(self, piece):
        movelist = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == BLACK or piece.queen:
            movelist.update(self.moveLeft(row - 1, max(row - 3, -1), -1, piece.color, left))
            movelist.update(self.moveRight(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.queen:
            movelist.update(self.moveLeft(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            movelist.update(self.moveRight(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    
        return movelist

    def moveLeft(self, start, stop, step, color, left, skiplist=[]):
        movelist = {}
        last = []
        for move in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[move][left]
            if current == 0:
                if skiplist and not last:
                    break
                elif skiplist:
                    movelist[(move, left)] = last + skiplist
                else:
                    movelist[(move, left)] = last
                
                if last:
                    if step == -1:
                        row = max(move-3, 0)
                    else:
                        row = min(move+3, ROWS)
                    movelist.update(self.moveLeft(move + step, row, step, color, left - 1, skiplist=last))
                    movelist.update(self.moveRight(move + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return movelist

    def moveRight(self, start, stop, step, color, right, skipped=[]):
        movelist = {}
        last = []
        for move in range(start, stop, step):
            if right >= COLUMNS:
                break
            
            current = self.board[move][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movelist[(move,right)] = last + skipped
                else:
                    movelist[(move, right)] = last
                
                if last:
                    if step == -1:
                        row = max(move-3, 0)
                    else:
                        row = min(move+3, ROWS)
                    movelist.update(self.moveLeft(move + step, row, step, color, right - 1, skiplist=last))
                    movelist.update(self.moveRight(move + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return movelist