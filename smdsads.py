import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
data = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Преобразование столбцов в числовой формат
data['gii'] = pd.to_numeric(data['gii'].str.replace(',', '.'), errors='coerce')
data['gdp'] = pd.to_numeric(data['gdp'].str.replace(',', '.'), errors='coerce')
data['women_rank'] = pd.to_numeric(data['women_rank'].str.replace(',', '.'), errors='coerce')

# Удаление строк с отсутствующими значениями и нулями
data = data.dropna(subset=['gii', 'gdp', 'women_rank'])
data = data[(data['gii'] != 0) & (data['gdp'] != 0) & (data['women_rank'] != 0)]

# Сортировка данных по GDP
data_sorted = data.sort_values(by='gdp')

# Разделение на квартели по GDP
data_sorted['gdp_quartile'] = pd.qcut(data_sorted['gdp'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])

# Построение графиков зависимости women_rank от gii для каждого квартиля
plt.figure(figsize=(15, 10))
for i, quartile in enumerate(data_sorted['gdp_quartile'].unique()):
    plt.subplot(2, 2, i + 1)
    subset = data_sorted[data_sorted['gdp_quartile'] == quartile]
    sns.scatterplot(x='gii', y='women_rank', data=subset, alpha=0.6)
    sns.regplot(x='gii', y='women_rank', data=subset, scatter=False, color='red')
    plt.title(f'Women Rank vs GII - {quartile}')
    plt.xlabel('GII')
    plt.ylabel('Women Rank')
    plt.grid()

plt.tight_layout()
plt.show()
