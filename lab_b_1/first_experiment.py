import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"
# figure, [sb1, sb2] = plt.subplots(2, 2)
color_map = {3: "blue", 10: "green"}
for number in [3, 10]:

    file_path = f'/Users/tomerpeker/hebrew_uni_project/lab_b_1/three_and_ten/{number}.csv.xlsx'
    data = pd.read_excel(file_path)
    # Extract columns for each channel
    time_ch1 = data['Time (s)']
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
             color=color_map[number], s=3, alpha=1)
    plt.xlabel(f'Vx {ALPHA} H (V)')
    plt.ylabel(f'Vc {ALPHA} B (V)')
    # plt.title(f'Hysteresis Loops, for Metals 1 and 2')
    plt.plot(np.linspace(min(volt_ch1-0.3), max(volt_ch1+0.3), 250),
             [0 for _ in range(250)]
             , color='black')
    plt.plot([0 for _ in range(250)],
             np.linspace(min(volt_ch2-0.3), max(volt_ch2+0.3), 250)
             , color='black')
    plt.grid(True)
    plt.xlim(min(volt_ch1-0.08), max(volt_ch1+0.08))
    plt.ylim(min(volt_ch2-0.001), max(volt_ch2+0.001))
    plt.legend()
    plt.tight_layout()
    # plt.savefig(f"/Users/tomerpeker/hebrew_uni_project/lab_b_1/images/metal_{number}_vx_vs_vc.png")
plt.show()
