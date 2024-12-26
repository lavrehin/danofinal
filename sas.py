import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import numpy as np

# Загрузка данных
main_football_data = pd.read_csv("/funny_data/MAIN_football.csv", sep=';', encoding='ISO-8859-1')
gdp_data = pd.read_csv("/funny_data/gdp_expenditure_shares.csv", sep=';', encoding='ISO-8859-1')

# Объединение данных по country и year
merged_data = pd.merge(main_football_data, gdp_data, on=['country', 'year'], how='inner')

# Фильтрация данных только за 2021 год
merged_data = merged_data[merged_data['year'] == 2021]

# Преобразование столбцов в числовой формат
for column in ['men_rank', 'women_rank', 'gii']:
    merged_data[column] = merged_data[column].astype(str).str.replace(',', '.')
    merged_data[column] = pd.to_numeric(merged_data[column], errors='coerce')

# Удаление строк с нулевыми значениями
merged_data = merged_data[(merged_data[['men_rank', 'women_rank', 'gii']] != 0).all(axis=1)]

# Проверка на наличие NaN значений и их удаление
merged_data = merged_data.dropna()

# Вычисление корреляции
correlation_matrix = merged_data[['men_rank', 'women_rank', 'gii']].corr()

# Визуализация матрицы корреляций
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True)
plt.title('Матрица корреляций за 2021 год (без нулей и NaN)')
plt.show()

# Регрессионный анализ для men_rank
X_men_2021 = merged_data[['gii']]
y_men_2021 = merged_data['men_rank']

X_men_2021 = sm.add_constant(X_men_2021)
model_men_2021 = sm.OLS(y_men_2021, X_men_2021).fit()

# Вывод результатов модели
model_men_2021_summary = model_men_2021.summary()
print(model_men_2021_summary)