import pygame as pg
import numpy as np
import random
from copy import deepcopy

#малюємо дошку
def draw_board(window_width: float, window_height: float, score: int) -> None:
    pg.draw.rect(screen, colors["board"], [0, 0, window_width, window_height * 0.8])
    pg.draw.rect(screen, colors["bg"], [window_width * 0.1, 0, window_width * 0.8, window_height * 0.8], border_radius=5)
    pg.draw.rect(screen, colors["board_button"], [window_width, window_height * 0.8, window_width, window_height * 0.2])
    font_one = pg.font.SysFont( "Arial" , 24)
    score_text = font_one.render(f'Рахунок: {score}', True, colors["board_button_text"])
    high_score_text = font_one.render(f'Найкращий рахунок: {hight_score}', True, colors["board_button_text"])
    screen.blit(score_text, (window_width * 0.1 , window_height * 0.85))
    screen.blit(high_score_text, (window_width * 0.1 , window_height * 0.9))

# i = y, j = x
def draw_block(game_board: list, block: str, colors: dict) -> None:
    block_color = colors[block]
    for i in range(20):
        for j in range(10):
            if game_board[i][j] == 1:
                
                pg.draw.rect(screen, block_color, [window_width * 0.1 + window_width * 0.8 / game_board.shape[1] * j,
                                                    window_height * 0.8 / game_board.shape[0] * i,
                                                    window_width * 0.8 / game_board.shape[1],
                                                    window_height * 0.8 / game_board.shape[0]], border_radius=3
                            )
                pg.draw.rect(screen, "black", [window_width * 0.1 + window_width * 0.8 / game_board.shape[1] * j,
                                                    window_height * 0.8 / game_board.shape[0] * i,
                                                    window_width * 0.8 / game_board.shape[1],
                                                    window_height * 0.8 / game_board.shape[0]], 3, border_radius=3
                            )
                

# i = y, j = x
def create_tetris_block(game_board: list, block_type: dict) -> list:
    block = random.choice(tuple(block_type.keys()))
    block_position = deepcopy(block_type_spawn[block])
    for i in range(20):
        for j in range(10):
            if [i, j] in block_position:
                game_board[i][j] = 1
    return game_board, block, block_position

def move_block(game_board: list, block_position: tuple , direction: str) -> list:
    if direction == "LEFT":
        if min([row[1] for row in block_position]) != 0: 
            for x in block_position:
                x[1] -= 1
    elif direction == "RIGHT":
        if max([row[1] for row in block_position]) != 9:
            for x in block_position:
                x[1] += 1
    elif direction == "DOWN":
        if max([row[0] for row in block_position]) != 19:
            for y in block_position:
                y[0] += 1
    #Малюємо Ігрове поле
    for i in range(20):
        for j in range(10):
            if [i, j] in block_position:
                game_board[i][j] = 1
            elif not game_board_mask[i][j]:
                game_board[i][j] = 0
    return game_board, block_position
    

#Вводимо константи
window_width = 400
window_height = 600
FPS = 15
game_board = np.zeros((20, 10))
game_board_mask = np.zeros((20, 10))

score = 0
hight_score = 0

#Вказуємо URL
icon_image_url = "images\\Tetris_icon\\icons-32.png"

#ініціалізація гри
pg.init()

#Створення екрану
screen = pg.display.set_mode((window_width, window_height), pg.RESIZABLE | pg.HWSURFACE)
pg.display.set_caption("Tetris")
icon = pg.image.load(icon_image_url)
pg.display.set_icon(icon)

#Кольри
colors = {
    "bg": (255, 255, 255),
    "board": (92, 105, 95),
    "board_button": (56, 64, 58),
    "board_button_text": (243, 245, 206),
    "squere": (151, 0, 72),
    "t": (84, 164, 122),
    "I": (255, 255, 51),
    "s": (245, 215, 66),
    "z": (245, 66, 93),
    "l": (90, 66, 245),
}

#блоки для гри
block_type_spawn = {
    "squere": ([0, 4], [0, 5], [1, 4], [1, 5]),
    "t": ([0, 4], [0, 5], [0, 6], [1, 5]),
    "I": ([0, 4], [1, 4], [2, 4], [3, 4]),
    "s": ([0, 4], [1, 4], [1, 5], [2, 5]),
    "z": ([0, 5], [1, 5], [1, 4], [2, 4]),
    "l": ([0, 4], [0, 5], [0, 6], [1, 6]),
}

#Добавляємо час
clock = pg.time.Clock()

#Створення флагів
run = True
spawn_block = True
direction = ""
while run:
    # Отримуємо розмір вікна
    window_width, window_height = screen.get_size()
    draw_board(window_width, window_height, score)

    #Обобляємо подій
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                run = False
            elif event.key == pg.K_LEFT:
                direction = "LEFT"
            elif event.key == pg.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pg.K_DOWN:
                direction = "DOWN"

    if spawn_block:
        game_board, block, block_position = create_tetris_block(game_board, block_type_spawn)
        spawn_block = False

    if direction:
        game_board, block_position = move_block(game_board, block_position, direction)
        direction = ""

    if max([row[0] for row in block_position]) == 19 or \
    (element for row in game_board for element in row) == (element for row in game_board_mask for element in row):
        for i in range(20):
            for j in range(10):
                if game_board[i][j] == 1:
                    game_board_mask[i][j] = 1
        spawn_block = True     

    draw_block(game_board, block, colors=colors)


    
    pg.display.update()
    clock.tick(FPS)
pg.quit()
