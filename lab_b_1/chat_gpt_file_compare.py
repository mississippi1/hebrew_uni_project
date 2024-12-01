import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


FPS = 5
MAX_VOLTAGE = 5
MIN_VOLTAGE = -5
BASE_PATH = "/users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames"


def count_pixels(image_path):
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    black_pixels = np.sum(img_array < 80)
    white_pixels = np.sum(img_array > 80)
    return black_pixels, white_pixels


def calculate_voltages(total_frames_, frequency, brightest_index_):
    period = 1 / frequency  # Period of one oscillation in seconds
    frames_per_cycle = FPS * period  # Total frames in one cycle
    voltage_range = MAX_VOLTAGE - MIN_VOLTAGE
    voltages_ = []

    # Compute voltages assuming a triangle wave pattern centered around the brightest frame
    for frame in range(total_frames_):
        relative_index = (frame - brightest_index_) % frames_per_cycle
        if relative_index < frames_per_cycle / 2:
            current_voltage = MAX_VOLTAGE - (relative_index / (frames_per_cycle / 2)) * voltage_range
        else:
            current_voltage = MIN_VOLTAGE + (
                    (relative_index - frames_per_cycle / 2) / (frames_per_cycle / 2)) * voltage_range
        voltages_.append(current_voltage)

    return voltages_


def detect_cycles(dark_to_light_ratios_):
    from scipy.signal import find_peaks
    peaks_, _ = find_peaks(dark_to_light_ratios_, height=0)  # Detect peaks for max (brightest)
    troughs_, _ = find_peaks(-1 * np.array(dark_to_light_ratios_), height=0)  # Detect troughs for min (darkest)
    return peaks_, troughs_


def main():
    # Iterate through folders
    for folder in os.listdir(BASE_PATH):
        folder_path = os.path.join(BASE_PATH, folder)
        if os.path.isdir(folder_path) and "record" in folder:
            # Extract frequency from folder name
            frequency_hz = float(
                folder.split('_')[1].replace('mh', '').replace('1h', '1000')) * 1e-3  # Convert '100mh' to Hz

            image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
            total_frames = len(image_files)

            # Find the brightest frame
            brightest_index = 0
            max_white_pixels = 0
            for i, image_file in enumerate(image_files):
                _, white_pixels = count_pixels(os.path.join(folder_path, image_file))
                if white_pixels > max_white_pixels:
                    max_white_pixels = white_pixels
                    brightest_index = i

            # Calculate black/white pixel ratio and voltages
            dark_to_light_ratios = []
            for image_file in image_files:
                black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
                ratio = (black_pixels - white_pixels) / (black_pixels + white_pixels)
                dark_to_light_ratios.append(ratio)

            voltages = calculate_voltages(total_frames, frequency_hz, brightest_index)

            # Detect cycles
            peaks, troughs = detect_cycles(dark_to_light_ratios)
            voltages_array = np.array(voltages)  # Convert voltages to a NumPy array
            ratios_array = np.array(dark_to_light_ratios)  # Ensure ratios are also a NumPy array

            # Plot hysteresis loop
            plt.figure()
            plt.plot(voltages, dark_to_light_ratios, 'o-', label=f'Frequency {frequency_hz} Hz')
            print(folder_path, peaks, troughs)
            plt.scatter(voltages_array[peaks], ratios_array[peaks], color='red', label='Peaks')
            plt.scatter(voltages_array[troughs], ratios_array[troughs], color='blue', label='Troughs')
            plt.xlabel("Voltage (V)")
            plt.ylabel("Ratio of (Black - White) Pixels")
            plt.title(f"Hysteresis Loop for {folder}")
            plt.legend()
            plt.grid(True)
            plt.savefig(f"Hysteresis Loop for {frequency_hz} - compare.jpg")


main()
