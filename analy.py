import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Импортируем seaborn для линейной регрессии

# Загрузка данных из CSV файла
data = pd.read_csv('main_football_updated.csv', sep=';')

# Преобразование столбцов 'gii' и 'men_rank' в числовой формат
data['gii'] = data['gii'].str.replace(',', '.').astype(float)
data['men_rank'] = data['men_rank'].str.replace(',', '.').astype(float)

# Установка процента для фильтрации топ стран
top_percentage = 0.80  # Измените это значение для изменения процента (например, 0.80 для 20%)

# Фильтрация данных за 2021 год и топ стран по абсолютному ВВП
data_2021 = data[data['year'] == 2021]
top_countries = data_2021[data_2021['absolutegdp'] >= data_2021['absolutegdp'].quantile(top_percentage)]

# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(top_countries['gii'], top_countries['men_rank'], alpha=0.7)

# Добавление подписей стран
for i in range(len(top_countries)):
    plt.annotate(top_countries['country'].iloc[i], 
                 (top_countries['gii'].iloc[i], top_countries['men_rank'].iloc[i]), 
                 textcoords="offset points", 
                 xytext=(0,5), 
                 ha='center', fontsize=8)

# Наложение линейной регрессии
sns.regplot(x='gii', y='men_rank', data=top_countries, scatter=False, color='red', line_kws={"label": "Линейная регрессия"})

plt.title(f'Зависимость men_rank от gii для топ {int((1-top_percentage) * 100 + 1)}% стран по абсолютному ВВП за 2021 год')
plt.xlabel('GII')
plt.ylabel('Men Rank')

# Установка единичных отрезков
plt.xticks(ticks=[round(x * 0.1, 1) for x in range(int(top_countries['gii'].min() * 10), int(top_countries['gii'].max() * 10) + 1)])  # шаг 0.1
plt.yticks(ticks=range(int(top_countries['men_rank'].min()), int(top_countries['men_rank'].max()) + 250, 250))  # шаг 250

plt.grid()
plt.legend()
plt.show()
