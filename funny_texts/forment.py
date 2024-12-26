import pandas as pd
import matplotlib.pyplot as plt

COUNTRY_ISO = 'RUS' # сюды можно изошки вставлять и смотреть динамику

df = pd.read_csv('funny_data/merged_data.csv', sep=';')

numeric_columns = ['gii', 'expenditure_sport_recreation', 'expenditure_health', 
                  'expenditure_education', 'men_rank', 'women_rank']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col].str.replace(',', '.'), errors='coerce')

country_data = df[df['iso'] == COUNTRY_ISO][[
    'year', 'country', 'gii', 'expenditure_sport_recreation',
    'expenditure_health', 'expenditure_education', 'men_rank', 'women_rank'
]]

country_name = country_data['country'].iloc[0] if not country_data.empty else COUNTRY_ISO

print(f"Данные по стране {country_name}:")
print(country_data)

if not country_data.empty:
    country_data = country_data.sort_values('year')
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax3 = ax1.twinx()
    
    if country_data['gii'].notna().any():
        line1 = ax1.plot(country_data['year'], country_data['gii'], 
                        color='#FFD700', marker='o', label='GII')
        ax1.invert_yaxis()
    
    lines3 = []
    if country_data['men_rank'].notna().any():
        l5 = ax3.plot(country_data['year'], country_data['men_rank'], 
                     color='blue', marker='v', label='Рейтинг мужской сборной')
        lines3.extend(l5)
    
    if country_data['women_rank'].notna().any():
        l6 = ax3.plot(country_data['year'], country_data['women_rank'], 
                     color='red', marker='>', label='Рейтинг женской сборной')
        lines3.extend(l6)
    
    ax1.set_xlabel('Год', fontsize=12)
    ax1.set_ylabel('GII', color='#FFD700', fontsize=12)
    ax3.set_ylabel('Рейтинг ФИФА', color='blue', fontsize=12)
    
    ax1.tick_params(axis='y', labelcolor='#FFD700')
    ax3.tick_params(axis='y', labelcolor='blue')
    
    plt.title(f'Динамика показателей в стране {country_name}\n2003-2021', fontsize=14)
    
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    years = country_data['year'].unique()
    ax1.set_xticks(years)
    ax1.set_xticklabels(years, rotation=45)
    
    lines = line1 + lines3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.show()
else:
    print(f"\nв данных отсутствуют значения для страны с кодом {COUNTRY_ISO}")
