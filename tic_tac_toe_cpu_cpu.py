import pygame
import sys
import math
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
CELL_SIZE = WIDTH // 3
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Initialize the board
board = [[' ' for _ in range(3)] for _ in range(3)]

def draw_board(board):
    '''
    Draw Tic-Tac-Toe board.
    '''
    # Clear the screen
    screen.fill(WHITE)

    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
    
    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
    
    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    '''
    Draw an 'X' when an empty cell is clicked.
    '''
    x_pos = col * CELL_SIZE + CELL_SIZE // 2
    y_pos = row * CELL_SIZE + CELL_SIZE // 2
    offset = CELL_SIZE // 4
    pygame.draw.line(screen, BLACK, (x_pos - offset, y_pos - offset), (x_pos + offset, y_pos + offset), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (x_pos + offset, y_pos - offset), (x_pos - offset, y_pos + offset), LINE_WIDTH)

def draw_o(row, col):
    '''
    Draw an 'O' when an empty cell is clicked.
    '''
    x_pos = col * CELL_SIZE + CELL_SIZE // 2
    y_pos = row * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 4
    pygame.draw.circle(screen, BLACK, (x_pos, y_pos), radius, LINE_WIDTH)

def check_winner(board):
    '''
    Check rows, columns, and diagonals for a winner.
    '''
    for i in range(3):
        # Check for 3 in a row
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return board[i][0]
        
        # Check for 3 in a column
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            return board[0][i]
        
    diag1 = board[0][0] == board[1][1] == board[2][2] != ' '
    diag2 = board[0][2] == board[1][1] == board[2][0] != ' '

    # Check for 3 in a diagonal
    if diag1 or diag2:
        return board[1][1]
    
    # No winner yet
    return None

def check_board_full(board):
    '''
    Check if the board is full.
    '''
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

def minimax(board, depth, is_maximizing):
    '''
    Minimax Algorithm
    '''
    result = check_winner(board)
    if result is not None:
        if result == 'X':
            return 1 - depth
        elif result == 'O':
            return -1 + depth
        else:
            return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    best_score = min(score, best_score)
        return best_score

def cpu_player_move(board):
    '''
    Decides how a CPU should move based on minimax or local optimal solution.
    '''
    # Check for winning moves
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'
                if check_winner(board) == 'O':
                    board[row][col] = ' '  # Reset the board
                    return row, col
                board[row][col] = ' '  # Reset the board

    # Check for blocking moves
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'X'
                if check_winner(board) == 'X':
                    board[row][col] = ' '  # Reset the board
                    return row, col
                board[row][col] = ' '  # Reset the board

    # If no winning or blocking moves, use Minimax
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'O'  # Simulate placing 'O' on the board
                if check_winner(board) == 'O':
                    board[row][col] = ' '  # Reset the board
                    return row, col
                board[row][col] = ' '  # Reset the board
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'X'  # Simulate placing 'X' on the board
                if check_winner(board) == 'X':
                    board[row][col] = ' '  # Reset the board
                    return row, col
                board[row][col] = ' '  # Reset the board

    # If no winning or blocking moves, use Minimax
    best_score = -math.inf
    best_move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                board[row][col] = 'X'
                score = minimax(board, 0, False)
                board[row][col] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    if best_move:
        return best_move                
    # If no winning or blocking moves, use Minimax
    available_actions = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    if available_actions:
        return random.choice(available_actions)

def main():
    global board
    current_player = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(board)
        pygame.display.update()

        # Reset game if there is a winner
        if check_winner(board):
            if current_player == 'X':
                print('O won!')
            else:
                print('X won!')
                time.sleep(1)
            board = [[' ' for _ in range(3)] for _ in range(3)]
            current_player = 'X'
            
        # Reset game if board is full
        if check_board_full(board):
            print('Draw!')
            time.sleep(1)
            board = [[' ' for _ in range(3)] for _ in range(3)]
            current_player = 'X'

        # CPU 'O' 
        if current_player == 'O':
            row, col = cpu_player_move(board)
            board[row][col] = 'O'
            current_player = 'X'
        else:
            row, col = cpu_player_move(board)
            board[row][col] = 'X'
            current_player = 'O'

if __name__ == '__main__':
    main()
