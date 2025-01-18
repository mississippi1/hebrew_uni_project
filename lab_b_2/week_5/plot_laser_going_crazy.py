import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot


plt.rcParams['font.size'] = 19
data = pd.read_excel("../week_2/raw_data/quarter_wave/static_measurments.xlsx", skiprows=5)
plt.plot(data["Time (s)"], data["Current (A)"])
plt.xlabel("Time (s)")
plt.ylabel("I (A)")
plt.grid(True)
print((data["Current (A)"].max() - data["Current (A)"].min())/data["Current (A)"].min(), data["Current (A)"].std())
plt.show()
