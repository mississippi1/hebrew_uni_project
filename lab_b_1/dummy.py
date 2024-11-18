import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10


def smooth_lines(data) -> pd.Series():
    return data.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(
        drop=True) / COEFFICIENT_TO_SMOOTH_LINES


voltage_2 = pd.read_excel("/Users/tomerpeker/Downloads/lab_b_1/round_corners_2.csv.xlsx",
                          sheet_name=0)
voltage_6 = pd.read_excel("/Users/tomerpeker/Downloads/lab_b_1/6.csv.xlsx",
                          sheet_name=0)
slim_04 = pd.read_excel("/Users/tomerpeker/Downloads/lab_b_1/slim_4.csv.xlsx",
                        sheet_name=0)

voltage_2_volt_ch1 = voltage_2['Volt Channel 1 (V)']
voltage_2_volt_ch2 = voltage_2['Volt Channel 2 (V)']
voltage_6_volt_ch1 = voltage_6['Volt Channel 1 (V)']
voltage_6_volt_ch2 = voltage_6['Volt Channel 2 (V)']
slim_04_volt_ch1 = slim_04['Volt Channel 1 (V)']
slim_04_volt_ch2 = slim_04['Volt Channel 2 (V)']

plt.figure(figsize=(12, 6))
plt.plot(smooth_lines(voltage_2_volt_ch1), smooth_lines(voltage_2_volt_ch2), label='Experiment 2', color='blue')
plt.legend()
plt.plot(smooth_lines(voltage_6_volt_ch1), smooth_lines(voltage_6_volt_ch2), label='Experiment 6', color='red')
plt.plot(smooth_lines(slim_04_volt_ch1), smooth_lines(slim_04_volt_ch2), label='Experiment 4', color='purple')
plt.plot(np.linspace(min(voltage_2_volt_ch1 - 0.3), max(voltage_2_volt_ch1 + 0.3), 250),
             [0 for _ in range(250)]
             , color='black')
plt.plot([0 for _ in range(250)],
         np.linspace(min(voltage_2_volt_ch1 - 0.3), max(voltage_2_volt_ch1 + 0.3), 250)
         , color='black')
plt.xlabel('Vx (V)')
plt.ylabel('Vc (V)')
plt.grid(True)
plt.xlim(-0.38, 0.38)
plt.ylim(-0.04, 0.04)
plt.title('Vx Vs Vc Across Experiments')

# plt.plot(np.linspace(min(voltage_2 - 0.2), max(voltage_2 + 0.2), 250),
#          [0 for _ in range(250)]
#          , color='black')
# plt.plot([0 for _ in range(250)],
#          np.linspace(min(voltage_2 - 0.2), max(voltage_2 + 0.2), 250)
#          , color='black')
# plt.grid(True)
# plt.xlim(min(voltage_2 - 0.001), max(voltage_2 + 0.001))
# plt.ylim(min(voltage_2 - 0.001), max(voltage_2 + 0.001))
plt.legend()

plt.tight_layout()
plt.show()

plt.close()
