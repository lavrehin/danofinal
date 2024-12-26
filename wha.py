import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
main_football_data = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Преобразование столбцов 'gii', 'men_rank' в числовой формат
main_football_data['gii'] = pd.to_numeric(main_football_data['gii'].str.replace(',', '.'), errors='coerce')
main_football_data['men_rank'] = pd.to_numeric(main_football_data['men_rank'], errors='coerce')

# Подготовка данных для анализа, убираем только нули в 'men_rank' и фильтруем только за 2020 год
gii_gdp = main_football_data[main_football_data['year'] == 2020][['country', 'gii', 'gdp', 'men_rank']]
gii_gdp = gii_gdp[gii_gdp['men_rank'].notna()].sort_values('gdp')
gii_gdp = gii_gdp[gii_gdp['men_rank'] != 0]  # Убираем только нули в 'men_rank'

# Проверка на наличие всех стран
all_countries = main_football_data['country'].unique()
missing_countries = set(all_countries) - set(gii_gdp['country'].unique())
if missing_countries:
    print(f"Отсутствуют данные для следующих стран: {missing_countries}")

# Проверка на наличие некорректных значений
initial_count = gii_gdp.shape[0]
gii_gdp = gii_gdp[gii_gdp['gii'].notna() & gii_gdp['men_rank'].notna()]
final_count = gii_gdp.shape[0]
print(f"Удалено {initial_count - final_count} некорректных значений.")

plt.figure(figsize=(14, 14))  # Создаем фигуру для всех графиков

# Графики для мужского рейтинга
k = 0
for x in np.array_split(gii_gdp, 4):
    Q_3 = np.quantile(gii_gdp['gii'], 0.75)
    Q_1 = np.quantile(gii_gdp['gii'], 0.25)
    Q_r = Q_3 - Q_1

    q = x[(Q_1 - Q_r * 1.5 <= x['gii']) & (x['gii'] <= (Q_3 + Q_r * 1.5))]

    # Проверка, есть ли достаточно данных для построения графика
    if not q.empty and len(q) > 1:
        plt.subplot(2, 2, k + 1)  # Размещаем график в сетке 2x2
        sns.regplot(x='gii', y='men_rank', data=q[['men_rank', 'gii']], line_kws=dict(color="r"))
        plt.title(f'gii vs men_rank {k + 1}', fontsize=14)
        plt.xlabel('gii', fontsize=12)
        plt.ylabel('men_rank', fontsize=12)
        plt.grid(True)

        # Определение выбросов
        outliers = q[(q['men_rank'] > (Q_3 + 1.5 * Q_r)) | (q['men_rank'] < (Q_1 - 1.5 * Q_r))]

        # Подпись выбросов
        for i in range(len(outliers)):
            plt.annotate(outliers['country'].iloc[i], (outliers['gii'].iloc[i], outliers['men_rank'].iloc[i]), 
                         textcoords="offset points", xytext=(0, 10), ha='center')

        k += 1
    else:
        print(f"Недостаточно данных для построения графика {k + 1}.")

plt.tight_layout()  # Автоматически подгоняет графики
plt.show()
