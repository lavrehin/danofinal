import pandas as pd

# Создаем словари для хранения данных за каждый год
data_2014 = {}
data_2020 = {}

# Читаем файл и извлекаем нужные данные
with open('funny_data/merged_data.csv', 'r') as file:
    for line in file:
        parts = line.strip().split(';')
        if len(parts) >= 7:  # Проверяем, что строка содержит достаточно элементов
            iso = parts[1]
            year = parts[2]
            gii = parts[6]
            
            # Проверяем, что GII не пустой
            if gii and gii != '':
                try:
                    gii = float(gii.replace(',', '.'))  # Заменяем запятую на точку
                    if year == '2014':
                        data_2014[iso] = gii
                    elif year == '2020':
                        data_2020[iso] = gii
                except ValueError:
                    continue

# Создаем список всех уникальных ISO кодов
all_iso = sorted(set(data_2014.keys()) | set(data_2020.keys()))

# Создаем список данных для датафрейма
data = []
for iso in all_iso:
    gii_2014 = data_2014.get(iso, '')
    gii_2020 = data_2020.get(iso, '')
    
    # Вычисляем абсолютную разницу только если есть оба значения
    abs_diff = ''
    if gii_2014 != '' and gii_2020 != '':
        abs_diff = abs(gii_2020 - gii_2014)
    
    data.append([iso, gii_2014, gii_2020, abs_diff])

# Создаем датафрейм
df = pd.DataFrame(data, columns=['iso', 'gii2014', 'gii2020', 'abs_diff'])

# Сохраняем результат в файл
df.to_csv('gii_comparison.csv', sep=';', index=False)

# Выводим топ 15 стран с наибольшей разницей
print("\nТоп 15 стран с наибольшей разницей GII между 2014 и 2020:")
print(df[df['abs_diff'] != ''].sort_values('abs_diff', ascending=False).head(15))
