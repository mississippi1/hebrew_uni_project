import os
import re

# Directory containing the images
image_dir = "/Users/tomerpeker/Downloads/drive-download-20241208T175842Z-001"


def rename_images(image_dir):
    # List all files in the directory
    files = [f for f in os.listdir(image_dir) if f.startswith("Capture_") and f.endswith(".jpg")]

    # Extract numeric suffixes and sort the files
    file_data = []
    for file in files:
        match = re.search(r"Capture_(\d+)\.jpg", file)
        if match:
            file_data.append((int(match.group(1)), file))

    # Sort files by their numeric suffix
    file_data.sort()

    # Rename files to their new order
    for new_index, (_, old_name) in enumerate(file_data, start=1):
        old_path = os.path.join(image_dir, old_name)
        new_name = f"image_{new_index}.jpg"
        new_path = os.path.join(image_dir, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")


# Run the script
rename_images(image_dir)
