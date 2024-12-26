import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Загрузка данных из файла main_football.csv с игнорированием ошибочных строк и указанием разделителя
data = pd.read_csv('funny_data/main_football.csv', sep=';', on_bad_lines='skip')

# Замена запятых на точки и преобразование в числовой формат
data['gii'] = data['gii'].str.replace(',', '.').astype(float)
data['gdp'] = data['gdp'].str.replace(',', '.').astype(float)

# Вывод списка столбцов для диагностики
print(data.columns)

GII = data['gii'].values  # Замена на реальные столбцы из файла
GDP = data['gdp'].values

# Функция для аппроксимации вида 1/x
def inv_func(x, a, b):
    return a / x + b

# Подгонка функции 1/x
params, _ = curve_fit(inv_func, GII, GDP, maxfev=10000)

# Предсказания
GII_sorted = np.sort(GII)
GDP_pred = inv_func(GII_sorted, *params)

# Вычисление R^2
SS_res = np.sum((GDP - inv_func(GII, *params))**2)
SS_tot = np.sum((GDP - np.mean(GDP))**2)
r_squared = 1 - (SS_res / SS_tot)

# Вывод R^2
print(f'Коэффициент детерминации R^2: {r_squared:.4f}')

# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(GII, GDP, color='blue', alpha=0.6, label='Данные')
plt.plot(GII_sorted, GDP_pred, color='red', linewidth=3, label='Регрессия 1/x')
plt.xlabel('GII')
plt.ylabel('GDP')
plt.title('Регрессия вида 1/x: GII и GDP')
plt.legend()
plt.grid()
plt.show()
