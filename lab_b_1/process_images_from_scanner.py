import os
from PIL import Image  # For image processing
import matplotlib.pyplot as plt
import numpy as np

# List of image indices
IMAGE_INDICES = list(range(218, 253)) + list(range(402, 446))

# List of numbers indicating partitions
PARTITION_POINTS = [230, 240, 410, 430]

# Sort the partition points for proper comparison
PARTITION_POINTS.sort()


def assign_images_to_voltages(image_indices, partition_points):
    image_voltage_map = {}  # Map images to their voltages
    for index in image_indices:
        assigned = False
        for i, point in enumerate(partition_points):
            if index < point:
                # TODO : need for a real map on voltages
                voltage = 6 if i % 2 == 0 else 0  # 6V for even partitions, 0V for odd partitions
                image_voltage_map[index] = voltage
                assigned = True
                break
        if not assigned:  # For indices greater than the last partition
            image_voltage_map[index] = 6
    return image_voltage_map


def count_black_pixels(image_path):
    try:
        with Image.open(image_path) as img:
            grayscale = img.convert("L")  # Convert to grayscale
            # Count black pixels (pixel value = 0)
            black_pixel_count = np.sum(np.array(grayscale) == 0)
        return black_pixel_count
    except FileNotFoundError:
        print(f"Image not found: {image_path}")
        return None


def process_images(image_indices_input, partition_points, image_dir):
    # Assign voltages
    image_voltage_map = assign_images_to_voltages(image_indices_input, partition_points)

    # Process each image
    black_pixel_counts = []
    voltages = []

    for image_index in image_indices_input:
        image_path = os.path.join(image_dir, f"image_{image_index}.png")  # Adjust naming as needed
        black_pixels = count_black_pixels(image_path)
        if black_pixels is not None:
            black_pixel_counts.append(black_pixels)
            voltages.append(image_voltage_map[image_index])

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.scatter(voltages, black_pixel_counts, c="blue", alpha=0.7)
    plt.title("Black Pixel Count vs Voltage")
    plt.xlabel("Voltage (V)")
    plt.ylabel("Black Pixel Count")
    plt.grid(True)
    plt.show()


# Directory containing images (update to your path)
image_dir_const = "./images"  # Change to the actual directory

# Run the script
process_images(IMAGE_INDICES, PARTITION_POINTS, image_dir_const)
