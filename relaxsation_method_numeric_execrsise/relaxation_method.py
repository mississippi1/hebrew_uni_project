from typing import Union
import numpy as np
from matplotlib import pyplot as plt, animation
from numba import jit

LENGTH_OF_GRID = 500
WIDTH_OF_GRID = 200
REQUIRED_PRECISION = 0.4
BASE_DISK_HEIGHT = 20
LOWER_Y_OF_DISK = BASE_DISK_HEIGHT
UPPER_Y_OF_DISK = BASE_DISK_HEIGHT + 1
LOWER_X_OF_DISK = 0
UPPER_X_OF_DISK = 400
POTENTIAL_AT_DISK = 0.5
STEP_SIZE = 0.5

ALLOWED_TO_PRINT = False


def custom_print(*args):
    if ALLOWED_TO_PRINT:
        print(*args)


def initialize_grid(length_input: int, width_input: int, max_change: float) -> np.ndarray:
    """
    Initialize the grid with a central hot spot.
        :param max_change: The initial charge of the hot spot.
        :param length_input: The size of the grid (size x size).
        :param width_input: The size of the grid (size x size).

    :return:
        np.ndarray: Initialized grid.

    """
    grid = (np.zeros(
        shape=(length_input, width_input)))
    grid[LOWER_X_OF_DISK: UPPER_X_OF_DISK, LOWER_Y_OF_DISK: UPPER_Y_OF_DISK, ] = max_change
    return grid


def is_allowed_area(x, y) -> bool:
    # Todo: should split to two fore each dosk
    is_allowed = (y < LOWER_Y_OF_DISK or UPPER_Y_OF_DISK < y or x < LOWER_X_OF_DISK or UPPER_X_OF_DISK < x)
    return is_allowed


def get_potential_from_neighbor(row, column, grid):
    #         Todo: should split for each dosk
    if not is_allowed_area(y=column, x=row):
        return POTENTIAL_AT_DISK
    elif is_outside(column=column, row=row):
        return 0
    else:
        return grid[row, column]


def is_outside(column, row):
    return row < 0 or row >= WIDTH_OF_GRID or column < 0 or column >= LENGTH_OF_GRID


def calculate_potential(row, column, step_size, grid):
    calculated_potential = 1 / 4 * (
            get_potential_from_neighbor(row + 1, column, grid) * (1 + step_size / (2 * row))
            + get_potential_from_neighbor(row - 1, column, grid) * (1 - step_size / (2 * row))
            + get_potential_from_neighbor(row, column + 1, grid)
            + get_potential_from_neighbor(row, column + 1, grid))
    return calculated_potential


def update_potential(grid: np.array) -> Union[np.array, float]:
    new_grid = grid.copy()
    max_diff_between_last_value_and_new = 0
    counter = 0
    for row in range(1, LENGTH_OF_GRID):
        for column in range(1, WIDTH_OF_GRID):
            if is_allowed_area(x=row, y=column) and not is_outside(column=column, row=row):
                counter += 1
                custom_print(row, column)
                new_value = calculate_potential(row=row, column=column, step_size=STEP_SIZE, grid=grid)
                new_grid[row, column] = new_value
                abs(new_grid[row, column] - new_value) / new_value
                max_diff_between_last_value_and_new = max(max_diff_between_last_value_and_new,
                                                          abs(new_grid[row, column] - new_value) / new_value)
    custom_print(max_diff_between_last_value_and_new)
    return new_grid, max_diff_between_last_value_and_new


def animate_heat_diffusion(grid_list: list[np.ndarray], interval) -> None:
    """
    Animate the heat diffusion process.

    Args:
        grid_list (list[np.ndarray]): List of grids at each time step.
        :param grid_list:
        :param interval:
    """
    fig, ax = plt.subplots()
    cax = ax.matshow(grid_list[0], cmap='hot', origin="lower")
    fig.colorbar(cax)
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_label_position('bottom')

    def update(frame: int):
        cax.set_data(grid_list[frame])
        return cax,

    ani = animation.FuncAnimation(fig, update, frames=len(grid_list), interval=interval, blit=True)
    plt.show()


def main():
    grid = initialize_grid(WIDTH_OF_GRID, LENGTH_OF_GRID, POTENTIAL_AT_DISK)
    max_diff_between_last_value_and_new = 1
    grid_list = [grid.copy()]
    counter = 1
    while REQUIRED_PRECISION < max_diff_between_last_value_and_new or counter < 100:
        counter += 1
        grid, max_diff_between_last_value_and_new = update_potential(grid=grid)
        grid_list.append(grid.copy())
    print(grid)
    animate_heat_diffusion(grid_list=grid_list, interval=20)  # Adjust interval to slow down transitions


if __name__ == "__main__":
    main()
