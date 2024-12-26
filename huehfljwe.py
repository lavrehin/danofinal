import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
from scipy import stats

# Define the file path
file_path = 'funny_data/MAIN_football.csv'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} was not found.")

# Load the dataset with proper delimiter and decimal format
df = pd.read_csv(file_path, delimiter=';', decimal=',')

# Filter out rows with zero or missing values for gii and gdp
df_filtered = df[(df['gii'] > 0) & (df['gdp'] > 0)]

# Define power-law function
def power_law(x, a, b):
    return a * x ** b

# Use GII as the independent variable and GDP as the dependent variable
x_data = df_filtered['gii'].values
y_data = df_filtered['gdp'].values

# Perform power-law curve fitting
params, _ = curve_fit(power_law, x_data, y_data, maxfev=10000)
y_pred = power_law(x_data, *params)
r_squared = r2_score(y_data, y_pred)

# Calculate statistical metrics
log_x = np.log(x_data)
log_y = np.log(y_data)
slope, intercept, r_value, p_value, std_err = stats.linregress(log_x, log_y)
f_stat = (r_value**2 / (1 - r_value**2)) * (len(x_data) - 2)

# Sort data for plotting
sorted_indices = np.argsort(x_data)
x_sorted = x_data[sorted_indices]
y_sorted = y_data[sorted_indices]
y_fit_sorted = power_law(x_sorted, *params)

# Plot the data points and the power-law regression line
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, color='blue', label='Данные', alpha=0.5)
plt.plot(x_sorted, y_fit_sorted, color='red', linewidth=2, 
         label=("Регрессионная кривая\n"
                f"R² = {r_squared:.4f}"))

plt.title('Зависимость GII и GDP')
plt.xlabel('GII')
plt.ylabel('GDP')
plt.grid(True, linestyle="--", linewidth=0.5)
plt.legend()
plt.show()
