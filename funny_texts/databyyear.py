# количество стран с данными по годам

import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных
df_exp = pd.read_csv('funny_data/gdp_expenditure_shares.csv', sep=';')
df_main = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Подсчет ненулевых значений по годам для каждого показателя
counts = pd.DataFrame({
    'GII': df_main.groupby('year')['gii'].apply(lambda x: x[x != 0].count()),
    'Спорт и отдых': df_exp.groupby('year')['expenditure_sport_recreation'].apply(lambda x: x[x != 0].count()),
    'Здравоохранение': df_exp.groupby('year')['expenditure_health'].apply(lambda x: x[x != 0].count()),
    'Образование': df_exp.groupby('year')['expenditure_education'].apply(lambda x: x[x != 0].count())
})

# Создание столбчатой диаграммы
plt.figure(figsize=(15, 8))
bar_width = 0.2
index = range(len(counts.index))

for i, column in enumerate(counts.columns):
    plt.bar([x + i * bar_width for x in index], 
            counts[column], 
            bar_width, 
            label=column,
            alpha=0.8)

plt.title('Количество ненулевых значений по годам')
plt.xlabel('Год')
plt.ylabel('Количество стран с данными')
plt.legend()
plt.grid(True, axis='y')

# Настройка меток оси X
plt.xticks([x + bar_width * 1.5 for x in index], 
           counts.index, 
           rotation=45)

# Настройка отступов
plt.tight_layout()

plt.show()