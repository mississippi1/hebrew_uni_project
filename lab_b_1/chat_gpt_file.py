import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

VPP = "vpp"

ALPHA = "\u03B1"
FPS = 5
MAX_VOLTAGE = 5
MIN_VOLTAGE = -5
BASE_PATH = "/users/tomerpeker/hebrew_uni_project/lab_b_1/week4/extracted_videos_frames/"
plt.rcParams['font.size'] = 22  # Set default size


def count_pixels(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    print(img_array)
    plt.hist(img_array.flatten(), bins=256)
    plt.xlim(0, 256)
    plt.show()
    black_pixels = np.sum(img_array < 100)
    white_pixels = np.sum(img_array > 100)
    std_dev = np.std(img_array)  # Standard deviation of pixel intensities
    return black_pixels, white_pixels, std_dev


def calculate_voltages(total_frames, frequency, brightest_index, max_voltage=MAX_VOLTAGE, min_voltage=MIN_VOLTAGE):
    period = 1 / frequency  # Period of one oscillation in seconds
    frames_per_cycle = FPS * period  # Total frames in one cycle
    voltage_range = max_voltage - min_voltage
    voltages = []

    for frame in range(total_frames):
        relative_index = (frame - brightest_index) % frames_per_cycle
        if relative_index < frames_per_cycle / 2:
            current_voltage = max_voltage - (relative_index / (frames_per_cycle / 2)) * voltage_range
        else:
            current_voltage = min_voltage + (
                        (relative_index - frames_per_cycle / 2) / (frames_per_cycle / 2)) * voltage_range
        voltages.append(current_voltage)

    return voltages


def determine_min_max_voltage(folder) -> [int, int]:
    return [-5, 5] if VPP in folder else [MIN_VOLTAGE, MAX_VOLTAGE]


def determine_frequency(folder):
    return float(folder.split('_')[1].replace('mh', '')) * 1e-3  # Convert 'record_100mh' to Hz


black_count = []


def main(base_path):
    for folder in os.listdir(base_path):
        folder_path = os.path.join(BASE_PATH, folder)
        if os.path.isdir(folder_path) and "record" in folder:
            results = []
            print(folder)
            frequency_hz = determine_frequency(folder)
            min_voltage, max_voltage = determine_min_max_voltage(folder=folder)
            image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])
            if frequency_hz not in [0.1, 0.12, 0.08, 0.15, 0.3, 0.2] and VPP not in folder:
                continue

            total_frames = len(image_files)
            brightest_index = 0
            max_black_pixels = 0

            dark_to_light_ratios = []
            std_errors = []

            # Compute dark-to-light ratios and standard deviation
            for image_file in image_files:
                black_pixels, white_pixels, std_dev = count_pixels(os.path.join(folder_path, image_file))
                ratio = (black_pixels - white_pixels) / (black_pixels + white_pixels)
                error = std_dev / (black_pixels + white_pixels)  # Error in the ratio
                dark_to_light_ratios.append(ratio)
                std_errors.append(error)
                results.append({"frequency": frequency_hz, "std_dev": std_dev})
                black_count.append(black_pixels)
            voltages = calculate_voltages(total_frames, frequency_hz, brightest_index, max_voltage=max_voltage,
                                          min_voltage=min_voltage)
            raw_std_dev = np.std([np.array(Image.open(os.path.join(folder_path, image_file)).convert('L'))
                                  for image_file in image_files])
            print(f"Raw Pixel Standard Deviation for Frequency {frequency_hz}: {raw_std_dev}")
            plt.figure()
            plt.hist(black_count, bins=100)
            plt.savefig(f"results/histogram_count_up_to_{result['std_dev']:.2f}.jpg",
                        dpi=300)
            plt.close()

            with open("results/histogram_std_dev.txt", "w+") as f:
                for result in results:
                    f.write(f"Frequency: {result['frequency']} Hz, Std Dev: {result['std_dev']:.2f}\n")
                f.write(f"Frequency: {frequency_hz} Hz, Std Dev: {raw_std_dev:.2f}\n")
            plt.figure()
            plt.errorbar(voltages, dark_to_light_ratios, yerr=std_errors, fmt='o-', label=f'Frequency {frequency_hz} Hz',
                         markersize=2, linewidth=0.5, alpha=0.5, capsize=2)
            plt.xlabel("Voltage (V)")
            plt.ylabel(f"Ratio of (Black - White) Pixels {ALPHA} Magnetization")
            plt.legend()
            plt.grid(True)
            plt.axhline(0, color='black', linewidth=0.8)  # Add y=0 line
            plt.axvline(0, color='black', linewidth=0.8)  # Add x=0 line
            plt.title(f"Hysteresis Loop for AC Current {frequency_hz} [Hz]")
            plt.savefig(f"results/Hysteresis Loop with Error for {folder.split('record_')[1].casefold()}.jpg", dpi=300)
            print(f"Finished with results/Hysteresis Loop with Error for {folder.split('record_')[1]}.jpg")
            plt.close()


for inx, path_ in enumerate([BASE_PATH, BASE_PATH+"/old"]):
    print(f"indx {inx}, out of {len(os.listdir(BASE_PATH))}")
    main(base_path=path_)


plt.figure()
plt.hist(black_count, bins=100)
plt.savefig(f"results/histogram_count_all.jpg",
            dpi=300)
plt.close()
