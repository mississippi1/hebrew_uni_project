import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"

def func(file_name_input):
    print(file_name_input)
    data = pd.read_excel(file_name_input, sheet_name=0)
    time_ch1 = data['Time (s)']
    volt_ch1 = data['Volt Channel 1 (V)']
    volt_ch2 = data['Volt Channel 2 (V)']

    # plt.figure(figsize=(12, 6))
    # plt.subplot(2, 2, 1)
    # plt.plot(time_ch1, volt_ch1, label='Channel 1', color='blue')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Vx (V)')
    # plt.title('Vx over Time')
    #
    # plt.legend()
    #
    # plt.subplot(2, 2, 2)
    # plt.plot(time_ch1, volt_ch2, label='Channel 2', color='red')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Vc (V)')
    # plt.title('Vc over Time')
    # plt.legend()
    # plt.savefig(file_name_input[:file_name_input.find(".")] + "_voltage_vs_time.png")
    # plt.close()

    plt.scatter(volt_ch1.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(
        drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
             volt_ch2.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(
                 drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
                s=0.8,
             label=metal_map[file_name_input[
                   len("/Users/tomerpeker/Downloads/lab_b_1/hysteresis_loop_for_2_data/material_4_measure_2_"):]
                    .replace(".csv.xlsx", "")]
                , color=color)
    plt.xlabel(f'Vx {ALPHA} E(V)')
    plt.ylabel(f'Vc {ALPHA} B (V)')
    plt.title('Hysteresis Loop')
    plt.plot(np.linspace(min(volt_ch1 - 0.3), max(volt_ch1 + 0.3), 250),
             [0 for _ in range(250)]
             , color='black')
    plt.plot([0 for _ in range(250)],
             np.linspace(min(volt_ch2 - 0.3), max(volt_ch2 + 0.3), 250)
             , color='black')
    plt.grid(True)
    plt.xlim(min(volt_ch1 - 0.001), max(volt_ch1 + 0.001))
    plt.ylim(min(volt_ch2 - 0.001), max(volt_ch2 + 0.001))
    plt.legend()

    plt.tight_layout()
    # plt.savefig(file_name_input[:file_name_input.find(".")] + "_voltage_vs_voltage.png")


files = os.listdir('/Users/tomerpeker/Downloads/lab_b_1/hysteresis_loop_for_2_data/')
colorcode = {1: "red", 0: "blue"}
metal_map = {"17_pieces": "Metal 4", "2_pieces": "Metal 2", }
cnt = 0
for file_name in files:
    if file_name.endswith(".xlsx"):
        print(file_name)
        color = colorcode[cnt]
        func(file_name_input="/Users/tomerpeker/Downloads/lab_b_1/hysteresis_loop_for_2_data/" + file_name)
        cnt += 1
plt.show()
