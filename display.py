import math

import game

from typing import Tuple

import pygame
import pygame.freetype

CELL_SIZE = 15
UPDATE_INTERVAL = 200
FONT = None
CURRENT_MODE = 'game_of_life'

MACRO_1 = [[]]

def create_window(grid_size: Tuple):
    grid_size = (grid_size[0] * CELL_SIZE, grid_size[1] * CELL_SIZE)
    screen = pygame.display.set_mode(grid_size)
    pygame.display.set_caption('The Game of Life')
    pygame.font.init()
    global FONT
    FONT = pygame.font.SysFont('Comic Sans MS', 30)

    return screen


def game_loop(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            key_events(screen, event)
        if game_state == 'simulation':
            game_of_life.update_grid()
            pygame.time.delay(UPDATE_INTERVAL)

        display_grid(screen)
        display_text(screen, f'Tick interval: {UPDATE_INTERVAL}ms', (10, 0))
        display_text(screen, f'Game state: {game_state}', (10, 30))
        display_text(screen, f'Current mode: {CURRENT_MODE}', (10, 60))
        pygame.display.flip()


def display_text(screen, text, pos):
    text_surface = FONT.render(text, False, (255, 255, 255))
    screen.blit(text_surface, pos)


def key_events(screen, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            global game_state
            if game_state == 'setup':
                game_state = 'simulation'
            else:
                game_state = 'setup'

        if event.key == pygame.K_1:
            set_mode('game_of_life')

        if event.key == pygame.K_2:
            set_mode('cities')

        if event.key == pygame.K_3:
            set_mode('labyrinth')

        if event.key == pygame.K_4:
            set_mode('coral')

        if event.key == pygame.K_5:
            set_mode('seed')

        if event.key == pygame.K_r:
            global game_of_life
            game_of_life = game.GameOfLife(grid_size, modes[CURRENT_MODE])

        if event.key == pygame.K_KP1:
            global MACRO_1
            MACRO_1 = game_of_life.get_copy()

        if event.key == pygame.K_KP2 and MACRO_1 != [[]]:
            game_of_life.set_grid([[col for col in row] for row in MACRO_1])

    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (math.floor(mouse_pos[0] / CELL_SIZE), math.floor(mouse_pos[1] / CELL_SIZE))
        if event.button == 1:
            game.set_cell_living(mouse_pos[0], mouse_pos[1], game_of_life.grid)
        elif event.button == 3:
            game.set_cell_dead(mouse_pos[0], mouse_pos[1], game_of_life.grid)

    if event.type == pygame.MOUSEWHEEL:
        global UPDATE_INTERVAL
        UPDATE_INTERVAL += event.y * 10


def set_mode(mode):
    global CURRENT_MODE
    CURRENT_MODE = mode

    game_of_life.set_mode(modes[mode])


def display_grid(screen):
    for row_index in range(grid_size[0]):
        for col_index in range(grid_size[1]):
            if game_of_life.grid[row_index][col_index] == 1:
                draw_living_cell(screen, (row_index, col_index))
            else:
                draw_dead_cell(screen, (row_index, col_index))


def draw_living_cell(screen, position: Tuple):
    pygame.draw.rect(screen, (255, 255, 255),
                     pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_dead_cell(screen, position: Tuple):
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


game_state = 'setup'
grid_size = (50, 50)

modes = {
    'game_of_life': ([2, 3], [3]),
    'cities': ([2, 3, 4, 5], [4, 5, 6, 7, 8]),
    'labyrinth': ([1, 2, 3, 4, 5], [3]),
    'coral': ([4, 5, 6, 7, 8], [3]),
    'seed': ([], [2])
}

game_of_life = game.GameOfLife(grid_size, modes['game_of_life'])

screen = create_window(grid_size)
game_loop(screen)
