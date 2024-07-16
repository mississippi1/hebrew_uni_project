import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from numba import jit
import matplotlib.animation as animation
import pandas as pd

# Parameters
GRID_LENGTH = 0.125  # meters
GRID_WIDTH = 0.05  # meters
STEP_SIZE = 0.00025  # meters
REQUIRED_PRECISION = 0.0001
MAX_ITERATIONS = 999999999
TOP_PLATE_POTENTIAL = -0.5
BOTTOM_PLATE_POTENTIAL = 0.5
PLATE_OFFSET = 0.0025  # meters
X_MAX_OF_DISK = 0.1  # meters
EPSILON_ZERO = 8.854 * 10 ** -12


class PotentialGrid:
    def __init__(self, length, width, step_size, top_potential, bottom_potential, plate_offset):
        self.length = length
        self.width = width
        self.step_size = step_size
        self.top_potential = top_potential
        self.bottom_potential = bottom_potential
        self.plate_offset = plate_offset
        self.grid = self.initialize_grid()

    def initialize_grid(self):
        length_idx = int(self.length / self.step_size)
        width_idx = int(self.width / self.step_size)
        grid = np.zeros((length_idx + 1, 2 * width_idx + 1))

        top_plate_y = width_idx + int(self.plate_offset / self.step_size)
        bottom_plate_y = width_idx - int(self.plate_offset / self.step_size)

        grid[:int(X_MAX_OF_DISK / STEP_SIZE), top_plate_y] = self.top_potential
        grid[:int(X_MAX_OF_DISK / STEP_SIZE), bottom_plate_y] = self.bottom_potential
        return grid


@jit(nopython=True)
def numba_relax_potential(grid, length_idx, width_idx, step_size, precision, max_iterations, plate_offset_idx):
    grids = []
    for iteration in range(max_iterations):
        max_diff = 0
        new_grid = grid.copy()
        for x in range(0, length_idx):
            for y in range(1, 2 * width_idx):
                if (y == width_idx + plate_offset_idx or y == width_idx - plate_offset_idx) and x < int(
                        X_MAX_OF_DISK / step_size):
                    continue
                value_at_left_point = grid[x, y] * (1 + step_size / (2 * (x if x != 0 else 1)))
                if x != 0:
                    value_at_left_point = grid[x - 1, y] * (1 + step_size / (2 * (x if x != 0 else 1)))
                new_grid[x, y] = 0.25 * (
                        grid[x + 1, y] * (1 + step_size / (2 * (x if x != 0 else 1))) +
                        value_at_left_point +
                        grid[x, y + 1] +
                        grid[x, y - 1]
                )
                max_diff = max(max_diff, abs(new_grid[x, y] - grid[x, y]))
        grid[:] = new_grid
        grids.append(grid.copy())
        if max_diff < precision:
            print(f"Converged after {iteration + 1} iterations")
            break
    else:
        print("Did not converge within the maximum number of iterations")
    return grids


class RelaxationSolver:
    def __init__(self, potential_grid, precision, max_iterations):
        self.potential_grid = potential_grid
        self.precision = precision
        self.max_iterations = max_iterations

    def relax_potential(self):
        length_idx = int(self.potential_grid.length / self.potential_grid.step_size)
        width_idx = int(self.potential_grid.width / self.potential_grid.step_size)
        plate_offset_idx = int(self.potential_grid.plate_offset / self.potential_grid.step_size)
        return numba_relax_potential(
            self.potential_grid.grid,
            length_idx,
            width_idx,
            self.potential_grid.step_size,
            self.precision,
            self.max_iterations,
            plate_offset_idx
        )


def save_animation_as_different_file_format(ani):
    try:
        ani.save('potential_animation.gif', writer='pillow')
        print("Animation successfully saved as potential_animation.gif")
    except Exception as e:
        print(f"Failed to save GIF animation: {e}")

    try:
        ani.save('potential_animation.mp4', writer='ffmpeg')
        print("Animation successfully saved as potential_animation.mp4")
    except Exception as e:
        print(f"Failed to save MP4 animation: {e}")

    try:
        ani.save('potential_animation.mov', writer='ffmpeg')
        print("Animation successfully saved as potential_animation.mov")
    except Exception as e:
        print(f"Failed to save MOV animation: {e}")

    try:
        ani.save('potential_animation.avi', writer='ffmpeg')
        print("Animation successfully saved as potential_animation.avi")
    except Exception as e:
        print(f"Failed to save AVI animation: {e}")

    try:
        ani.save('potential_animation.html', writer='html')
        print("Animation successfully saved as potential_animation.html")
    except Exception as e:
        print(f"Failed to save HTML5 animation: {e}")


