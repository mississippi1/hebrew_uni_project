import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.size'] = 19  # Set default size


# Function to process the Excel file
def plot_current_with_errorbars(file_path, exp_type):
    # Extract the frequency from the file name (assumes name is numeric and represents frequency)
    frequency = os.path.splitext(os.path.basename(file_path))[0]  # File name without extension

    # Read the Excel file
    # Skip rows with metadata at the top (row 6 contains column headers, index = 5 for pandas)
    data = pd.read_excel(file_path, skiprows=5)

    # Ensure the data is clean and the relevant columns exist
    if 'Current (A)' not in data.columns:
        raise ValueError("Expected column 'Current (A)' not found in the Excel file.")

    # Calculate statistics for current
    avg_current = data['Current (A)'].mean()*1_000
    min_current = data['Current (A)'].min()*1_000
    max_current = data['Current (A)'].max()*1_000

    # Prepare data for plotting
    frequencies = [float(frequency)]  # Single frequency as a list
    averages = [avg_current]
    error_bars = [[avg_current - min_current], [max_current - avg_current]]
    # Plotting
    if float(frequency) == 0:
        plt.errorbar(frequencies, averages, yerr=np.array(averages)*0.077,
                     xerr=float(2)/360*2*np.pi, markersize=4,
                     fmt='o', color=COLOR_MAP[exp_type])
    else:
        plt.errorbar(frequencies, averages, yerr=np.array(averages)*0.077, xerr=float(2)/360*2*np.pi,
                     markersize=4,
                     fmt='o', color=COLOR_MAP[exp_type])
    # plt.title(f'Average Current vs Angle')
    plt.xlabel('Angle (Deg)')
    plt.ylabel('Current (mA)')
    # plt.xlim((0, 3.5))
    # plt.ylim((0, 0.0002))
    plt.legend()
    plt.grid(True)


COLOR_MAP = {"Two Different Polarizes": "blue", "Three Different Polarizes": "green"}
for exp_type in ["Two Different Polarizes", "Three Different Polarizes"]:
    base_path = f"../week_1/raw_data/{exp_type}/"
    for file in os.listdir(base_path):
        try:
            int(file[:file.find(".")])
        except ValueError:
            print(f"Could not parse as number the file name {file}")
            continue
        plot_current_with_errorbars(base_path+file, exp_type)
    plt.show()
