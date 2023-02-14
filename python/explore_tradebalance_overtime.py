import polars as pl

# Define function that loads data in parquet format 
def load_data(filename):
    return pl.read_parquet(filename) 

# Write the main function 
def main():
    # Load the data 
    # Iterate through all years and load parquet files from 2000 to 2020 
    trade_data_all_years = pl.DataFrame()
    for year in range(2000, 2021):
        # Load the data
        trade_data = load_data(f'../data/country_partner_sitcproduct4digit_year_{year}.parquet')
        # Convert the export_value and import_value columns to numeric
        trade_data = trade_data.with_columns([
            pl.col('export_value').cast(pl.Float64),
            pl.col('import_value').cast(pl.Float64)
        ])
        # Calculate the trade balance
        trade_data = trade_data.with_column(
            pl.col('trade_balance').alias('export_value') - pl.col('import_value')
        )
        # Append the data to the trade_data_all_years dataframe
        trade_data_all_years = trade_data_all_years.append(trade_data)

    # Load the product labels 
    product_labs = pl.read_csv('../data/sitc_product_labels.csv')
    # Merge the trade data with the product labels 
    labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')
    # Filter to the USA, CHN, and RUS (China, Russia, and the United States)
    labelled_df = labelled_df.filter(pl.col('location_code').isin(['USA', 'CHN', 'RUS']))
    # Summarize the trade_balance by location_code and product_description
    labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'description']).agg([
        pl.sum(pl.col('trade_balance')).alias('trade_balance')
    ]).reset_index()
    # Filter to the top 10 products by trade balance for CHN 
    usa_df = labelled_df.filter(pl.col('location_code') == 'RUS').sort(pl.col('trade_balance'), reverse=True)
    # Select unique values from the parent_code and description columns 
    usa_df = usa_df.select(['parent_code', 'description']).distinct()
    # Filter to the top 10 products by trade balance for CHN 
    usa_df = usa_df.filter(pl.col('parent_code').isin(['0342']))
    # Print the top 10 products by trade balance for CHN 
    print(usa_df)

# Call the main function
if __name__ == '__main__':
    main()