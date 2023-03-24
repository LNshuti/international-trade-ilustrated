import pandas as pd
import pyarrow.parquet as pq
import matplotlib as mpl
import matplotlib.pyplot as plt


def load_transform_data():     
    
    # Read in the data
    product_labs = pd.read_csv('../../data/processed/SITCCodeandDescription.csv')

    # Read in the data
    trade_data_all_years = pq.ParquetDataset('../../data/country_partner_sitcproduct4digit_year_2020.parquet').read_pandas().to_pandas()

    # Import the population data  
    pop_data = pd.read_csv('../../data/processed/API_SP_POP_TOTL_DS2.csv', skiprows=4)
    pop_data = pop_data[['Country Code', 'Country Name', '2020']]
    # Rename 2020 to pop_2020
    pop_data = pop_data.rename(columns={'2020': 'pop_2020'})


    trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
    trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
    trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

    labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')

    # Join pop_data 
    labelled_df = labelled_df.merge(pop_data, left_on='location_code', right_on='Country Code', how='inner')

    # Drop Country Code 
    labelled_df = labelled_df.drop(columns=['Country Code'])

    # Keep only the following two columns from pop_data: Country Name, Country Code
    pop_data = pop_data[['Country Name', 'Country Code']]
    # Rename Country Name to Importer
    pop_data = pop_data.rename(columns={'Country Name': 'Importer'})

    #pop_data = pop_data.drop(columns=['pop_2020'])
    # From pop_data, keep only the following columns: Country Name, Country Code
    # Only keep uniuqe rows
    pop_data = pop_data[['Importer', 'Country Code']].drop_duplicates() 

    #labelled_df = labelled_df.merge(pop_data, left_on='location_code', right_on='Country Code', how='inner')

    # Drop the following columns: year, location_id, partner_id, export_value, parent_code, description, code, product_code
    # Drop rows with pop_2020 < 500000
    labelled_df = labelled_df[labelled_df['pop_2020'] > 500000]
    labelled_df = labelled_df.drop(columns=['year','pop_2020', 'location_id','product_id','sitc_eci','sitc_coi','location_code', 'export_value', 'parent_code', 'code'])
    #labelled_df = labelled_df.merge(pop_data, left_on='partner_code', right_on='Country Code', how='inner')
    
    print(labelled_df)
    return labelled_df
    
def main():
    data = load_transform_data()
    
    data.write_csv("processed_country_partner_df.csv")
    

if __name__ == '__main__':
    main()