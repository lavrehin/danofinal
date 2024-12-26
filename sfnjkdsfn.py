import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = "funny_data/MAIN_football.csv"
data = pd.read_csv(file_path, delimiter=';')

# Clean the data
# Strip spaces and replace commas if necessary
data['gii'] = data['gii'].str.replace(',', '.').str.strip()
data['men_rank'] = data['men_rank'].str.replace(',', '.').str.strip()
data['women_rank'] = data['women_rank'].str.replace(',', '.').str.strip()

# Convert to numeric
data['gii'] = pd.to_numeric(data['gii'], errors='coerce')
data['men_rank'] = pd.to_numeric(data['men_rank'], errors='coerce')
data['women_rank'] = pd.to_numeric(data['women_rank'], errors='coerce')

# Group by country and calculate the average for each country
df_avg = data.groupby('country')[['gii', 'men_rank', 'women_rank']].mean().dropna()

# Filter out zero values for men_rank and women_rank
df_avg_filtered = df_avg[(df_avg['men_rank'] > 0) & (df_avg['women_rank'] > 0)]

# Plot the combined graph with points only
plt.figure(figsize=(12, 6))

# Plot Men's Rank in blue
plt.plot(df_avg_filtered['gii'], df_avg_filtered['men_rank'], 'o', color='blue', label="Мужской рейтинг", alpha=0.7)

# Plot Women's Rank in red
plt.plot(df_avg_filtered['gii'], df_avg_filtered['women_rank'], 'o', color='red', label="Женский рейтинг", alpha=0.7)

# Add labels and title
plt.title("Индекс гендерного неравенства vs средние мужской и женский рейтинг")
plt.xlabel("Индекс гендерного неравенства")
plt.ylabel("Средний рейтинг ФИФА")
plt.legend()
plt.grid(True)
plt.show()
