import time

import game

from typing import Tuple

import pygame


def create_window(grid_size: Tuple):
    screen = pygame.display.set_mode(grid_size)
    pygame.display.set_caption('Game of life')

    return screen


def game_loop(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            setup_key_events(screen, event)
        if game_state == 'simulation':
            game_of_life.update_grid()
            pygame.time.delay(200)

        display_grid(screen)
        pygame.display.flip()


def setup_key_events(screen, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            global game_state
            if game_state == 'setup':
                game_state = 'simulation'
            else:
                game_state = 'setup'


    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:
            game.set_cell_living(mouse_pos[0], mouse_pos[1], game_of_life.grid)
        elif event.button == 3:
            game.set_cell_dead(mouse_pos[0], mouse_pos[1], game_of_life.grid)


def display_grid(screen):
    for row_index in range(grid_size[0]):
        for col_index in range(grid_size[1]):
            if game_of_life.grid[row_index][col_index] == 1:
                draw_living_cell(screen, (row_index, col_index))
            else:
                draw_dead_cell(screen, (row_index, col_index))


def draw_living_cell(screen, position: Tuple):
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(position[0], position[1], 1, 1))


def draw_dead_cell(screen, position: Tuple):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(position[0], position[1], 1, 1))


game_state = 'setup'
grid_size = (200, 100)

game_of_life = game.GameOfLife(grid_size)

screen = create_window(grid_size)
game_loop(screen)
