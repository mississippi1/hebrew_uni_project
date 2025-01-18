import numpy as np
from numpy import polyfit
import pandas as pd
import matplotlib.pyplot as plt
import os
plt.rcParams['font.size'] = 19  # Set default size


# Function to process the Excel file
def plot_current_with_errorbars(exp_type):
    # Extract the frequency from the file name (assumes name is numeric and represents frequency)
    frequencies = []
    averages = []
    error_bars = []
    base_path = f"../week_1/raw_data/{exp_type}/"
    for file in os.listdir(base_path):
        try:
            int(file[:file.find(".")])
        except ValueError:
            print(f"Could not parse as number the file name {file}")
            continue
        file_path = base_path+file
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
        frequencies += [(np.cos(float(frequency)/360*2*np.pi))**2]  # Single frequency as a list
        averages += [avg_current]
        error_bars += [[avg_current - min_current], [max_current - avg_current]]
    # Plotting
    if float(frequency) == 0:
        plt.errorbar(frequencies, averages, markersize=5, yerr=np.array(averages)*0.077,
                     fmt='o', color=COLOR_MAP[exp_type], label=exp_type)
    else:
        plt.errorbar(frequencies, averages, markersize=5, yerr=np.array(averages)*0.077,
                     fmt='o', color=COLOR_MAP[exp_type])
    # plt.title(f'Average Current vs Angle')
    plt.xlabel('Cos^2 (Angle)')
    plt.ylabel('Current (mA)')
    plt.legend()
    plt.grid(True)

    # Data example
    x = frequencies  # Replace with your actual x-axis data
    y = averages  # Replace with your actual y-axis data

    # Compute linear fit
    coefficients = np.polyfit(x, y, 1)  # Linear fit (degree=1)
    linear_fit = np.poly1d(coefficients)  # Generate linear fit function
    y_pred = linear_fit(x)  # Predicted y values
    ss_res = np.sum((y - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)  # R-squared formula

    fit_equation = f"y = {coefficients[0]:.3e}x + {coefficients[1]:.3e}, R^2  = {r_squared:.3f}"
    print(fit_equation)
    plt.plot(x, y_pred, color='red', linestyle='--', label=fit_equation)
    plt.legend()


COLOR_MAP = {"Two Different Polarizes": "blue", "Three Different Polarizes": "green"}
for exp_type in ["Two Different Polarizes"]:
    plot_current_with_errorbars(exp_type)


plt.show()

