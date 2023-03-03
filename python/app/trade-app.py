import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from typing import List 
from streamlit_searchbox import st_searchbox
import polars as pl

def main(): 
    st.title("Trading Partners by Country")
    st.sidebar.title("Country Code")
    st.markdown("Explore countries and their trading partners")

    st.cache(persist=True)
    def load_data():     
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

        # Drop population
        #pop_data = pop_data.drop(columns=['pop_2020'])

        #labelled_df = labelled_df.merge(pop_data, left_on='location_code', right_on='Country Code', how='inner')

        # Drop the following columns: year, location_id, partner_id, export_value, parent_code, description, code, product_code
        labelled_df = labelled_df.drop(columns=['year', 'location_id','product_id','sitc_eci','sitc_coi', 'sitc_product_code', 'partner_id','location_code', 'export_value', 'parent_code', 'code'])
        
        return labelled_df
    
    data = load_data()
    # Implement selector for state 
    print(data.head(10))

    # Implement selector for location_code 
    location_code = st.sidebar.selectbox('Exporter', data['Country Name'].unique())

    # Implement selector for description 
    #description = st.sidebar.selectbox('Select description', data['description'].unique())

    data = data[data['Country Name'] == location_code]
    #data = data[data['description'] == description]

    # Select distinct location_code and use it in the title 
    location_code = data['Country Name'].unique()

    # Find the top 10 import_value by location_code and location_code
    data_top10 = data.sort_values(by='import_value', ascending=False).head(10)

    # Append location_code to the title
    #st.title('''Imports by ''' + str(location_code[0]) + ''' from ''' + str(location_code[0]) + ''' in 2020''')
    st.write(data_top10)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(data.head(20))


if __name__ == '__main__':
    main()