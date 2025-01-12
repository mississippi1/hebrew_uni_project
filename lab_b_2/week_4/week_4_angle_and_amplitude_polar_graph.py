import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


# Function to process the Excel file
def plot_current_with_errorbars(file_path, exp_type_):
    angles = []
    averages = []
    base_path_ = file_path
    plt.rcParams['font.size'] = 14  # Set default size
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

        # Prepare data for plotting
        if float(frequency) < 45:
            angles += [float(frequency) + 45]  # Single frequency as a list
        else:
            angles += [float(frequency) - 45]  # Single frequency as a list
        averages += [avg_current]

    # Convert angles and averages for polar coordinates
    angles_rad = np.deg2rad(np.array(angles))  # Convert angles to radians
    radius = np.array(averages)

    # Create a polar plot
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.scatter(angles_rad, radius, color=COLOR_MAP[exp_type_], label=exp_type_)

    # Adjusting the plot's appearance
    ax.set_theta_zero_location('E')  # Move zero to the East (right)
    ax.set_theta_direction(1)  # Set counterclockwise direction for angles
    # ax.set_theta_offset(np.pi / 2)  # Rotate the plot by 90 degrees
    # ax.grid(True)  # Show the grid

    ax.legend()
    plt.tick_params(axis='y', labelleft=False, labelbottom=False)  # Removes numbers on x-axis

    # Show the plot
    plt.show()


COLOR_MAP = {"half_wave": "blue", "quarter_wave": "green"}
for exp_type in ["half_wave", "quarter_wave"]:
    base_path = f"raw_data/{exp_type}/"
    plot_current_with_errorbars(base_path, exp_type)
