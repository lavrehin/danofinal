import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных из файла main_football.csv
main_football_data = pd.read_csv('funny_data/MAIN_football.csv', sep=';', encoding='latin1')

# Преобразование столбцов в числовой формат
main_football_data['men_rank'] = pd.to_numeric(main_football_data['men_rank'].str.replace(',', '.'), errors='coerce')
main_football_data['women_rank'] = pd.to_numeric(main_football_data['women_rank'].str.replace(',', '.'), errors='coerce')
main_football_data['gdp'] = pd.to_numeric(main_football_data['gdp'].str.replace(',', '.'), errors='coerce')
main_football_data['gii'] = pd.to_numeric(main_football_data['gii'].str.replace(',', '.'), errors='coerce')

# Удаление строк с нулевыми значениями
filtered_data = main_football_data[(main_football_data['men_rank'] != 0) & 
                                    (main_football_data['women_rank'] != 0) & 
                                    (main_football_data['gdp'] != 0) & 
                                    (main_football_data['gii'] != 0)]

# Предполагается, что у вас есть DataFrame с данными
data = {
    'men_rank': filtered_data['men_rank'].tolist(),  # ваши данные
    'women_rank': filtered_data['women_rank'].tolist(),  # ваши данные
    'gdp': filtered_data['gdp'].tolist(),  # ваши данные
    'gii': filtered_data['gii'].tolist()  # ваши данные
}

df = pd.DataFrame(data)

# Вычисление матрицы корреляций
correlation_matrix = df[['men_rank', 'women_rank', 'gdp', 'gii']].corr()

# Построение тепловой карты
plt.figure(figsize=(10, 8))
plt.gcf().set_facecolor('#E1D4C1')  # Установка цвета фона вокруг тепловой карты
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar_kws={'label': 'Корреляция'})
plt.title('Матрица корреляций', fontsize=16)
plt.show()