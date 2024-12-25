import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from raw_data.calculate_std_from_baseline import calculate_std_for_baseline

# Function to process the Excel file
QUARTER_WAVE = "quarter_wave"
HALF_WAVE = "half_wave"


def modify_errorbars(angles, averages):
    error_bars = []
    for angle in angles:
        angle1 = (angle/360*2*np.pi)
        two_degrees_in_rad = (2 / 360 * 2 * np.pi)
        if angle1 < np.pi/2:
            error_bars.append(np.cos(angle1) ** 2 / np.cos(angle1 + two_degrees_in_rad) ** 2)
        else:
            error_bars.append(np.cos(angle1 + two_degrees_in_rad) ** 2 / np.cos(angle1) ** 2)
    print(np.array(error_bars) * np.array(averages) - averages)
    return abs(np.array(averages)*1.0278) - np.array(averages)


def plot_current_with_errorbars(file_path, exp_type_):
    angles = []
    averages = []
    plt.rcParams['font.size'] = 16  # Set default size
    error_bars = [[], []]  # Two rows: lower and upper errors
    base_path_ = file_path
    for file_ in os.listdir(base_path_):
        try:
            int(file_[:file_.find(".")])
        except ValueError:
            print(f"Could not parse as number the file name {file_}")
            continue
        file_path = base_path_ + file_
        frequency = os.path.splitext(os.path.basename(file_path))[0]  # File name without extension

        data = pd.read_excel(file_path, skiprows=5)

        # Ensure the data is clean and the relevant columns exist
        if 'Current (A)' not in data.columns:
            raise ValueError("Expected column 'Current (A)' not found in the Excel file.")

        # Calculate statistics for current
        avg_current = data['Current (A)'].mean()
        min_current = data['Current (A)'].min()
        max_current = data['Current (A)'].max()

        # Prepare data for plotting
        if float(frequency) < 90:
            angles += [float(frequency) + 90]  # Single frequency as a list
        else:
            angles += [float(frequency) - 90]  # Single frequency as a list
        averages += [avg_current]
        error_bars[0].append(avg_current - min_current)  # Lower error
        error_bars[1].append(max_current - avg_current)  # Upper error
        # Plotting
    if exp_type_ == HALF_WAVE:
        error_bars = modify_errorbars(angles=angles, averages=averages)
    print(len(averages), len(error_bars))
    plt.errorbar(angles, averages, yerr=error_bars, xerr=float(2), markersize=2,
                 fmt='o', color=COLOR_MAP[exp_type_])

    plt.xlabel('Angle (deg)')
    plt.ylabel('I (A)')
    plt.ylim(0, max(averages)*1.1)
    plt.legend()
    plt.grid(True)

    if exp_type_ == QUARTER_WAVE:
        calculate_fit(angles=angles, averages=averages)


def calculate_fit(angles, averages):
    # Data example
    x = angles  # Replace with your actual x-axis data
    y = averages  # Replace with your actual y-axis data

    # Compute linear fit
    coefficients = np.polyfit(x, y, 0)  # Linear fit (degree=1)
    from raw_data.calculate_std_from_baseline import calculate_std_for_baseline
    std_for_baseline = calculate_std_for_baseline()
    upper_bound = (1 + std_for_baseline)
    lower_bound = (1 - std_for_baseline)
    fit_equation = (f"y = {coefficients[0]:.3e}, "
                    f"y_s = {coefficients[0] * upper_bound:.3e}, "
                    f"y_i = {coefficients[0] * lower_bound:.3e}")
    plt.plot(x,
             [coefficients.mean() for _ in range(len(x))],
             color='red',
             linestyle='--',
             label=f"y = {coefficients[0]:.3e}")
    plt.plot(x,
             [coefficients.mean() * upper_bound for _ in range(len(x))],
             color='blue',
             linestyle='--',
             alpha=0.5,
             label=f"y_s = {coefficients[0] * upper_bound:.3e}")
    plt.plot(x,
             [coefficients.mean() * lower_bound for _ in range(len(x))],
             color='blue',
             linestyle='--',
             alpha=0.5,
             label=f"y_s = {coefficients[0] * lower_bound:.3e}")
    plt.legend()


COLOR_MAP = {HALF_WAVE: "blue", QUARTER_WAVE: "green"}
for exp_type in [HALF_WAVE, QUARTER_WAVE]:
    base_path = f"../week_2/raw_data/{exp_type}/"
    plot_current_with_errorbars(base_path, exp_type)
    plt.show()
