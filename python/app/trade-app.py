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

        trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
        trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
        trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

        labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')

        # Drop the following columns: year, location_id, partner_id, export_value, parent_code, description, code, product_code
        labelled_df = labelled_df.drop(columns=['year', 'location_id', 'partner_id', 'export_value', 'parent_code', 'code'])
        
        return labelled_df
    
    data = load_data()
    # Implement selector for state 
    location_code = st.sidebar.selectbox('Select location_code', data['location_code'].unique())

    # Implement selector for partner_code 
    partner_code = st.sidebar.selectbox('Select partner_code', data['partner_code'].unique())

    # Implement selector for description 
    description = st.sidebar.selectbox('Select description', data['description'].unique())
    
    data = data[data['location_code'] == location_code]
    data = data[data['partner_code'] == partner_code]
    data = data[data['description'] == description]

    # Find the top 10 export_value by location_code and partner_code
    data = data.sort_values(by='export_value', ascending=False).head(10)

    st.write(data)
    # Plot a histogram of the total award 
     
    # Select distinct location_code and use it in the title 
    location_code = data['location_code'].unique()
    partner_code = data['partner_code'].unique()

    # Append location_code to the title
    st.title('''Imports by ''' + str(location_code[0]) + ''' from ''' + str(partner_code[0]) + ''' in 2020''')

    # Calculate sum of import_value by location_code and partner_code
    data = data.groupby(['location_code', 'partner_code', 'sitc_product_code', 'description']).sum().reset_index()

    fig, ax = plt.subplots()
    ax.hist(data['import_value'])
    ax.set_xlabel('Imports ($Millions)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(data.head(20))


if __name__ == '__main__':
    main()