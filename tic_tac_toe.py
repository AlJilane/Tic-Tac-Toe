# First step: Install Python and Pygame

# Ensure you have Python installed on your system. 
# You can download it from the official Python website: https://www.python.org/

# After installing Python, install Pygame via pip by running the following command in your terminal or command prompt:
# pip install pygame

#Sarmad alJilane

import pygame as pg
import sys
import time

# game variables
current_player = 'X'
winner = None
is_draw = False
screen_width = 400
screen_height = 450
bg_color = (255, 255, 255)
line_color = (10, 10, 10)

# 3x3 Board
board = [[None] * 3, [None] * 3, [None] * 3]

# pygame window
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((screen_width, screen_height), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# Load images
opening_image = pg.image.load('tic_tac_opening.png')
x_image = pg.image.load('x.png')
o_image = pg.image.load('o.png')

# Resize images
x_image = pg.transform.scale(x_image, (80, 80))
o_image = pg.transform.scale(o_image, (80, 80))
opening_image = pg.transform.scale(opening_image, (screen_width, screen_height - 50))

def display_opening():
    screen.fill(bg_color)

    # Opening image
    screen.blit(opening_image, (0, 0))
    
    # Welcome message
    try:
        font = pg.font.Font('FiraCode-Regular.ttf', 24)
    except FileNotFoundError:
        font = pg.font.Font(None, 24)  # Fallback if FiraCode font is not found

    welcome_text = font.render("Welcome to X / O By Jilane", True, (0, 0, 0))
    welcome_rect = welcome_text.get_rect(center=(screen_width / 2, 30))
    screen.blit(welcome_text, welcome_rect)
    
    pg.display.update()

    # Wait for user click to start
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                waiting = False

    screen.fill(bg_color)

    # Grid lines
    pg.draw.line(screen, line_color, (screen_width / 3, 0), (screen_width / 3, screen_height - 50), 7)
    pg.draw.line(screen, line_color, (screen_width / 3 * 2, 0), (screen_width / 3 * 2, screen_height - 50), 7)
    pg.draw.line(screen, line_color, (0, (screen_height - 50) / 3), (screen_width, (screen_height - 50) / 3), 7)
    pg.draw.line(screen, line_color, (0, (screen_height - 50) / 3 * 2), (screen_width, (screen_height - 50) / 3 * 2), 7)
    update_status()

def update_status():
    global is_draw

    if winner is None:
        message = current_player + "'s Turn"
    else:
        message = winner + " won!"
    if is_draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # Clear the previous status area
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    screen.fill(bg_color, (0, screen_height - 50, screen_width, 50))
    
    # Display the message
    text_rect = text.get_rect(center=(screen_width / 2, 450 - 25))
    screen.blit(text, text_rect)

    # Display status
    status_font = pg.font.Font(None, 24)
    status_text = status_font.render(message, True, (0, 0, 0))
    status_rect = status_text.get_rect(center=(screen_width / 2, screen_height - 25))
    screen.blit(status_text, status_rect)

    pg.display.update()

def check_winner():
    global board, winner, is_draw

    # Check rows, columns and diagonals for a winner
    for row in range(3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1) * (screen_height - 50) / 3 - (screen_height - 50) / 6), \
                         (screen_width, (row + 1) * (screen_height - 50) / 3 - (screen_height - 50) / 6), 4)
            break

    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * screen_width / 3 - screen_width / 6, 0), \
                         ((col + 1) * screen_width / 3 - screen_width / 6, screen_height - 50), 4)
            break

    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all([all(row) for row in board]) and winner is None:
        is_draw = True

    update_status()

def draw_symbol(row, col):
    global board, current_player
    posx = posy = 0

    if row == 1:
        posx = 30
    elif row == 2:
        posx = screen_width / 3 + 30
    elif row == 3:
        posx = screen_width / 3 * 2 + 30

    if col == 1:
        posy = 30
    elif col == 2:
        posy = (screen_height - 50) / 3 + 30
    elif col == 3:
        posy = (screen_height - 50) / 3 * 2 + 30

    board[row - 1][col - 1] = current_player
    if current_player == 'X':
        screen.blit(x_image, (posy, posx))
        current_player = 'O'
    else:
        screen.blit(o_image, (posy, posx))
        current_player = 'X'
    pg.display.update()

def handle_click():
    x, y = pg.mouse.get_pos()

    col = row = None
    if x < screen_width / 3:
        col = 1
    elif x < screen_width / 3 * 2:
        col = 2
    elif x < screen_width:
        col = 3

    if y < (screen_height - 50) / 3:
        row = 1
    elif y < (screen_height - 50) / 3 * 2:
        row = 2
    elif y < (screen_height - 50):
        row = 3

    if row and col and board[row - 1][col - 1] is None:
        draw_symbol(row, col)
        check_winner()

def reset_game():
    global board, winner, current_player, is_draw
    time.sleep(3)
    current_player = 'X'
    is_draw = False
    display_opening()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]

display_opening()

# Game loop
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            handle_click()
            if winner or is_draw:
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)
