import pyarrow.parquet as pq
import polars as pl
import pandas as pd
import squarify
import seaborn as sns
import matplotlib.pyplot as plt
import dataframe_image as dfi
import subprocess

# Read in the data
product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')

# Read in the data
trade_data_all_years = pq.ParquetDataset('../data/country_partner_sitcproduct4digit_year_2020.parquet').read_pandas().to_pandas()

trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')
#print(labelled_df.head(10))
# Filter location_code to the USA, CHN, and RUS (China, Russia, and the United States)
labelled_df = labelled_df[labelled_df['location_code'].isin(['RWA', 'BDI', 'UGA'])]
#print(labelled_df.head(10))

# Summarize the trade_balance by location_code and product_description
labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'partner_code', 'description'])['trade_balance'].sum().reset_index()

# Filter to the top 10 products by trade balance for CHN 
rwa_df = labelled_df[labelled_df['location_code'] == 'RWA'].sort_values(by='trade_balance', ascending=False)

# Select unique values from the parent_code and description columns 
rwa_df = rwa_df[['parent_code','location_code', 'partner_code', 'description', 'trade_balance']].drop_duplicates()

# Summarize the trade_balance by location_code and product_description
rwa_df = rwa_df.groupby(['location_code', 'partner_code', 'description'])['trade_balance'].sum().reset_index()

# Create a new variable trade_balance_millions to make the numbers more readable
rwa_df['trade_balance_millions'] = rwa_df['trade_balance'] / 1000000


# Filter to the top 10 products by trade balance for CHN 
top10 = rwa_df.sort_values(by='trade_balance', ascending=False).head(20)
 
# Make the font human readable 
sns.set(font_scale=1.1)
sns.set_style("whitegrid")
sns.catplot(x='trade_balance_millions', y='partner_code', data=top10, palette='Blues_d', kind='bar', height=6, aspect=0.8)
plt.title('')
plt.xlabel('Trade Balance in Million USD')
plt.ylabel('')
# Seaborn decreasethe font size of y labels 
plt.yticks(fontsize=8, color='grey')
#plt.show()
plt.savefig('../output/rwanda_top_trade_partners' + '.png', dpi=300, bbox_inches='tight')
# rwa_df = rwa_df[rwa_df['parent_code'].isin(['0342'])]

#Use python do download the data about what percentage of energy source is solar, versus coal, and other renewables and non renewables. I want data for the following countries: China, Russia, USA, Brazil, India, South Africa, and the ASEAN countries. Please also add Germany, France, and the UK.
#Write python code below
# use Copilot to write the code
# Path: python\explore_energy_generation.py
