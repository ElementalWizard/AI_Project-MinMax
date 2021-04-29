from copy import deepcopy as copy
from time import sleep
import pygame


BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

def minimax(board, depth, player, game):
    if depth == 0 or board.winner() != None:
        return board.utilityValue(), board

    if player:
        alpha = float('-inf')
        bestMove = None
        for move in getAllPossibleMove(board, WHITE, game):
            result = minimax(move, depth-1, False, game)[0]
            alpha = max(alpha, result)
            if alpha == result:
                bestMove = move

        return alpha, bestMove
    else:
        beta = float('inf')
        bestMove = None
        for move in getAllPossibleMove(board, BLACK, game):
            result = minimax(move, depth-1, True, game)[0]
            beta = min(beta, result)
            if beta == result:
                bestMove = move

        return beta, bestMove


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.eating(skip)
    return board


def getAllPossibleMove(board, color, game):
    movelist = []
    listOfPieces = board.getAllPiecesByColor(color)
    for piece in listOfPieces:
        listOfMoving = board.getValidMove(piece)
        getValidMovesList = listOfMoving
        for move, skip in getValidMovesList.items():
            copyBoard = copy(board)
            copyPiece = copyBoard.getPiece(piece.row, piece.column)
            simulate_board = simulate_move(copyPiece, move, copyBoard, game, skip)
            movelist.append(simulate_board)

    return movelist