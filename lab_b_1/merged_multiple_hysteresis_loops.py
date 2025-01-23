import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from numpy import trapz



ALPHA = "\u03B1"
FPS = 5
MAX_VOLTAGE = 5
MIN_VOLTAGE = -5
BASE_PATH = "/users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames"
color_map = {0.1: "blue", 0.2: "green", 0.4: "red"}

plt.rcParams['font.size'] = 22  # Set default size

def count_pixels(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    black_pixels = np.sum(img_array < 100)
    white_pixels = np.sum(img_array > 100)
    return black_pixels, white_pixels


def calculate_voltages(total_frames, frequency, brightest_index):
    period = 1 / frequency  # Period of one oscillation in seconds
    frames_per_cycle = FPS * period  # Total frames in one cycle
    voltage_range = MAX_VOLTAGE - MIN_VOLTAGE
    voltages = []

    # Compute voltages assuming a triangle wave pattern centered around the brightest frame
    for frame in range(total_frames):
        relative_index = (frame - brightest_index) % frames_per_cycle
        if relative_index < frames_per_cycle / 2:
            current_voltage = MAX_VOLTAGE - (relative_index / (frames_per_cycle / 2)) * voltage_range
        else:
            current_voltage = MIN_VOLTAGE + (
                    (relative_index - frames_per_cycle / 2) / (frames_per_cycle / 2)) * voltage_range
        voltages.append(current_voltage)

    return voltages


def detect_intersections_and_extrema(voltages, dark_to_light_ratios):
    # Find intersections with axes and extrema of the hysteresis loop
    intersections = [(v, m) for v, m in zip(voltages, dark_to_light_ratios) if np.isclose(m, 0, atol=0.2)]
    max_point = max(zip(voltages, dark_to_light_ratios), key=lambda x: x[1])  # Top-right point
    min_point = min(zip(voltages, dark_to_light_ratios), key=lambda x: x[1])  # Bottom-left point
    return intersections, max_point, min_point


def calculate_hysteresis_area(voltage, magnetization):
    # Ensure the data forms a closed loop
    if not (voltage[0] == voltage[-1] and magnetization[0] == magnetization[-1]):
        voltage = np.append(voltage, voltage[0])
        magnetization = np.append(magnetization, magnetization[0])

    # Use Simpson's rule to calculate the enclosed area
    area = simpson(y=magnetization, x=voltage)
    return abs(area), trapz(x=voltage, y=magnetization), "error - " + str(abs(area) - abs(trapz(x=voltage, y=magnetization)))


def main():
    folders = [folder for folder in os.listdir(BASE_PATH)
               if os.path.isdir(os.path.join(BASE_PATH, folder))
               and "record" in folder
               and "vpp" in folder]
    folders = sorted(folders)  # Sort folders for consistent subplot arrangement

    frequencies_to_plot = [0.1, 0.2, 0.4]
    # figure, axes = plt.subplots(2, 2, figsize=(12, 10))
    # axes = axes.flatten()
    axes = plt.figure()
    all_extrema = []  # Store extrema for the 4th plot

    for i, folder in enumerate(folders):
        folder_path = os.path.join(BASE_PATH, folder)
        frequency_hz = float(folder.split('_')[1].replace('mh', '')) * 1e-3  # Convert 'record_100mh' to Hz
        if frequency_hz not in frequencies_to_plot:
            continue

        image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
        total_frames = len(image_files)

        # Find the brightest frame
        brightest_index = 0
        max_black_pixels = 0
        for i, image_file in enumerate(image_files):
            black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
            if black_pixels > max_black_pixels:
                max_black_pixels = black_pixels
                brightest_index = i

        # Compute dark-to-light ratios
        dark_to_light_ratios = []
        for image_file in image_files:
            black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
            ratio = (black_pixels - white_pixels) / (black_pixels + white_pixels)
            dark_to_light_ratios.append(ratio)

        # Calculate voltages
        voltages = calculate_voltages(total_frames, frequency_hz, brightest_index)

        # Calculate area and error
        area, _, _ = calculate_hysteresis_area(voltage=voltages, magnetization=dark_to_light_ratios)

        # Calculate errors
        x_error = [2*frequency_hz] * len(voltages)  # Error in x-axis (half the frequency)

        # Plot error bars instead of a simple line plot
        # ax = axes[frequencies_to_plot.index(frequency_hz)]
        plt.errorbar(voltages, dark_to_light_ratios, xerr=x_error, fmt='o',
                    markersize=3, linewidth=1, alpha=0.5, color=color_map[frequency_hz])
        plt.plot(voltages, dark_to_light_ratios, 'o-', markersize=5, linewidth=4,
                alpha=0.5,
                color=color_map[frequency_hz])

        # Add labels and titles
        plt.xlabel("Voltage (V)")
        # ax.set_ylabel(f"M - Ratio of (Black - White) Pixels {ALPHA} Magnetization")
        plt.legend()
        plt.axhline(0, color='black', linewidth=0.8)  # Horizontal line at y=0
        plt.axvline(0, color='black', linewidth=0.8)  # Vertical line at x=0
        plt.grid(True)
        plt.title(f"Hysteresis Loop - {frequency_hz} Hz")
        plt.show()
        # plt.close()
    plt.tight_layout()
    plt.savefig("results/Hysteresis_Loop_Subplots.jpg", dpi=300)
    plt.show()


main()