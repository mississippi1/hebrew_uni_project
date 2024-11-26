import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ALPHA = "\u03B1"
data = pd.read_excel("/Users/tomerpeker/Downloads/Combined_Fifth_Columns_Data.xlsx")

legend_labels = {
    "blue": f"Vx {ALPHA} H",
    "red": f"Vc {ALPHA} B"
}
for col in data.columns:
    if col != "time" and col != "2_metal" and col.find("Unnamed") < 0:
        number_of_plates = col.replace("_metal", "").replace("_ch1", "").replace("_ch2", "")
        print(max(data[col]), int(number_of_plates))
        print(int(number_of_plates), max(data[col]))
        plt.scatter(int(number_of_plates), max(data[col]),
                    color="blue" if col.find("_ch1") > 0 else "red")
plt.legend([plt.Line2D([0], [0], color=color, marker='o', linestyle='')
            for color in legend_labels.keys()], legend_labels.values())
# plt.xlim(min(data["time"]), max(data["time"]))
# metal_ = "16_metal"
# plt.ylim(-0.45, 0.45)
# plt.plot(np.linspace(min(data[metal_]) - 0.3, max(data[metal_]) + 0.3, 250),
#          [0 for _ in range(250)], color='black')
# plt.plot([0 for _ in range(250)], np.linspace(min(data[metal_]) - 0.3, max(data[metal_]) + 0.3, 250)
#          , color='black')
plt.title("Voltage as a Function of Number of Metal Plates")
plt.xlabel(f"Number of Metal Plates {ALPHA} Area [#]")
plt.ylabel("Max Voltage [V]")
plt.show()
