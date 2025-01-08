import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from raw_data.calculate_std_from_baseline import calculate_std_for_baseline

# Constants and Settings
QUARTER_WAVE = "quarter_wave"
HALF_WAVE = "half_wave"
COLOR_MAP = {HALF_WAVE: "blue", QUARTER_WAVE: "green"}
plt.rcParams['font.size'] = 12  # Set default size


def modify_errorbars(angles, averages):
    error_bars = []
    for angle in angles:
        angle1 = (angle / 360 * 2 * np.pi)
        two_degrees_in_rad = (2 / 360 * 2 * np.pi)
        if angle1 < np.pi / 2:
            error_bars.append(np.cos(angle1) ** 2 / np.cos(angle1 + two_degrees_in_rad) ** 2)
        else:
            error_bars.append(np.cos(angle1 + two_degrees_in_rad) ** 2 / np.cos(angle1) ** 2)
    return abs(np.array(averages) * 1.0278) - np.array(averages)


def calculate_fit(angles, averages, ax: plt.Axes):
    x = angles
    y = averages
    coefficients = np.polyfit(x, y, 0)
    std_for_baseline = calculate_std_for_baseline()
    upper_bound = (1 + std_for_baseline)
    lower_bound = (1 - std_for_baseline)
    ax.set_ylim(0, 0.1)
    ax.plot(x, [coefficients.mean() for _ in range(len(x))],
             color='red', linestyle='--', label=f"y = {coefficients[0]:.3e}")
    ax.plot(x, [coefficients.mean() * upper_bound for _ in range(len(x))],
             color='blue', linestyle='--', alpha=0.5, label=f"y_s = {coefficients[0] * upper_bound:.3e}")
    ax.plot(x, [coefficients.mean() * lower_bound for _ in range(len(x))],
             color='blue', linestyle='--', alpha=0.5, label=f"y_s = {coefficients[0] * lower_bound:.3e}")
    ax.legend()


def plot_current_with_errorbars(file_path, exp_type_, ax):
    angles = []
    averages = []
    error_bars = [[], []]

    for file_ in os.listdir(file_path):
        try:
            int(file_[:file_.find(".")])
        except ValueError:
            print(f"Could not parse as number the file name {file_}")
            continue

        data = pd.read_excel(file_path + file_, skiprows=5)

        if 'Current (A)' not in data.columns:
            raise ValueError("Expected column 'Current (A)' not found in the Excel file.")

        avg_current = data['Current (A)'].mean() * 1000
        min_current = data['Current (A)'].min() * 1000
        max_current = data['Current (A)'].max() * 1000

        frequency = os.path.splitext(os.path.basename(file_path + file_))[0]
        if float(frequency) < 90:
            angles += [float(frequency) + 90]
        else:
            angles += [float(frequency) - 90]
        averages += [avg_current]
        error_bars[0].append(avg_current - min_current)
        error_bars[1].append(max_current - avg_current)

    if exp_type_ == HALF_WAVE:
        error_bars = modify_errorbars(angles=angles, averages=averages)

    ax.errorbar(angles, averages, yerr=error_bars, xerr=float(2), markersize=2,
                fmt='o', color=COLOR_MAP[exp_type_],
                # label=exp_type_
                )
    ax.set_xlabel('Angle (deg)')
    ax.set_ylabel('I (mA)')
    ax.grid(True)

    if exp_type_ == QUARTER_WAVE:
        calculate_fit(angles=angles, averages=averages, ax=ax)


def plot_polar_current(file_path, exp_type_, ax):
    angles = []
    averages = []

    for file_ in os.listdir(file_path):
        try:
            int(file_[:file_.find(".")])
        except ValueError:
            print(f"Could not parse as number the file name {file_}")
            continue

        data = pd.read_excel(file_path + file_, skiprows=5)

        if 'Current (A)' not in data.columns:
            raise ValueError("Expected column 'Current (A)' not found in the Excel file.")

        avg_current = data['Current (A)'].mean()
        frequency = os.path.splitext(os.path.basename(file_path + file_))[0]
        if float(frequency) < 90:
            angles += [float(frequency) + 90]
        else:
            angles += [float(frequency) - 90]
        averages += [avg_current]

    angles_rad = np.deg2rad(np.array(angles))
    radius = np.array(averages)
    ax.scatter(angles_rad, radius, color=COLOR_MAP[exp_type_], label=exp_type_)
    ax.set_theta_zero_location('E')
    ax.set_theta_direction(1)
    ax.legend()


# Main Execution
fig, axs = plt.subplots(1, 2, figsize=(14, 7))  # 1 row, 2 columns

base_paths = {
    HALF_WAVE: "../week_2/raw_data/half_wave/",
    QUARTER_WAVE: "../week_2/raw_data/quarter_wave/"
}

path_options = [QUARTER_WAVE]  # Add QUARTER_WAVE if needed

# Plot Error Bars on the Left
for exp_type in path_options:
    plot_current_with_errorbars(base_paths[exp_type], exp_type, axs[0])

# Plot Polar Graph on the Right
axs[1] = plt.subplot(122, projection='polar')  # Polar plot on the right
for exp_type in path_options:
    plot_polar_current(base_paths[exp_type], exp_type, axs[1])

plt.tight_layout()
plt.show()
