# Use python to plot treemaps of exports by country and by product

import pyarrow.parquet as pq
import pandas as pd
import squarify
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
labelled_df = labelled_df[labelled_df['location_code'].isin(['USA', 'CHN', 'RUS'])]

# Summarize the trade_balance by location_code and product_description
labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'description'])['trade_balance'].sum().reset_index()

# Filter to the top 10 products by trade balance for CHN 
china_df = labelled_df[labelled_df['location_code'] == 'CHN'].sort_values(by='trade_balance', ascending=False).head(10)

# Using squarify to plot treemaps
# Save plot as png file
plt.figure(figsize=(8,6))
# Plot the treemap
squarify.plot(sizes=china_df['trade_balance'], label=china_df['parent_code'], alpha=.8 )
# Remove the axis
plt.axis('off')
# # Save the plot as a png file
# plt.savefig('../output/china_exports_treemap.png', bbox_inches='tight')

# Increase font size for the text in the table 

plt.figure(figsize=(8,6))
cell_text = []
for row in china_df.iterrows():
    cell_text.append([row[1]['parent_code'], row[1]['description']])
    # set font size for the table
    
# Create the table
plt.table(cellText=cell_text, colLabels=['SITC Code', 'Description'], loc='bottom')

#plt.rcParams.update({'font.size': 10})
# save the plot as a png file
plt.savefig('../output/china_exports_tab.png', bbox_inches='tight')

# Save the plot as a png file
#dfi.export(df_styled,"../output/china_exports_table.png")


#dfi.export(df_styled,"../output/china_exports_table.png")
#dfi.export(df_styled,"../output/china_exports_labels.png")


# # Filter to the top 10 products by trade balance for CHN 
# usa_df = labelled_df[labelled_df['location_code'] == 'USA'].sort_values(by='trade_balance', ascending=False).head(10)

# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=usa_df['trade_balance'], label=usa_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# plt.savefig('../output/usa_exports_treemap.png', bbox_inches='tight')

# print(usa_df.head(10))


# # Filter to the top 10 products by trade balance for CHN 
# rus_df = labelled_df[labelled_df['location_code'] == 'RUS'].sort_values(by='trade_balance', ascending=False).head(10)

# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=rus_df['trade_balance'], label=rus_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# plt.savefig('../output/russia_exports_treemap.png', bbox_inches='tight')

# print(rus_df.head(10))


