import os
import pandas as pd
import matplotlib.pyplot as plt

COEFFICIENT_TO_SMOOTH_LINES = 10
ALPHA = "\u03B1"


def get_value_per_operation(volt_ch1: pd.Series, operation: callable) -> int:
    return max(volt_ch1[volt_ch1 == operation(volt_ch1)].index)


def calculate_gradient(series: pd.Series, index: int) -> int:
    return series[index - 5] - series[index]


def func(file_name_input):
    a = []
    data = pd.read_excel(file_name_input, sheet_name=0)
    volt_ch1 = data['Volt Channel 1 (V)']
    volt_ch2 = data['Volt Channel 2 (V)']
    plt.xlabel(f'Voltage {ALPHA} H (V)')
    plt.ylabel(f'Permeability (H/m)')
    plt.title(f'Permeability As a Function of Voltage')
    plt.grid(True)
    index_of_min = get_value_per_operation(volt_ch1=volt_ch1, operation=min)
    index_of_max = get_value_per_operation(volt_ch1=volt_ch1, operation=max)
    a.append(
        (volt_ch1[index_of_min], volt_ch2[index_of_min], volt_ch1[index_of_max], volt_ch2[index_of_max])
    )
    return a


for num, color in [[1, "green"], [2, "blue"], [4, "red"]]:
    metal_type = f'Metal {num}'
    max_y_vals = 0
    for file_name in sorted(list(i for i in os.listdir('/Users/tomerpeker/Downloads/lab_b_1/%s/' % metal_type))):
        if file_name.endswith(".xlsx"):
            t = func(file_name_input="/Users/tomerpeker/Downloads/lab_b_1/" + metal_type + "/" + file_name)
            y_vals = [i[2] / i[3] for i in t]
            print(metal_type, metal_type, max(y_vals))
            max_y_vals = max(max_y_vals, max(y_vals))
            plt.scatter(
                y=y_vals,
                x=[i[3] for i in t],
                color=color,
                marker='*',
                label=metal_type
            )
    plt.title(f"{metal_type} - Permeability As a Function of Voltage")
    plt.ylim(0, max_y_vals+2)
    plt.show()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Remove duplicates
    # plt.legend(by_label.values(), by_label.keys(), title="Metals", loc="upper right")
    print(metal_type, max_y_vals)
    plt.close()
plt.show()
