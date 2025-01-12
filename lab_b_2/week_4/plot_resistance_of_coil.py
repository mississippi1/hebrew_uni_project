import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel(r"raw_data/first_experiment/baseline_coil.xlsx").iloc[:12,]
plt.rcParams['font.size'] = 16  # Set default size
X_VALUES = "V"
Y_VALUES = "B"
plt.scatter(data[X_VALUES], data[Y_VALUES])
coefficients = np.polyfit(x=data[X_VALUES], y=data[Y_VALUES], deg=1)
EXPECTED_RESISTANCE = coefficients[0]


values_ = np.array([x * EXPECTED_RESISTANCE for x in data[X_VALUES].values])
ss_res = np.sum((values_ - data[Y_VALUES]) ** 2)  # Residual sum of squares
ss_tot = np.sum((values_ - np.mean(values_)) ** 2)  # Total sum of squares
r_squared = 1 - (ss_res / ss_tot)  # R-squared formula
fit_equation = f"y = {coefficients[0]:.3}x + {coefficients[1]:.3}, R^2  = {r_squared:.3f}"
plt.plot(data[X_VALUES], values_,
         label=fit_equation, color="green")
DELTA = 1.5

plt.legend()
plt.xlabel('Voltage (V)')
plt.ylabel('B (G)')
plt.legend()
plt.grid(True)
plt.show()
