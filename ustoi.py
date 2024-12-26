import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
data = pd.read_csv('funny_data/MAIN_football.csv', sep=';')  # Убедитесь, что путь к файлу указан правильно

# Фильтрация данных по un_subreg для Южной Америки за 2021 год
south_america_data = data[(data['un_subreg'] == 'Central America') & (data['year'] == 2021)]
# Преобразование типов данных
south_america_data['gii'] = pd.to_numeric(south_america_data['gii'].str.replace(',', '.'), errors='coerce')
south_america_data['women_rank'] = pd.to_numeric(south_america_data['women_rank'].str.replace(',', '.'), errors='coerce')

# Удаление строк с нулевыми значениями в 'gii' и 'women_rank'
south_america_data = south_america_data.dropna(subset=['gii', 'women_rank'])
south_america_data = south_america_data[(south_america_data['gii'] != 0) & (south_america_data['women_rank'] != 0)]  # Удаление строк с нулями

# Проверка на пустоту данных
if south_america_data.empty:
    print("Нет данных для Южной Америки за 2021 год.")
else:
    # Сортировка данных по 'country'
    south_america_data = south_america_data.sort_values(by='country')  # Сортировка по названию страны

    # Построение графика
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='gii', y='women_rank', data=south_america_data)

    # Линейная регрессия
    slope, intercept = np.polyfit(south_america_data['gii'], south_america_data['women_rank'], 1)
    plt.plot(south_america_data['gii'], slope * south_america_data['gii'] + intercept, color='red')

    # Вычисление R^2
    y_pred = slope * south_america_data['gii'] + intercept
    r_squared = 1 - (np.sum((south_america_data['women_rank'] - y_pred) ** 2) / np.sum((south_america_data['women_rank'] - np.mean(south_america_data['women_rank'])) ** 2))

    # Вывод R^2
    print(f'Коэффициент детерминации R^2: {r_squared:.4f}')

    # Подписи стран
    for i, row in south_america_data.iterrows():
        plt.annotate(row['country'], (row['gii'], row['women_rank']), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

    # Добавление R^2 на график
    plt.text(0.05, 0.95, f'R² = {r_squared:.4f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')

    # Настройки графика
    plt.title('Зависимость GII от Women Rank для Центральной Америки за 2021 год')
    plt.xlabel('GII')
    plt.ylabel('Women Rank')
    plt.ylim(800, 2200)  # Установка пределов по оси Y
    plt.grid()
    plt.show()