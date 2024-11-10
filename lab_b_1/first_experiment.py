import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10


file_path = '/Users/tomerpeker/Downloads/must_poular_1.xlsx'
data = pd.read_excel(file_path, sheet_name=0)
# Extract columns for each channel
time_ch1 = data['Time (s)']
volt_ch1 = data['Volt Channel 1 (V)']
volt_ch2 = data['Volt Channel 2 (V)']

# Plot Channel 1
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(time_ch1, volt_ch1, label='Channel 1', color='blue')
plt.xlabel('Time (s)')
plt.ylabel('Vx (V)')
plt.title('Vx over Time')

plt.legend()

# Plot Channel 2
plt.subplot(2, 2, 2)
plt.plot(time_ch1, volt_ch2, label='Channel 2', color='red')
plt.xlabel('Time (s)')
plt.ylabel('Vc (V)')
plt.title('Vc over Time')
plt.legend()
plt.show()

plt.plot(volt_ch1.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
         volt_ch2.groupby(data.index // COEFFICIENT_TO_SMOOTH_LINES).sum().reset_index(drop=True) / COEFFICIENT_TO_SMOOTH_LINES,
         label='Vx Vs Vc', color='purple')
plt.xlabel('Vx (V)')
plt.ylabel('Vc (V)')
plt.title('Vx Vs Vc')
plt.plot(np.linspace(min(volt_ch1-0.3), max(volt_ch1+0.3), 250),
         [0 for _ in range(250)]
         , color='black')
plt.plot([0 for _ in range(250)],
         np.linspace(min(volt_ch2-0.3), max(volt_ch2+0.3), 250)
         , color='black')
plt.grid(True)
plt.xlim(min(volt_ch1-0.001), max(volt_ch1+0.001))
plt.ylim(min(volt_ch2-0.001), max(volt_ch2+0.001))

plt.legend()


plt.tight_layout()
plt.show()
