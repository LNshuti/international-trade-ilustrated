import polars as pl

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

        print(trade_data.schema)
        print(trade_data.head())

        print("\n")
        #trade_data_all_years = pl.concat(trade_data)

    #print(trade_data_all_years)

# Call the main function
if __name__ == '__main__':
    main()