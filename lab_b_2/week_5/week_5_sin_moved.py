import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
cmap = plt.get_cmap("tab10")  # Use a colormap with a variety of distinct colors


def cosine_wave(x, A, B, C):
    """Sine function for fitting."""
    return A * np.cos(np.radians(B * x + C)) ** 2


def fit_cosine_wave(angles, averages) -> [np.array, np.array, np.array]:
    """Fit the sine wave to the data."""
    # Initial guess for the parameters [Amplitude, Frequency, Phase]
    initial_guess = [max(averages) - min(averages), 1, 0]
    params = curve_fit(f=cosine_wave, xdata=angles, ydata=averages, p0=initial_guess)
    return params[0]


def plot_current_with_errorbars(file_path, exp_type_):
    plt.rcParams['font.size'] = 16  # Set default font size
    base_path_ = file_path
    delta_theta_array = []
    # Get the list of voltage directories
    directories = [directory_ for directory_ in os.listdir(base_path_) if os.path.isdir(base_path_ + directory_)]
    directories.sort(key=lambda directory_name: float(directory_name.replace("v", "")))  # Optional: Sort directories to ensure consistent order
    print(directories)
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
        A, B, C = fit_cosine_wave(angles, averages)
        print(A)
        color = cmap(i % 10)  # Cycle through colormap
        delta_theta_array.append(C)
        plt.errorbar(
            x=angles,
            y=averages,
            xerr=0,
            yerr=0,
            fmt='o',
            markersize=6,
            linewidth=2,
            alpha=0.9,
            capsize=5,
            color=color
        )
        fit_angles = np.linspace(0, 100, 500)
        fit_averages = cosine_wave(fit_angles, A, B, C)
        plt.plot(fit_angles, fit_averages,
                 label=f"Fit Volt {voltage}: {A:.2f} * cosine^2({B:.2f}x + {C:.2f})", linestyle='--', color=color)

        plt.title(f"laser: {exp_type_}")
        plt.xlabel("Angle (degrees)")
        plt.ylabel("I (mA)")
        plt.grid(True)
        plt.legend()
        plt.xlim(0, 100)

    # Adjust layout
    plt.xlim(0, 100)
    plt.tight_layout()
    return (np.array([float(i.replace("v", "")) for i in directories]),
            delta_theta_array)


def get_list_of_projects_to_run():
    return [
        "green_543",
        "red",
        "yellow_594",
    ]


def plot_linear_verdet(volt_array: np.array, delta_theta_array: np.array, title: str):
    ratio_of_volt_to_magnetic_field = 15.2*10**-4
    length_of_coil = 23.5*10**-3
    magnetic_field_array = volt_array*ratio_of_volt_to_magnetic_field
    magnetic_field_array_times_length = magnetic_field_array * length_of_coil
    f = plt.figure()
    max_angle = max(np.array(delta_theta_array))
    delta_theta_array_minus_min_angle = (max_angle - np.array(delta_theta_array))/360*2*np.pi
    x = magnetic_field_array_times_length
    y = delta_theta_array_minus_min_angle
    coefficients = np.polyfit(x=x, y=y, deg=1)
    linear_fit = np.poly1d(coefficients)  # Generate linear fit function
    y_pred = linear_fit(x)  # Predicted y values
    ss_res = np.sum((y - y_pred) ** 2)  # Residual sum of squares
    ss_tot = np.sum((y - np.mean(y)) ** 2)  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)  # R-squared formula
    fit_equation = f"y = {coefficients[0]:3}x + {coefficients[1]:3}, R^2  = {r_squared:.3f}"
    plt.plot(x,
             y,
             markersize=6,
             linewidth=2,
             alpha=0.9
             )
    plt.plot(x, y_pred, color='red', linestyle='--', label=fit_equation)
    plt.title(f"laser: {title}")
    plt.xlabel("b*l")
    plt.ylabel("delta theta")
    plt.grid(True)
    plt.legend()


def main():
    for exp_type in get_list_of_projects_to_run():
        base_path = f"raw_data/{exp_type}/"
        print(base_path)
        volt_array, delta_theta_array = plot_current_with_errorbars(base_path, exp_type)
        plot_linear_verdet(volt_array, delta_theta_array, exp_type)
        plt.show()


if __name__ == "__main__":
    main()