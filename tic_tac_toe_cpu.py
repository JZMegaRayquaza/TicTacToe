import pygame
import sys
import math

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

def draw_board():
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

def get_row_col_from_mouse(pos):
    '''
    Get location of mouse cursor.
    '''
    x, y = pos
    row = y // CELL_SIZE
    col = x // CELL_SIZE
    return row, col

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
    # If it's the first move and the player chose a corner, CPU blocks the center
    if board[1][1] == ' ' and sum(row.count(' ') for row in board) == 8:
        return 1, 1  # Block the center
    
    # If it's the second move and the CPU has placed 'O' in the center
    if sum(row.count(' ') for row in board) == 6 and board[1][1] == 'O':
        # Block an edge to force the player to block
        for move in [(0, 1), (1, 0), (1, 2), (2, 1)]:
            if board[move[0]][move[1]] == ' ':
                return move

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
        return available_actions[0]

def main():
    global board
    current_player = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_player == 'X':
                    row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                    if board[row][col] == ' ':
                        board[row][col] = current_player
                        current_player = 'O'
        draw_board()

        # Reset game if there is a winner or board is full
        if check_winner(board) or check_board_full(board):
            board = [[' ' for _ in range(3)] for _ in range(3)]
            current_player = 'X'

        # CPU moves after check to avoid crash    
        if current_player == 'O':
            row, col = cpu_player_move(board)
            board[row][col] = 'O'
            current_player = 'X'

        pygame.display.update()

if __name__ == '__main__':
    main()