import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.read_csv("/Users/tomerpeker/Downloads/Combined_Fifth_Columns_Data.csv")


for col in data.columns:
    if col != "time" and col != "2_metal":
        plt.plot(data["time"], data[col], label=col.replace("_", " ")+"s")
        plt.legend()
        print(col)
plt.xlim(min(data["time"]), max(data["time"]))
metal_ = "16_metal"
plt.ylim(-0.45, 0.45)
plt.plot(np.linspace(min(data[metal_]) - 0.3, max(data[metal_]) + 0.3, 250),
         [0 for _ in range(250)], color='black')
plt.plot([0 for _ in range(250)], np.linspace(min(data[metal_]) - 0.3, max(data[metal_]) + 0.3, 250)
         , color='black')
plt.title("Voltage as a Function of Number of Metal Plates")
plt.xlabel("Time [s]")
plt.ylabel("Voltage [V]")
plt.show()
