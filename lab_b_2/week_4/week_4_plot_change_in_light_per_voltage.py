import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

EXPECTED_VERDET = 96.4

RESISTANCE = 11.38952164

NL_R = 15.2 * 10 ** -4
FIRST_EXPERIMENT = "first_experiment"
SECOND_EXPERIMENT = "second_experiment"
LENGTH = 23.5 * 10 ** -3


def modify_errorbars(angles, averages):
    error_bars = []
    for angle in angles:
        angle1 = (np.pi/2-angle / 360 * 2 * np.pi)
        two_degrees_in_rad = (2 / 360 * 2 * np.pi)
        if angle1 < np.pi / 2:
            error_bars.append(np.cos(angle1) ** 2 / np.cos(angle1 + two_degrees_in_rad) ** 2)
        else:
            error_bars.append(np.cos(angle1 + two_degrees_in_rad) ** 2 / np.cos(angle1) ** 2)
    return abs(np.array(averages) * 1.0278) - np.array(averages)


def plot_current_with_errorbars(file_path, exp_type_, axes):
    voltages = []
    averages = []
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
        avg_current = data['Current (A)'].mean() * 1_000
        min_current = data['Current (A)'].min() * 1_000
        max_current = data['Current (A)'].max() * 1_000
        # Prepare data for plotting

        voltages += [float(frequency)]  # Single frequency as a list
        averages += [avg_current]
        error_bars[0].append(avg_current - min_current)  # Lower error
        error_bars[1].append(max_current - avg_current)  # Upper error

    error_bars = modify_errorbars(angles=voltages, averages=averages)

    # Plot on the first subplot
    axes[0].errorbar(voltages, averages, yerr=error_bars, markersize=2,
                     fmt='o')
    axes[0].set_xlabel('Voltage (V)')
    axes[0].set_ylabel('I (mA)')
    axes[0].legend()
    axes[0].grid(True)

    pred = calculate_fit(
        theta=np.zeros(len(voltages)),
        voltages=np.array(voltages),
        mean_intensity=np.array(averages),
        baseline_intensity=107.88 * 10 ** -3
    )
    pred_no_inf = np.ma.masked_invalid(pred)
    ss_res = np.ma.masked_invalid((pred_no_inf - 96.4) ** 2).sum()
    ss_tot = np.ma.masked_invalid((np.array(pred_no_inf) - np.ma.masked_invalid(pred_no_inf).mean()) ** 2).sum()
    r_squared = 1 - (ss_res / ss_tot)

    axes[1].errorbar(
        x=voltages,
        y=pred,
        xerr=1*10**-2,
        yerr=2 * 2 * np.pi / 360 / (np.array(voltages) * NL_R * LENGTH),
        label=f"avg={np.ma.masked_invalid(pred).sum()/len(np.ma.masked_invalid(pred)):.3f}, r^2={r_squared}",
        fmt='o',
        markersize=6,
        linewidth=2,
        alpha=0.9,
        capsize=5
    )
    plt.plot(voltages, [EXPECTED_VERDET for _ in voltages], label=f"y={EXPECTED_VERDET}")
    axes[1].set_xlabel('Voltage (V)')
    axes[1].set_ylabel('Verdet Const. (Rad/(T*m))')
    axes[1].legend()
    axes[1].grid(True)
    # axes[1].set_title('Predicted Fit')


def calculate_fit(theta, voltages, mean_intensity, baseline_intensity):
    delta_theta = (np.pi/2-(1.015 + theta) / 360 * 2 * np.pi)
    arccos_val = np.arccos((mean_intensity / baseline_intensity) ** 0.5)
    verdet_equation = abs(delta_theta - arccos_val) / (voltages * NL_R * LENGTH)
    return verdet_equation


def get_list_of_projects_to_run():
    return [
        "first_experiment"
    ]


fig, axes = plt.subplots(1, 2, figsize=(16, 8))  # Create 1 row, 2 columns of subplots
for exp_type in get_list_of_projects_to_run():
    base_path = f"raw_data/{exp_type}/"
    print(base_path)
    plot_current_with_errorbars(base_path, exp_type, axes)

plt.tight_layout()  # Adjust spacing between subplots
plt.show()
