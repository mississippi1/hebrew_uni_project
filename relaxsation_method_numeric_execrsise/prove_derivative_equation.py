import numpy as np
import matplotlib.pyplot as plt
import jit


# Define the function and its true derivative
def f(x):
    return np.cos(x)


def true_derivative(x):
    return -np.sin(x)


# Define the point at which we will approximate the derivative
x = 1.0

# Create a range of h values
h_values = np.logspace(-1, -15, 100)

# Compute the errors for the regular difference quotient and the central difference quotient
regular_errors = []
central_errors = []

for h in h_values:
    regular_approx = (f(x + h) - f(x)) / h
    central_approx = (f(x + h) - f(x - h)) / (2 * h)
    true_value = true_derivative(x)

    regular_errors.append(np.abs(regular_approx - true_value))
    central_errors.append(np.abs(central_approx - true_value))
    if h < 1*10**-5:
        print(np.abs(central_approx - true_value))


# Plot the errors
plt.figure(figsize=(10, 6))
plt.loglog(h_values, regular_errors, label='Regular Difference Quotient', marker='o')
plt.loglog(h_values, central_errors, label='Central Difference Quotient', marker='x')
plt.xlabel('h')
plt.ylabel('Absolute Error')
plt.title('Comparison of Difference Quotients for Approximating the Derivative of cos(x)')
plt.legend()
plt.grid(True)
plt.show()
