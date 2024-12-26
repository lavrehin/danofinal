import pandas as pd
import matplotlib.pyplot as plt

COUNTRY_ISO = 'QAT'

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
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    
    ax3.spines['right'].set_position(('outward', 60))
    
    if country_data['gii'].notna().any():
        line1 = ax1.plot(country_data['year'], country_data['gii'], 
                        color='red', marker='o', label='GII')
        ax1.invert_yaxis()
    
    lines2 = []
    if country_data['expenditure_sport_recreation'].notna().any():
        l2 = ax2.plot(country_data['year'], country_data['expenditure_sport_recreation'], 
                     color='blue', marker='s', label='Расходы на спорт')
        lines2.extend(l2)
    
    if country_data['expenditure_health'].notna().any():
        l3 = ax2.plot(country_data['year'], country_data['expenditure_health'], 
                     color='green', marker='^', label='Расходы на здравоохранение')
        lines2.extend(l3)
    
    if country_data['expenditure_education'].notna().any():
        l4 = ax2.plot(country_data['year'], country_data['expenditure_education'], 
                     color='purple', marker='D', label='Расходы на образование')
        lines2.extend(l4)
    
    lines3 = []
    if country_data['men_rank'].notna().any():
        l5 = ax3.plot(country_data['year'], country_data['men_rank'], 
                     color='orange', marker='v', label='Рейтинг мужской сборной')
        lines3.extend(l5)
    
    if country_data['women_rank'].notna().any():
        l6 = ax3.plot(country_data['year'], country_data['women_rank'], 
                     color='pink', marker='>', label='Рейтинг женской сборной')
        lines3.extend(l6)
    
    ax1.set_xlabel('Год', fontsize=12)
    ax1.set_ylabel('GII', color='red', fontsize=12)
    ax2.set_ylabel('Расходы (% ВВП)', color='blue', fontsize=12)
    ax3.set_ylabel('Рейтинг ФИФА', color='orange', fontsize=12)
    
    ax1.tick_params(axis='y', labelcolor='red')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax3.tick_params(axis='y', labelcolor='orange')
    
    plt.title(f'Динамика показателей в стране {country_name}\n2003-2021', fontsize=14)
    
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    years = country_data['year'].unique()
    ax1.set_xticks(years)
    ax1.set_xticklabels(years, rotation=45)
    
    lines = line1 + lines2 + lines3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    plt.show()
else:
    print(f"\nК сожалению, в данных отсутствуют значения для страны с кодом {COUNTRY_ISO}")
