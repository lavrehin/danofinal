import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных с указанием кодировки
df = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Фильтрация необходимых столбцов
df = df[['country', 'iso', 'gii', 'women_rank', 'year', 'inc_group']]

# Преобразование данных
df['gii'] = pd.to_numeric(df['gii'].str.replace(',', '.'), errors='coerce')
df['women_rank'] = pd.to_numeric(df['women_rank'].str.replace(',', '.'), errors='coerce')

# Удаление строк с отсутствующими значениями
df = df.dropna()

# Фильтрация данных только за 2020 год
df_2020 = df[df['year'] == 2020]

# Удаление строк с нулевыми значениями
df_2020 = df_2020[(df_2020['gii'] != 0) & (df_2020['women_rank'] != 0)]

# Уникальные группы доходов
income_groups = df_2020['inc_group'].unique()

# Построение графиков для каждой группы доходов
plt.figure(figsize=(15, 10))
for income_group in income_groups:
    group_data = df_2020[df_2020['inc_group'] == income_group]
    
    # Построение графика
    plt.subplot(2, 2, list(income_groups).index(income_group) + 1)
    sns.regplot(x='gii', y='women_rank', data=group_data, scatter_kws={'alpha':0.6}, line_kws={'color':'red'})
    
    # Подпись стран-выбросов
    outliers = group_data[group_data['women_rank'] > 100]  # Пример условия для выбросов
    for i, row in outliers.iterrows():
        plt.annotate(row['country'], (row['gii'], row['women_rank']), textcoords="offset points", xytext=(0,10), ha='center')

    plt.title(f'Зависимость женского рейтинга от GII ({income_group}) за 2020 год')
    plt.xlabel('GII')
    plt.ylabel('Женский рейтинг')
    plt.grid(True)

plt.tight_layout()
plt.show() 