class PotentialPlotter:
    def __init__(self, potential_grid, grids):
        self.potential_grid = potential_grid
        self.grids = grids

    def plot_potential(self):
        plt.figure(figsize=(12, 8))
        plt.title("Potential Distribution Around the Board Capacitor")
        plt.xlabel("r (meters)")
        plt.ylabel("z (meters)")
        plt.gca().invert_yaxis()
        plt.imshow(
            self.potential_grid.grid.T,
            extent=[0, self.potential_grid.length, -self.potential_grid.width, self.potential_grid.width],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        plt.colorbar(label='Potential (V)')
        plt.savefig("Potential Distribution Around the Board Capacitor .png")
        plt.show()

    def plot_positive_y_values(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        im = ax.imshow(
            self.potential_grid.grid[:, int(self.potential_grid.width / self.potential_grid.step_size):].T,
            extent=[0, self.potential_grid.length, 0, self.potential_grid.width],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        ax.set_title("Potential Distribution for Positive y Values")
        ax.set_xlabel("r (meters)")
        ax.set_ylabel("z (meters)")
        ax.invert_yaxis()
        plt.colorbar(im, ax=ax, orientation='vertical', label='Potential (V)')
        plt.savefig("Potential Distribution for Positive y Values.png")
        plt.show()

    def plot_negative_y_values(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        im = ax.imshow(
            self.potential_grid.grid[:, :int(self.potential_grid.width / self.potential_grid.step_size)].T,
            extent=[0, self.potential_grid.length, -self.potential_grid.width, 0],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        ax.set_title("Potential Distribution for Negative y Values")
        ax.set_xlabel("r (meters)")
        ax.set_ylabel("z (meters)")
        ax.invert_yaxis()
        plt.colorbar(im, ax=ax, orientation='vertical', label='Potential (V)')
        plt.savefig("Potential Distribution for Negative y Values .png")
        plt.show()

    def plot_potential_line_at_x0(self):
        potential_values = self.potential_grid.grid[1, :]
        y_values = np.linspace(-self.potential_grid.width, self.potential_grid.width, len(potential_values))
        plt.figure(figsize=(12, 8))
        plt.plot(y_values, potential_values[::-1], label="Potential at x = 0", color='b', marker=".")
        electric_field_trend_line = (list(0 for _ in range(0, 190))
                          + list(200 * i * self.potential_grid.step_size for i in range(-10, 11))
                          + list(0 for _ in range(0, 190)))
        plt.plot(y_values, electric_field_trend_line, label="Trend Line for Electric Field")
        plt.title("Potential Distribution at x = 0")
        plt.ylabel("Potential (V)")
        plt.xlabel("y (meters)")
        plt.grid(True)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.show()

    def get_electric_field(self):
        charge_density = self.calculate_electric_field() * EPSILON_ZERO
        integral = 0
        charge_density.head(401).to_excel("electric_field.xlsx")
        for row_number in range(0, 401):
            charge_density_value = charge_density[row_number]
            radius = (row_number * self.potential_grid.step_size ** 2)
            integral += radius * 2 * np.pi * charge_density_value
        return f"step_size: " + str(self.potential_grid.step_size) + ". integral: " + str(integral)

    def calculate_electric_field(self):
        potential_values_for_electric_field = pd.DataFrame(self.potential_grid.grid[:, :])
        potential_values_for_electric_field.to_excel("raw_Data_2.xlsx")
        charge_density = (
                                 (potential_values_for_electric_field.iloc[:, 190]
                                  - potential_values_for_electric_field.iloc[:, 191]) / self.potential_grid.step_size
                         )
        return charge_density

    def animate_potential(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title("Potential Distribution Around the Board Capacitor")
        ax.set_xlabel("x (meters)")
        ax.set_ylabel("y (meters)")
        ax.invert_yaxis()

        im = ax.imshow(
            self.grids[0].T,
            extent=[0, self.potential_grid.length, -self.potential_grid.width, self.potential_grid.width],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        plt.colorbar(im, ax=ax, label='Potential (V)')

        def update(frame):
            im.set_data(self.grids[frame].T)
            return [im]

        ani = animation.FuncAnimation(fig, update, frames=len(self.grids), blit=True, interval=50)

        # save_animation_as_different_file_format(ani)

        plt.show()


def main():
    potential_grid = PotentialGrid(
        GRID_LENGTH, GRID_WIDTH, STEP_SIZE, TOP_PLATE_POTENTIAL, BOTTOM_PLATE_POTENTIAL, PLATE_OFFSET
    )
    solver = RelaxationSolver(potential_grid, REQUIRED_PRECISION, MAX_ITERATIONS)
    grids = solver.relax_potential()
    plotter = PotentialPlotter(potential_grid, grids)

    plotter.plot_potential()
    plotter.plot_positive_y_values()
    plotter.plot_negative_y_values()
    plotter.plot_potential_line_at_x0()
    plotter.animate_potential()


def calculate_integral_for_different_h():
    for h in [
        # STEP_SIZE / 2,
        STEP_SIZE,
        # STEP_SIZE * 2, STEP_SIZE * 4, STEP_SIZE * 8
            ]:
        potential_grid = PotentialGrid(
            GRID_LENGTH, GRID_WIDTH, h, TOP_PLATE_POTENTIAL, BOTTOM_PLATE_POTENTIAL, PLATE_OFFSET
        )
        solver = RelaxationSolver(potential_grid, REQUIRED_PRECISION, MAX_ITERATIONS)
        grids = solver.relax_potential()
        pd.DataFrame(grids[-1]).to_excel("raw_data.xlsx")
        plotter = PotentialPlotter(potential_grid, grids)
        print(plotter.plot_potential_line_at_x0())


if __name__ == "__main__":
    calculate_integral_for_different_h()
    main()
