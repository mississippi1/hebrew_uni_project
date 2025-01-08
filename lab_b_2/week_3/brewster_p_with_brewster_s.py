import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from raw_data.calculate_std_from_baseline import calculate_std_for_baseline

def modify_errorbars(angles, averages):
    error_bars = []
    for angle in angles:
        angle1 = (angle/360*2*np.pi)
        two_degrees_in_rad = (2 / 360 * 2 * np.pi)
        if angle1 < np.pi/2:
            error_bars.append(np.cos(angle1) ** 2 / np.cos(angle1 + two_degrees_in_rad) ** 2)
        else:
            error_bars.append(np.cos(angle1 + two_degrees_in_rad) ** 2 / np.cos(angle1) ** 2)
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
        # if float(frequency) < 90:
        angles += [float(frequency)]  # Single frequency as a list
        # else:
        #     angles += [float(frequency) - 90]  # Single frequency as a list
        averages += [avg_current]
        error_bars[0].append(avg_current - min_current)  # Lower error
        error_bars[1].append(max_current - avg_current)  # Upper error
        # Plotting

    plt.xlabel('Angle (deg)')
    plt.ylabel('I (A)')
    plt.ylim(0, max(averages)*1.1)
    plt.legend()
    plt.grid(True)
    plt.errorbar(angles, averages, yerr=error_bars, xerr=float(1), markersize=2,
                 fmt='o', color=COLOR_MAP[exp_type_])
    return angles


def get_rp_prediction(angles, baseline_light_power, n2):
    angles_in_rad = sorted(np.array(angles) / 360 * 2 * np.pi)
    nominator = (n2 * np.cos(angles_in_rad) - np.sqrt(1 - (np.sin(angles_in_rad) / n2) ** 2))
    denominator = (n2 * np.cos(angles_in_rad) + np.sqrt(1 - (np.sin(angles_in_rad) / n2) ** 2))
    expected_values = (nominator / denominator) ** 2 * baseline_light_power
    return expected_values


def get_rs_prediction(angles, baseline_light_power, n2):
    angles_in_rad = sorted(np.array(angles) / 360 * 2 * np.pi)
    nominator = (np.cos(angles_in_rad) - n2 * np.sqrt(1 - (np.sin(angles_in_rad) / n2) ** 2))
    denominator = (np.cos(angles_in_rad) + n2 * np.sqrt(1 - (np.sin(angles_in_rad) / n2) ** 2))
    expected_values = (nominator / denominator) ** 2 * baseline_light_power
    return expected_values


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


COLOR_MAP = {"brewster_p": "blue", "brewster_s": "green"}
for exp_type in ["brewster_p", "brewster_s"]:
    base_path = f"raw_data/{exp_type}/"
    print(base_path)
    angles_ = plot_current_with_errorbars(base_path, exp_type)

for n2 in [143, 147, 151]:
    n2 = n2/100
    baseline_light_power = 9.44*10**-5
    rp_prediction = get_rp_prediction(angles_, baseline_light_power, n2)
    rs_prediction = get_rs_prediction(angles_, baseline_light_power, n2)
    if n2 == 1.47:
        plt.plot(sorted(angles_), rp_prediction, label=f"Reflected Intensity P - {n2}")
    plt.plot(sorted(angles_), rs_prediction, label=f"Reflected Intensity S - {n2}")
    plt.legend()
plt.show()
