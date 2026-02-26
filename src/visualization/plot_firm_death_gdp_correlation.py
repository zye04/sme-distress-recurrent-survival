import pandas as pd
import matplotlib.pyplot as plt
import os

# Define file paths using the new structure
RAW_DATA_PATH = '02_implementation/data/raw'
REPORTS_FIGURES_PATH = '02_implementation/reports/figures'

firm_data_path = os.path.join(RAW_DATA_PATH, 'deaths_births_survivors_firms.csv')
gdp_data_path = os.path.join(RAW_DATA_PATH, 'pib_growth.csv')

# Ensure the output directory exists
os.makedirs(REPORTS_FIGURES_PATH, exist_ok=True)

# --- 1. Load Data ---
df_firms = pd.read_csv(firm_data_path)
df_gdp = pd.read_csv(gdp_data_path)

# --- 2. Clean GDP Data ---
# Filter for Portugal data
df_gdp_portugal = df_gdp[df_gdp['02. Nome País (Europa)'] == 'Portugal'].copy()

# Select relevant columns and rename for clarity
df_gdp_portugal = df_gdp_portugal[['01. Ano', '09. Valor']]
df_gdp_portugal.rename(columns={'01. Ano': 'Year', '09. Valor': 'GDP_Growth'}, inplace=True)

# Convert GDP_Growth to numeric, handling potential non-numeric entries (like 'x' or 'Pro')
df_gdp_portugal['GDP_Growth'] = pd.to_numeric(df_gdp_portugal['GDP_Growth'], errors='coerce')

# Drop rows with NaN in GDP_Growth after conversion
df_gdp_portugal.dropna(subset=['GDP_Growth'], inplace=True)

# --- 3. Merge Data ---
# Merge on 'Year'
df_merged = pd.merge(df_firms, df_gdp_portugal, on='Year', how='inner')

# --- 4. Generate Plot ---
plt.figure(figsize=(12, 7))

# Plot Company Deaths
plt.plot(df_merged['Year'], df_merged['Deaths'], label='Company Deaths', marker='o', color='red')

# Create a second y-axis for GDP Growth
ax2 = plt.gca().twinx()
ax2.plot(df_merged['Year'], df_merged['GDP_Growth'], label='GDP Growth (%)', marker='x', color='blue', linestyle='--')

# --- Add correlation coefficient to plot ---
# Calculate correlation, excluding non-numeric columns and 'Year'
correlation = df_merged['Deaths'].corr(df_merged['GDP_Growth'])

# Add text for correlation
plt.text(0.05, 0.95, f'Correlation (Deaths vs. GDP Growth): {correlation:.2f}',
         transform=plt.gca().transAxes, fontsize=12, verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5))


plt.title('Company Deaths vs. GDP Growth in Portugal (2004-2022)')
plt.xlabel('Year')
plt.ylabel('Company Deaths', color='red')
ax2.set_ylabel('GDP Growth (%)', color='blue')

# Add legends for both y-axes
lines, labels = plt.gca().get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.grid(True)
plt.tight_layout()

# Save the plot
output_plot_path = os.path.join(REPORTS_FIGURES_PATH, 'firm_death_gdp_correlation.png')
plt.savefig(output_plot_path)

print(f"Plot saved to: {output_plot_path}")
