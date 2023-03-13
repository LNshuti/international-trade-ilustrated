import polars as pl
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split

# Define function that loads data in parquet format 
def load_data(filename):
    return pl.read_parquet(filename) 

# Create variable that holds the path to the data
data_path = 'D:\portfolio\dataverse-files\parquet'

# Write the main function 
def main():
    # Load the data 
    # Iterate through all years and load parquet files from 2000 to 2020 
    trade_data_all_years = pl.DataFrame()
    for year in range(2000, 2021):
        # Load the data
        trade_data = load_data(f'{data_path}/country_partner_sitcproduct4digit_year_{year}.parquet')
        #trade_data = load_data(f'../data/country_partner_sitcproduct4digit_year_{year}.parquet')
        # Convert the export_value and import_value columns to numeric
        trade_data = trade_data.with_columns([
            pl.col('export_value').cast(pl.Float64),
            pl.col('import_value').cast(pl.Float64),
            # cast year to factor 
            pl.col('year').cast(pl.Int32),
        ])

        trade_data_subset = trade_data.select(
            ['export_value','year', 'location_code','partner_code', 'sitc_product_code', 'sitc_eci', 'sitc_coi',  'import_value']
        )
        
        trade_data_all_years = pl.concat([trade_data], how='vertical')

    print(trade_data_all_years)
    trade_data_all_years.write_parquet(f'../data/processed/country_partner_sitcproduct4digit_year_all.parquet')



    Y=trade_data_all_years.iloc[:,0]
    X=trade_data_all_years.iloc[:, 1:6]
    ##TRANSFORMING Y:
    Y[Y >=0.5] = 1
    Y[Y <0.5] = 0
    x_train, x_test, y_train, y_test = train_test_split(trade_data_all_years.iloc[:, 1:6], trade_data_all_years.iloc[:,0],test_size = 0.25)
    x_train=x_train.replace([np.inf, -np.inf], 9999).dropna(axis=0)
    x_test=x_test.replace([np.inf, -np.inf], 9999).dropna(axis=0)

    print(x_train)
# Call the main function
if __name__ == '__main__':
    main()