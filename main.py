import sys
import time
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

REQUIRED_PRECISION = 0.0004
LOWER_LEFT_OF_RESTRICTED_AREA = 24
UPPER_RIGHT_OF_RESTRICTED_AREA = 30
LOW_BOUNDARY_RANDOM_DATA_VALUES = 20
HIGH_BOUNDARY_RANDOM_DATA_VALUES = 250
SHOULD_PRINT = False


def initialize_grid(size: int, max_change: float, min_charge: float, should_add_random_noise=True,) -> np.ndarray:
    """
    Initialize the grid with a central hot spot.
        :param min_charge: The initial charge of the rest of the grid.
        :param max_change: The initial charge of the hot spot.
        :param size: The size of the grid (size x size).
        :param should_add_random_noise:

    :return:
        np.ndarray: Initialized grid.

    """
    grid = (np.random.randint(low=LOW_BOUNDARY_RANDOM_DATA_VALUES, high=HIGH_BOUNDARY_RANDOM_DATA_VALUES, size=(size, size)) if should_add_random_noise else np.ones((size, size)) * min_charge)
    grid[LOWER_LEFT_OF_RESTRICTED_AREA:UPPER_RIGHT_OF_RESTRICTED_AREA, LOWER_LEFT_OF_RESTRICTED_AREA:
                                                                       UPPER_RIGHT_OF_RESTRICTED_AREA] = max_change

    return grid


def check_if_point_is_in_restricted_area(row: int, col: int) -> bool:
    return (LOWER_LEFT_OF_RESTRICTED_AREA <= row < UPPER_RIGHT_OF_RESTRICTED_AREA
            and LOWER_LEFT_OF_RESTRICTED_AREA <= col < UPPER_RIGHT_OF_RESTRICTED_AREA)


def custom_print(*params) -> None:
    if SHOULD_PRINT:
        print(params)


def apply_quarter_grid_calculation_to_rest_of_the_grid(grid) -> np.ndarray:
    new_grid = grid.copy()
    size = grid.shape[0]
    for row in range(1, size // 2 + 1):
        for col in range(1, size // 2 + 1):
            if True:
                current_charge = new_grid[row, col]
                custom_print(row, col)
                new_grid[size - row - 1, col] = current_charge
                custom_print(size - row - 1, col)
                new_grid[row, size - col - 1] = current_charge
                custom_print(row, size - col - 1)
                new_grid[size - row - 1, size - col - 1] = current_charge
                custom_print(size - row - 1, size - col - 1)
                custom_print("*"*10)
    return new_grid


def update_grid(grid: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Update the grid charges using the relaxation method.

    Args:
        grid (np.ndarray): The current grid.

    Returns:
        tuple[np.ndarray, float]: Updated grid and the maximum ratio of charge differences.
    """
    new_grid = grid.copy()
    size = grid.shape[0]
    min_ratio_diff_in_charge = -np.inf
    for row in range(0, size // 2 + 1):
        for col in range(0, size // 2+1):
            if not check_if_point_is_in_restricted_area(row, col):
                new_charge = calculate_charge_change(col, grid, row)
                min_ratio_diff_in_charge = max(save_divide(new_charge - float(new_grid[row, col]),
                                                           float(new_grid[row, col])), min_ratio_diff_in_charge)
                new_grid[row, col] = new_charge
            custom_print(row, col)
    new_grid = apply_quarter_grid_calculation_to_rest_of_the_grid(new_grid)
    return new_grid, min_ratio_diff_in_charge


def save_divide(divisor: float, divider: float) -> float:
    return divisor / divider if divider != 0 else np.inf


def calculate_charge_change(col: int, grid: np.ndarray, row: int) -> float:
    """
    Calculate the new charge for a specific cell.

    Args:
        col (int): Column index of the cell.
        grid (np.ndarray): The current grid.
        row (int): Row index of the cell.

    Returns:
        float: New charge of the cell.
    """
    return float(grid[row - 1, col] + grid[row, col + 1] + grid[row, col - 1] + grid[row + 1, col]) / 4


def simulate_charge_diffusion(size: int, max_change: float, min_charge: float) \
        -> list[np.ndarray]:
    """
    Simulate charge diffusion until equilibrium is reached.

    Args:
        size (int): The size of the grid (size x size).
        max_change (float): The initial charge of the hot spot.
        min_charge (float): The initial charge of the rest of the grid.

    Returns:
        list[np.ndarray]: List of grids at each time step.
    """
    grid = initialize_grid(size, max_change, min_charge)
    grid_list = [grid.copy()]
    min_ratio_diff_in_charge = np.inf
    while REQUIRED_PRECISION * 100 < abs(min_ratio_diff_in_charge):
        grid, min_ratio_diff_in_charge = update_grid(grid)
        grid_list.append(grid.copy())
    return grid_list


def animate_heat_diffusion(grid_list: list[np.ndarray], interval) -> None:
    """
    Animate the heat diffusion process.

    Args:
        grid_list (list[np.ndarray]): List of grids at each time step.
        :param grid_list:
        :param interval:
    """
    fig, ax = plt.subplots()
    cax = ax.matshow(grid_list[0], cmap='hot')
    fig.colorbar(cax)

    def update(frame: int):
        cax.set_data(grid_list[frame])
        return cax,

    ani = animation.FuncAnimation(fig, update, frames=len(grid_list), interval=interval, blit=True)
    plt.show()


def main():
    # Run the simulation
    grids = simulate_charge_diffusion(*get_inputs())
    # Animate the simulation
    animate_heat_diffusion(grids, interval=100)  # Adjust interval to slow down transitions


def get_inputs() -> Tuple:
    try:
        size = sys.argv[1]
        max_temp = sys.argv[2]
        min_temp = sys.argv[3]
        print(f" Values are {size=}, {max_temp=}, {min_temp=}")
        return int(size), float(max_temp), float(min_temp)
    except IndexError:
        print("No values were set")
        time.sleep(5)
        return 53, 1000, 1


if __name__ == "__main__":
    main()