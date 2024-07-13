import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from numba import jit
import matplotlib.animation as animation

# Parameters
GRID_LENGTH = 500
GRID_WIDTH = 200
STEP_SIZE = 0.025
REQUIRED_PRECISION = 0.0001
MAX_ITERATIONS = 10_000
TOP_PLATE_POTENTIAL = -0.5
BOTTOM_PLATE_POTENTIAL = 0.5
PLATE_OFFSET = 20
X_MAX_OF_DISK = 400

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
        grid = np.zeros((self.length + 1, 2 * self.width + 1))
        grid[:X_MAX_OF_DISK, self.width + self.plate_offset] = self.top_potential
        grid[:X_MAX_OF_DISK, self.width - self.plate_offset] = self.bottom_potential
        return grid

@jit(nopython=True)
def numba_relax_potential(grid, length, width, step_size, precision, max_iterations, plate_offset):
    grids = []
    for iteration in range(max_iterations):
        max_diff = 0
        new_grid = grid.copy()
        for x in range(1, length):
            for y in range(1, 2 * width):
                if (y == width + plate_offset or y == width - plate_offset) and x < 400:
                    continue
                new_grid[x, y] = 0.25 * (
                        grid[x + 1, y] * (1 + step_size / (2 * (x if x != 0 else 1))) +
                        grid[x - 1, y] * (1 - step_size / (2 * (x if x != 0 else 1))) +
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
        return numba_relax_potential(
            self.potential_grid.grid,
            self.potential_grid.length,
            self.potential_grid.width,
            self.potential_grid.step_size,
            self.precision,
            self.max_iterations,
            self.potential_grid.plate_offset
        )

class PotentialPlotter:
    def __init__(self, potential_grid, grids):
        self.potential_grid = potential_grid
        self.grids = grids

    def plot_potential(self):
        plt.figure(figsize=(12, 8))
        plt.title("Potential Distribution Around the Board Capacitor")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.gca().invert_yaxis()
        plt.imshow(
            self.potential_grid.grid.T,
            extent=[0, self.potential_grid.length, -self.potential_grid.width, self.potential_grid.width],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        plt.colorbar(label='Potential (V)')
        plt.show()

    def plot_negative_y_values(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        im = ax.imshow(
            self.potential_grid.grid[:, self.potential_grid.width:].T,
            extent=[0, self.potential_grid.length, 0, self.potential_grid.width - 300],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        ax.set_title("Potential Distribution for Negative y Values")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.colorbar(im, ax=ax, orientation='vertical', label='Potential (V)')
        plt.show()

    def plot_positive_y_values(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        im = ax.imshow(
            self.potential_grid.grid[:, :self.potential_grid.width].T,
            extent=[0, self.potential_grid.length, 0, self.potential_grid.width],
            cmap='hot',
            norm=mcolors.Normalize(vmin=-0.5, vmax=0.5)
        )
        ax.set_title("Potential Distribution for Positive y Values")
        ax.set_xlabel("r")
        ax.set_ylabel("z")
        plt.colorbar(im, ax=ax, orientation='vertical', label='Potential (V)')
        plt.show()

    def plot_vertical_line_at_x0(self):
        # Compute the y-values to match the grid's vertical axis
        y_values = np.linspace(-self.potential_grid.length, self.potential_grid.length, self.potential_grid.grid.shape[1])

        # Extract potential values from the grid at x = 0
        potential_values = self.potential_grid.grid[1, :]
        plt.figure(figsize=(12, 8))
        plt.plot(potential_values, y_values, label="Potential at x = 0", color='b')
        plt.title("Potential Distribution at x = 0")
        plt.xlabel("Potential (V)")
        plt.ylabel("y")
        plt.grid(True)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.show()

    def animate_potential(self):
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_title("Potential Distribution Around the Board Capacitor")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
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
        plt.show()

def main():
    potential_grid = PotentialGrid(
        GRID_LENGTH, GRID_WIDTH, STEP_SIZE, TOP_PLATE_POTENTIAL, BOTTOM_PLATE_POTENTIAL, PLATE_OFFSET
    )
    solver = RelaxationSolver(potential_grid, REQUIRED_PRECISION, MAX_ITERATIONS)
    print("Starting relaxation method...")
    grids = solver.relax_potential()
    print("Relaxation method completed.")
    plotter = PotentialPlotter(potential_grid, grids)
    plotter.plot_potential()
    plotter.plot_positive_y_values()
    plotter.plot_negative_y_values()
    plotter.plot_vertical_line_at_x0()  # Added line plot for x = 0
    plotter.animate_potential()
    print(potential_grid.grid[0::10])


if __name__ == "__main__":
    main()
