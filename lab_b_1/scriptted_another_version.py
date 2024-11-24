import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"


def func(file_name_input):
    data = pd.read_excel(file_name_input, sheet_name=0)
    time_ch1 = data['Time (s)']
    volt_ch1 = data['Volt Channel 1 (V)']
    volt_ch2 = data['Volt Channel 2 (V)']

    # plt.figure(figsize=(12, 6))
    # plt.subplot(2, 2, 1)
    # plt.plot(time_ch1, volt_ch1, label='Channel 1', color='blue')
    # plt.xlabel('Time (s)')
    # plt.ylabel(f'Vx {ALPHA} E(V)')
    # plt.title('Vx over Time')
    #
    # plt.legend()
    #
    # plt.subplot(2, 2, 2)
    # plt.plot(time_ch1, volt_ch2, label='Channel 2', color='red', )
    # plt.xlabel('Time (s)')
    # plt.ylabel(f'Vc {ALPHA} B(V)')
    # plt.title('Vc over Time')
    # plt.legend()
    # plt.savefig(file_name_input[:file_name_input.find(".")] + "_voltage_vs_time.png")
    # plt.close()

    plt.scatter(x=volt_ch1.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(
        drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
             y=volt_ch2.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(
                 drop=True) / COEFFICIENT_TO_SMOOTH_LINES, s=0.5, color='blue')
    plt.xlabel(f'Vx {ALPHA} E (V)')
    plt.ylabel(f'Vc {ALPHA} B (V)')
    plt.title(f'{metal_type.capitalize()} - Vx {ALPHA} E As a Function of Vc {ALPHA} B')
    plt.plot(np.linspace(min(volt_ch1 - 0.3), max(volt_ch1 + 0.3), 250),
             [0 for _ in range(250)], color='black')
    plt.plot([0 for _ in range(250)],
             np.linspace(min(volt_ch2 - 0.3), max(volt_ch2 + 0.3), 250),
             color='black')
    plt.grid(True)
    a.append(
        (min(volt_ch1), min(volt_ch2), max(volt_ch1), max(volt_ch2))
    )

    plt.xlim(min([i[0] for i in a]), max([i[2] for i in a]))
    plt.ylim(min([i[1] for i in a]), max([i[3] for i in a]))
    plt.legend()

    # plt.tight_layout()
    # plt.savefig(file_name_input[:file_name_input.find(".")] + "_voltage_vs_voltage.png")
    # plt.close()
    # print(os.getcwd())


a = []
metal_type = 'Metal 1'
for file_name in sorted(list(i for i in os.listdir('/Users/tomerpeker/Downloads/lab_b_1/%s/' % metal_type))):
    if file_name.endswith(".xlsx"):
        func(file_name_input="/Users/tomerpeker/Downloads/lab_b_1/" + metal_type + "/" + file_name)
        print(file_name)
plt.scatter(x=[i[2] for i in a]+[0], y=[i[3] for i in a]+[0], color="red", marker='*')
plt.plot(sorted([i[2] for i in a]+[0]), sorted([i[3] for i in a]+[0]), color="red")
# plt.scatter(x=[i[0] for i in a]+[0], y=[i[1] for i in a]+[0], color="red", marker='*')
# plt.plot(sorted([i[0] for i in a]+[0]), sorted([i[1] for i in a]+[0]), color="red")
plt.show()
