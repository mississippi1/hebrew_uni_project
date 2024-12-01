import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


ALPHA = "\u03B1"


# Function to count black and white pixels
def count_pixels(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    black_pixels = np.sum(img_array < 30)
    white_pixels = np.sum(img_array > 30)
    return black_pixels, white_pixels


# Extract frequency from folder name
def extract_frequency(folder_name):
    parts = folder_name.split('_')
    for part in parts:
        if 'mh' in part.lower():
            return int(part.lower().replace('mh', '').replace('m', ''))
    return None


# Base directory containing folders of images
base_dir = "/Users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames"
fps = 25  # Camera frames per second

# Loop through each folder
for folder in sorted(os.listdir(base_dir)):
    folder_path = os.path.join(base_dir, folder)
    if os.path.isdir(folder_path):
        frequency = extract_frequency(folder)
        if frequency is None:
            continue

        white_pixel_counts = []
        black_pixel_counts = []
        images = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])

        # Process each image and count pixels
        for image_file in images:
            image_path = os.path.join(folder_path, image_file)
            black_pixels, white_pixels = count_pixels(image_path)
            white_pixel_counts.append(white_pixels)
            black_pixel_counts.append(black_pixels)

        # Determine imax (index of the image with most white pixels)
        imax = np.argmax(white_pixel_counts)

        # Calculate voltage for each frame using triangular wave model
        T = fps / frequency  # Number of frames in one period
        voltages = []
        switch = False

        for i in range(len(white_pixel_counts)):

            if 5 - (20 / T) * i >= -5:
                switch = True
            if not switch:
                voltages.append(5 - (20 / T) * i)
            else:
                voltages.append(5 - (20 / T) * i)

        # Normalize black and white pixel counts for hysteresis plot
        black_white_ratios = [
            (2 * (w - b)) / (w + b)
            for w, b in zip(white_pixel_counts, black_pixel_counts)
        ]
        print()
        # Plot the hysteresis loop
        plt.figure(figsize=(8, 6))
        plt.plot(voltages, black_white_ratios, label=f'Hysteresis for {frequency} MHz', marker='o')
        plt.axhline(0, color='black', linewidth=0.8)  # Add y=0 line
        plt.axvline(0, color='black', linewidth=0.8)  # Add x=0 line
        plt.title(f'Hysteresis Loop for Frequency {frequency} MHz')
        plt.xlabel('Voltage [V]')
        plt.ylabel(f'Normalized Pixel Ratio {ALPHA} Magnetization')
        plt.legend()
        plt.grid(True)
        plt.show()
