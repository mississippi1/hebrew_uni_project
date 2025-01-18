import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

NL_R = 15.2 * 10 ** -4
FIRST_EXPERIMENT = "first_experiment"
SECOND_EXPERIMENT = "second_experiment"
LENGTH = 23.5 * 10 ** -3


def calculate_fit(theta, voltage, mean_intensity, baseline_intensity):
    delta_theta = (-2 + theta) * 2 * np.pi / 360
    arccos_val = np.arccos((mean_intensity / baseline_intensity) ** 0.5)
    verdet_equation = abs(delta_theta - arccos_val) / (voltage * NL_R * LENGTH)
    return verdet_equation


def plot_current_with_errorbars(file_path, exp_type_):
    plt.rcParams['font.size'] = 16  # Set default font size
    base_path_ = file_path

    # Get the list of voltage directories
    directories = [directory_ for directory_ in os.listdir(base_path_) if os.path.isdir(base_path_ + directory_)]
    directories.sort()  # Optional: Sort directories to ensure consistent order
    for i, directory_ in enumerate(directories):
        angles = []
        averages = []
        print(directory_)
        for file_ in os.listdir(base_path_ + directory_):
            try:
                int(file_[:file_.find(".")])
            except ValueError:
                print(f"Could not parse as number the file name {file_}")
                continue
            file_path = base_path_ + directory_ + "/" + file_
            angle = os.path.splitext(os.path.basename(file_path))[0]  # File name without extension
            data = pd.read_excel(file_path, skiprows=5)
            if 'Current (A)' not in data.columns:
                raise ValueError("Expected column 'Current (A)' not found in the Excel file.")
            avg_current = data['Current (A)'].mean() * 1_000
            angles.append(float(angle))
            averages.append(avg_current)
        angles = np.array(angles)
        voltage = float(directory_.replace("v", ""))
        # pred = calculate_fit(
        #     theta=angles,
        #     voltage=voltage,
        #     mean_intensity=np.array(averages),
        #     baseline_intensity=107.88 * 10 ** -3
        # )

        # Plot in the corresponding subplot
        plt.errorbar(
            x=angles,
            y=averages,
            xerr=0,
            yerr=0,
            label=f"volt - {voltage}",
            fmt='o',
            markersize=6,
            linewidth=2,
            alpha=0.9,
            capsize=5
        )
        plt.title(f"Voltage: {directory_}")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("I (mA)")
        plt.grid(True)
        plt.legend()
        plt.xlim(0, 50)
    # Adjust layout
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.show()


COLOR_MAP = {SECOND_EXPERIMENT: "blue", FIRST_EXPERIMENT: "green"}


def get_list_of_projects_to_run():
    return [
        SECOND_EXPERIMENT
        # FIRST_EXPERIMENT
    ]


for exp_type in get_list_of_projects_to_run():
    base_path = f"raw_data/{exp_type}/"
    print(base_path)
    plot_current_with_errorbars(base_path, exp_type)
