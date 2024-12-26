import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('main_football_updated.csv', delimiter=';')

# Ensure 'gdp' column is of type string before replacing commas
df['gdp'] = df['gdp'].astype(str).str.replace(',', '.').astype(float)
df['TotalPopulation'] = df['TotalPopulation'].astype(int)

# Create a new column 'absolutegdp' by multiplying 'TotalPopulation' with 'gdp'
df['absolutegdp'] = (df['TotalPopulation'] * df['gdp']).round(0).astype(int)

# Save the updated DataFrame back to the CSV file
df.to_csv('main_football_updated.csv', index=False, sep=';')