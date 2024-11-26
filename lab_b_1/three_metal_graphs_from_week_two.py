import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"


# Extract columns for each channel

def draw(number_):
    file_path = f'/Users/tomerpeker/hebrew_uni_project/lab_b_1/week_3_same_data/{number_}.csv.xlsx'
    data = pd.read_excel(file_path, sheet_name=0)
    volt_ch1 = data['Volt Channel 1 (V)']
    volt_ch2 = data['Volt Channel 2 (V)']

    # # Plot Channel 1
    # plt.figure(figsize=(12, 6))
    # plt.subplot(2, 2, 1)
    # plt.plot(time_ch1, volt_ch1, label='Channel 1', color='blue')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Vx (V)')
    # plt.title('Vx over Time')
    #
    # plt.legend()
    #
    # # Plot Channel 2
    # plt.subplot(2, 2, 2)
    # plt.plot(time_ch1, volt_ch2, label='Channel 2', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Vc (V)')
    # plt.title('Vc over Time')
    # plt.legend()
    # plt.show()

    plt.scatter(volt_ch1.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
             volt_ch2.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
             label=f"Metal {number_}", s=1.5, alpha=0.8)

    plt.xlabel(f'Vx {ALPHA} H (V)')
    plt.ylabel(f'Vc {ALPHA} B (V)')
    plt.title(f'Hysteresis Loops')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1, linestyle='-')  # Horizontal line at y=0
    plt.axvline(0, color='black', linewidth=1, linestyle='-')  # Vertical line at x=0

    plt.legend()
    plt.tight_layout()


for i in [2, 4, 6]:
    draw(i)

plt.savefig(f"/Users/tomerpeker/hebrew_uni_project/lab_b_1/images/metal_multiple_vx_vs_vc.png")

