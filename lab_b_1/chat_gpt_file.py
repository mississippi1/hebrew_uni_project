import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Parameters
fps = 25  # Frames per second from your camera
max_voltage = 5
min_voltage = -5
base_path = "/Users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames"


def count_pixels(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    black_pixels = np.sum(img_array < 30)
    white_pixels = np.sum(img_array > 30)
    return black_pixels, white_pixels


def calculate_voltages(frames_count, frequency, brightest_index):
    period = 1 / frequency  # Period of one oscillation in seconds
    frames_per_cycle = fps * period  # Total frames in one cycle
    voltage_range = max_voltage - min_voltage  # Total voltage range
    voltage_increment = voltage_range / (frames_per_cycle / 2)  # Triangle wave increment per frame

    voltages = []
    current_voltage = max_voltage
    increasing = False  # Start decreasing after the brightest frame

    for frame in range(frames_count):
        # Adjust cycle around the brightest frame
        print(frame)
        relative_index = (frame - brightest_index) % frames_per_cycle
        if relative_index < frames_per_cycle / 2:
            current_voltage = max_voltage - voltage_increment * relative_index
        else:
            current_voltage = min_voltage + voltage_increment * (relative_index - frames_per_cycle / 2)
        voltages.append(current_voltage)

    return voltages


# Iterate through folders
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    if os.path.isdir(folder_path) and "record" in folder:
        # Extract frequency from folder name
        frequency_hz = float(folder.split('_')[1].replace('mh', '')) * 1e-3  # Convert '100mh' to Hz

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

        # Calculate voltages
        voltages = calculate_voltages(total_frames, frequency_hz, brightest_index)

        # Calculate black and white pixel ratios
        dark_to_light_ratios = []
        for image_file in image_files:
            black_pixels, white_pixels = count_pixels(os.path.join(folder_path, image_file))
            ratio = (black_pixels - white_pixels) / (black_pixels + white_pixels)
            dark_to_light_ratios.append(ratio)

        # Plot hysteresis loop
        plt.figure()
        plt.plot(voltages, dark_to_light_ratios, 'o-', label=f'Frequency {frequency_hz} Hz')
        plt.xlabel("Voltage (V)")
        plt.ylabel("Ratio of (Black - White) Pixels")
        plt.title(f"Hysteresis Loop for {folder}")
        plt.legend()
        plt.grid(True)
        plt.show()
