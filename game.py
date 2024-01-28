from typing import Tuple, List


def set_cell_living(x, y, grid_copy):
    grid_copy[x][y] = 1


def set_cell_dead(x, y, grid_copy):
    grid_copy[x][y] = 0


class GameOfLife:
    def __init__(self, size: Tuple, mode: Tuple[List[int], List[int]]):
        self.mode = mode
        self.grid = [[0] * size[1] for row in range(size[0])]
        self.grid_size = size

    def set_grid(self, grid: List[List[int]]):
        self.grid = grid
        self.grid_size = (len(grid), len(grid[0]))

    def set_mode(self, mode: Tuple[List[int], List[int]]):
        self.mode = mode

    def display_grid(self):
        for row in self.grid:
            for col in row:
                print(f'{col} ', end='')
            print('')
        print('')

    def update_grid(self):
        grid_copy = self.get_copy()
        for row_index in range(len(self.grid)):
            for col_index in range(len(self.grid[row_index])):
                if self.grid[row_index][col_index] == 1:
                    self.handle_living_cell(row_index, col_index, grid_copy)
                else:
                    self.handle_dead_cell(row_index, col_index, grid_copy)
        self.grid = grid_copy.copy()

    def get_copy(self):
        return [[col for col in row] for row in self.grid]

    def handle_living_cell(self, row_index, col_index, grid_copy):
        living_neighbours = self.get_living_neighbours_count(row_index, col_index)

        if living_neighbours not in self.mode[0]:
            set_cell_dead(row_index, col_index, grid_copy)

    def handle_dead_cell(self, row_index, col_index, grid_copy):
        living_neighbours = self.get_living_neighbours_count(row_index, col_index)

        if living_neighbours in self.mode[1]:
            set_cell_living(row_index, col_index, grid_copy)

    def get_living_neighbours_count(self, row_index, col_index):
        living_neighbours = 0

        living_neighbours += self.check_cell_state(row_index, col_index - 1)
        living_neighbours += self.check_cell_state(row_index, col_index + 1)
        living_neighbours += self.check_cell_state(row_index - 1, col_index)
        living_neighbours += self.check_cell_state(row_index + 1, col_index)

        living_neighbours += self.check_cell_state(row_index - 1, col_index - 1)
        living_neighbours += self.check_cell_state(row_index - 1, col_index + 1)
        living_neighbours += self.check_cell_state(row_index + 1, col_index - 1)
        living_neighbours += self.check_cell_state(row_index + 1, col_index + 1)

        return living_neighbours

    def check_cell_state(self, row_index, col_index):
        if row_index < 0 or row_index >= self.grid_size[0]:
            return 0

        if col_index < 0 or col_index >= self.grid_size[1]:
            return 0

        return self.grid[row_index][col_index]