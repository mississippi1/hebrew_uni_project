import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


ALPHA = "\u03B1"
FPS = 5
MAX_VOLTAGE = 5
MIN_VOLTAGE = -5
BASE_PATH = "/lab_b_1/week_5/hysteresis_loop_ac_dc"


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


def detect_cycles(dark_to_light_ratios):
    from scipy.signal import find_peaks
    peaks, _ = find_peaks(dark_to_light_ratios, height=0)
    troughs, _ = find_peaks(-1 * np.array(dark_to_light_ratios), height=0)
    return peaks, troughs


def main():
    plt.figure()
    for folder in os.listdir(BASE_PATH):
        folder_path = os.path.join(BASE_PATH, folder)
        print(folder)
        if os.path.isdir(folder_path) and "record" in folder:
            frequency_hz = float(folder.split('_')[1].replace('mh', '')) * 1e-3  # Convert 'record_100mh' to Hz

            image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
            if frequency_hz not in [0.1, 0.2, 0.4]:
                continue
            total_frames = len(image_files)

            brightest_index = 0
            max_black_pixels = 0
            for i, image_file in enumerate(image_files):
                black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
                if black_pixels > max_black_pixels:
                    max_black_pixels = black_pixels
                    brightest_index = i

            dark_to_light_ratios = []
            for image_file in image_files:
                black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
                ratio = (black_pixels - white_pixels) / (black_pixels + white_pixels)
                dark_to_light_ratios.append(ratio)

            voltages = calculate_voltages(total_frames, frequency_hz, brightest_index)
            plt.plot(voltages, dark_to_light_ratios, 'o-', label=f'Frequency {frequency_hz} Hz',
                     markersize=2, linewidth=1, alpha=0.5)
            plt.xlabel("Voltage (V)")
            plt.ylabel(f"M - Ratio of (Black - White) Pixels {ALPHA} Magnetization")
            plt.legend()
            plt.axhline(0, color='black', linewidth=0.8)
            plt.axvline(0, color='black', linewidth=0.8)
            plt.grid(True)
    plt.title(f"Merged Hysteresis Loops")
    plt.savefig(f"results/Hysteresis Loop, Merged.jpg", dpi=300)


main()
