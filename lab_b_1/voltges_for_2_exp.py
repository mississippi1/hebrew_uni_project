import os
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"


def func(file_name_input):
    a = []
    data = pd.read_excel(file_name_input, sheet_name=0)
    volt_ch1 = data['Volt Channel 1 (V)']
    volt_ch2 = data['Volt Channel 2 (V)']
    plt.xlabel(f'Voltage {ALPHA} E (V)')
    plt.ylabel(f'Permeability (H/m)')
    plt.title(f'Permeability As a Function of Voltage')
    plt.grid(True)
    a.append(
        (min(volt_ch1), min(volt_ch2), max(volt_ch1), max(volt_ch2))
    )
    return a


for num, color in [[2, "blue"], [4, "red"]]:
    metal_type = f'Metal {num}'
    for file_name in sorted(list(i for i in os.listdir('/Users/tomerpeker/Downloads/lab_b_1/%s/' % metal_type))):
        if file_name.endswith(".xlsx"):
            t = func(file_name_input="/Users/tomerpeker/Downloads/lab_b_1/" + metal_type + "/" + file_name)
            plt.scatter(
                y=[i[2] / i[3] for i in t],
                x=[i[3] for i in t],
                color=color,
                marker='*',
                label=metal_type
            )
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))  # Remove duplicates
plt.legend(by_label.values(), by_label.keys(), title="Metals", loc="upper right")
plt.ylim(0, 14)
plt.xlim(0, 0.05)
plt.show()
