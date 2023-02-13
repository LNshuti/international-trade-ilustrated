# Use python to plot treemaps of exports by country and by product

import pyarrow.parquet as pq
import pandas as pd
import squarify
import matplotlib.pyplot as plt

# Read in the data
product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')
print(product_labs.head())

# Read in the data
trade_data_all_years = pq.ParquetDataset('../data/trade_data_all_years.parquet').read_pandas().to_pandas()
print(trade_data_all_years.head())
