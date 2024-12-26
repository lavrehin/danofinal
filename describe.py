import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
from matplotlib import font_manager

# Ensure the Inter font is available
font_path = 'Inter_18pt-Bold.ttf'  # Replace with the actual path to the Inter font file
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Inter'

# Load data from CSV file with specified encoding
df = pd.read_csv('funny_data/MAIN_football.csv', delimiter=';', encoding='ISO-8859-1')

# Replace commas with dots and convert to numeric format
columns_to_convert = ['gii', 'gdp', 'temp', 'men_rank', 'women_rank']
for column in columns_to_convert:
    df[column] = pd.to_numeric(df[column].str.replace(',', '.'), errors='coerce')

# Remove rows with missing values in the specified columns
df_cleaned = df.dropna(subset=columns_to_convert + ['year'])

# Describe the selected columns and round to two decimal places
description = df_cleaned[columns_to_convert + ['year']].describe().round(2)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 6))  # set size frame
ax.axis('tight')
ax.axis('off')

# Create a table with customized appearance
tbl = table(ax, description, loc='center', cellLoc='center', colWidths=[0.1]*len(description.columns))

# Customize the table appearance
tbl.auto_set_font_size(False)
tbl.set_fontsize(8)  # reduce font size
tbl.scale(1.2, 1.2)

# Set table styles
for key, cell in tbl.get_celld().items():
    cell.set_edgecolor('black')
    cell.set_linewidth(1.5)
    cell.set_facecolor('#E1D4C1')
    cell.set_text_props(color='#2C584B', fontproperties=font_manager.FontProperties(fname=font_path))
    if key[0] == 0:  # Header row
        cell.set_text_props(weight='bold', fontproperties=font_manager.FontProperties(fname=font_path))

# Save the table as a PNG file with a transparent background and higher resolution
plt.savefig('description_table.png', bbox_inches='tight', dpi=600, transparent=True)
plt.close()