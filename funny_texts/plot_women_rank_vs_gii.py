import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных с указанием кодировки
df = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Фильтрация необходимых столбцов
df = df[['country', 'iso', 'gii', 'women_rank', 'year']]

# Преобразование данных
df['gii'] = pd.to_numeric(df['gii'].str.replace(',', '.'), errors='coerce')
df['women_rank'] = pd.to_numeric(df['women_rank'].str.replace(',', '.'), errors='coerce')

# Удаление строк с отсутствующими значениями
df = df.dropna()

# Фильтрация данных только за 2020 год
df_2020 = df[df['year'] == 2020]

# Удаление строк с нулевыми значениями
df_2020 = df_2020[(df_2020['gii'] != 0) & (df_2020['women_rank'] != 0)]

# Построение графика
plt.figure(figsize=(12, 8))
plt.scatter(df_2020['gii'], df_2020['women_rank'], alpha=0.6)

# Подпись стран-выбросов
outliers = df_2020[df_2020['women_rank'] > 100]  # Пример условия для выбросов
for i, row in outliers.iterrows():
    plt.annotate(row['country'], (row['gii'], row['women_rank']), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Зависимость женского рейтинга от GII за 2020 год')
plt.xlabel('GII')
plt.ylabel('Женский рейтинг')
plt.grid(True)
plt.show() 