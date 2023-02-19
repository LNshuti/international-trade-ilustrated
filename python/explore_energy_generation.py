import pyarrow.parquet as pq
import polars as pl
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
labelled_df = labelled_df[labelled_df['location_code'].isin(['RWA', 'BDI', 'UGA'])]
#print(labelled_df.head(10))

# Summarize the trade_balance by location_code and product_description
labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'partner_code', 'description'])['trade_balance'].sum().reset_index()

# Filter to the top 10 products by trade balance for CHN 
usa_df = labelled_df[labelled_df['location_code'] == 'RWA'].sort_values(by='trade_balance', ascending=False)

# Select unique values from the parent_code and description columns 
usa_df = usa_df[['parent_code','location_code', 'partner_code', 'description', 'trade_balance']].drop_duplicates()

# convert to polars dataframe
usa_df = pl.from_pandas(usa_df)
print(usa_df)
# usa_df = usa_df[usa_df['parent_code'].isin(['0342'])]

