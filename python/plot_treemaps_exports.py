# Use python to plot treemaps of exports by country and by product

import pyarrow.parquet as pq
import pandas as pd
import squarify
import matplotlib.pyplot as plt

# Read in the data
product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')
print(product_labs.head())

# Read in the data
trade_data_all_years = pq.ParquetDataset('../data/country_partner_sitcproduct4digit_year_2020.parquet').read_pandas().to_pandas()

trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')
print(labelled_df.head(10))
# Filter location_code to the USA, CHN, and RUS (China, Russia, and the United States)
labelled_df = labelled_df[labelled_df['location_code'].isin(['USA', 'CHN', 'RUS'])]

# Summarize the trade_balance by location_code and product_description
labelled_df = labelled_df.groupby(['location_code', 'parent_code'])['trade_balance'].sum().reset_index()

# Filter to the top 10 products by trade balance for CHN 
china_df = labelled_df[labelled_df['location_code'] == 'CHN'].sort_values(by='trade_balance', ascending=False).head(10)
print(china_df.head(10))

# Using squarify to plot treemaps
# Save plot as png file
plt.figure(figsize=(10,10))

# Plot the treemap
squarify.plot(sizes=china_df['trade_balance'], label=china_df['parent_code'], alpha=.8 )

# Remove the axis
plt.axis('off')

# Save the plot as a png file
plt.savefig('../output/china_exports_treemap.png', bbox_inches='tight')

# Select location_code and description
#labelled_df = labelled_df[['description', 'parent_code']]
print(china_df.head(10))


