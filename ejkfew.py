import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # Импортируем seaborn для боксплотов

# Загрузка данных из CSV файла
data = pd.read_csv('main_football_updated.csv', sep=';')

# Преобразование столбцов 'men_rank' в числовой формат
data['men_rank'] = data['men_rank'].str.replace(',', '.').astype(float)

# Фильтрация данных для Европы
european_countries = data[data['unicef_reg'] == 'EECA']  # Предполагается, что 'EECA' соответствует Европе

# Удаление нулей из men_rank
european_countries = european_countries[european_countries['men_rank'] != 0]

# Построение боксплота
plt.figure(figsize=(10, 6))
sns.boxplot(x='men_rank', data=european_countries, width=0.1)
plt.title('Боксплот men_rank для стран Европы (без нулей)')
plt.xlabel('Men Rank')
plt.grid()
plt.show()

# Фильтрация данных для женщин
women_countries = data[data['unicef_reg'] == 'EECA']  # Предполагается, что 'EECA' соответствует Европе

# Удаление нулей из women_rank
women_countries = women_countries[women_countries['women_rank'] != 0]

# Построение боксплота для женщин
plt.figure(figsize=(10, 6))
sns.boxplot(x='women_rank', data=women_countries, width=0.1)
plt.title('Боксплот women_rank для стран Европы (без нулей)')
plt.xlabel('Women Rank')
plt.grid()
plt.show()
