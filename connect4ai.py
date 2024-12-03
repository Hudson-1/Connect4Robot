# Imports
import numpy as np
import pygame
import sys
import math
from threading import Timer
import random

# Global Constants
ROWS = 6
COLS = 7
PLAYER_TURN = 0
AI_TURN = 1
PLAYER_PIECE = 1
AI_PIECE = 2
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Functions
def create_board():
    return np.zeros((ROWS, COLS))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    for c in range(3, COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True

def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            else:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
    pygame.display.update()

def detect_human_move():
    col = random.randint(0, COLS - 1)  # Simulated input
    print(f"Human move detected in column {col}")
    return col

def move_arm_to_column(col):
    print(f"Moving arm to column {col}")

def move_arm_out_of_way():
    print("Moving arm out of the way")

def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    return [col for col in range(COLS) if is_valid_location(board, col)]

def score_position(board, piece):
    return 0  # Placeholder scoring function

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def end_game():
    global game_over
    game_over = True
    print(game_over)

# Initialize the game
board = create_board()
game_over = False
not_over = True
turn = PLAYER_TURN
pygame.init()
SQUARESIZE = 100
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE / 2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)
my_font = pygame.font.SysFont("monospace", 75)
draw_board(board)
pygame.display.update()

# Game Loop
while not game_over:
    if turn == PLAYER_TURN and not game_over and not_over:
        col = detect_human_move()
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)
            if winning_move(board, PLAYER_PIECE):
                print("HUMAN WINS!")
                label = my_font.render("HUMAN WINS!", 1, RED)
                screen.blit(label, (40, 10))
                not_over = False
                Timer(3.0, end_game).start()
            draw_board(board)
            turn = (turn + 1) % 2

    if turn == AI_TURN and not game_over and not_over:
        col, _ = minimax(board, 5, -math.inf, math.inf, True)
        if is_valid_location(board, col):
            move_arm_to_column(col)
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)
            if winning_move(board, AI_PIECE):
                print("AI WINS!")
                label = my_font.render("AI WINS!", 1, YELLOW)
                screen.blit(label, (40, 10))
                not_over = False
                Timer(3.0, end_game).start()
            move_arm_out_of_way()
            draw_board(board)
            turn = (turn + 1) % 2
