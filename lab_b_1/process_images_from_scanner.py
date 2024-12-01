import os
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


ALPHA = "\u03B1"
IMAGE_INDICES = list(range(0, 552))

# VOLTAGE_MAP = pd.read_excel("/Users/tomerpeker/Downloads/הצמדה בין שם תמונה למתח.xlsx")

VOLTAGE_MAP = pd.read_excel('/Users/tomerpeker/Downloads/הצמדת מתחים פריימים 100 מיליהרץ.xlsx')


def assign_images_to_voltages(image_indices):
    image_voltage_map = {}
    for index in image_indices:
        voltage = VOLTAGE_MAP[VOLTAGE_MAP["Index"] == index]["Voltage"]
        image_voltage_map[index] = float(voltage.values)
    return image_voltage_map


def count_black_pixels(image_path):
    try:
        with Image.open(image_path) as img:
            grayscale = img.convert("L")
            # grayscale.save("grayscale_"+image_path+".jpg")
            whites = np.sum(np.array(grayscale) > 80)
            blacks = (np.sum(np.array(grayscale) <= 80))
            ratio = (whites - blacks) / (blacks + whites)
            black_pixel_count = ratio
            if image_path.endswith("233.jpg"):
                print(black_pixel_count, whites)
        return black_pixel_count
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return None


def process_images(image_indices_input, image_dir):
    image_voltage_map = assign_images_to_voltages(image_indices_input)
    black_pixel_counts = []
    voltages = []
    for image_index in image_indices_input:
        image_path = os.path.join(image_dir, f"frame_{str(image_index).zfill(4)}.jpg")
        black_pixels = count_black_pixels(image_path)
        if black_pixels is not None:
            black_pixel_counts.append(black_pixels)
            voltages.append(image_voltage_map[image_index])
    plt.figure(figsize=(10, 6))
    plt.scatter(voltages, black_pixel_counts, c="blue", alpha=0.7, s=5)
    plt.plot(voltages, black_pixel_counts, c="purple", alpha=0.6)
    plt.title("Dark and Light Pixels as a function of Voltage")
    plt.xlabel(f"Voltage {ALPHA} H (V)")
    plt.ylabel(f"Ratio between Dark and Light {ALPHA} Magnetization")
    plt.axhline(0, color='black', linewidth=1, linestyle='-')  # Horizontal line at y=0
    plt.axvline(0, color='black', linewidth=1, linestyle='-')  # Vertical line at x=0
    plt.grid(True)
    # plt.savefig("/Users/tomerpeker/hebrew_uni_project/lab_b_1/images/dark_and_light.png")
    plt.show()


image_dir_const = "/Users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames/record_100mh_10vpp"

# Run the script
process_images(IMAGE_INDICES, image_dir_const)
