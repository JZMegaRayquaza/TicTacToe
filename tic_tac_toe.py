import pygame
import sys

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

def main():
    global board
    current_player = 'X'

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                if board[row][col] == ' ':
                    board[row][col] = current_player
                    current_player = 'O' if current_player == 'X' else 'X'
        draw_board()

        # Reset game if there is a winner or board is full
        if check_winner(board) or check_board_full(board):
            board = [[' ' for _ in range(3)] for _ in range(3)]
            current_player = 'X'

        pygame.display.update()

if __name__ == '__main__':
    main()