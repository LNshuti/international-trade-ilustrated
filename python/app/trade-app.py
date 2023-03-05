import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from typing import List 
from streamlit_searchbox import st_searchbox
import polars as pl
import seaborn as sns
import squarify

def main(): 
     # set streamlit theme to dark by default 
    st.set_page_config(layout="wide", page_icon="plots/us_dollar.png", initial_sidebar_state="expanded")

    st.title("Trade between Countries")
    #st.sidebar.subtitle("Search by country or product")    
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

        # Drop Country Code 
        labelled_df = labelled_df.drop(columns=['Country Code'])

        # Keep only the following two columns from pop_data: Country Name, Country Code
        pop_data = pop_data[['Country Name', 'Country Code']]
        # Rename Country Name to Importer
        pop_data = pop_data.rename(columns={'Country Name': 'Importer'})

        # Only keep the following columns from labelled_df: Importer, partner_code, partner, import_value, descrip
    
        #join pop_data to labelled_df
      
        # Drop population
        #pop_data = pop_data.drop(columns=['pop_2020'])
        # From pop_data, keep only the following columns: Country Name, Country Code
        # Only keep uniuqe rows
        pop_data = pop_data[['Importer', 'Country Code']].drop_duplicates() 

        #labelled_df = labelled_df.merge(pop_data, left_on='location_code', right_on='Country Code', how='inner')

        # Drop the following columns: year, location_id, partner_id, export_value, parent_code, description, code, product_code
        labelled_df = labelled_df.drop(columns=['year', 'location_id','product_id','sitc_eci','sitc_coi', 'sitc_product_code','location_code', 'export_value', 'parent_code', 'code'])
        #labelled_df = labelled_df.merge(pop_data, left_on='partner_code', right_on='Country Code', how='inner')
    
        return labelled_df
    
    data = load_data()

    #print(data.head(10))

    # Implement selector for location_code 
    location_code = st.sidebar.selectbox('Importer', data['Country Name'].unique())

    # Implement selector for location_code 
    partner_id = st.sidebar.selectbox('Exporter', data['partner_code'].unique())

    # Implement selector for description 
    # description = st.sidebar.selectbox('Product description', data['description'].unique())

    data = data[data['Country Name'] == location_code]
    data = data[data['partner_code'] == partner_id]
    # data = data[data['description'] == description]

    # Select distinct location_code and use it in the title 
    location_code = data['Country Name'].unique()

    # sort by import_value
    data_top10 = data.sort_values(by='import_value', ascending=False)

    # Rename Country Name to Exporter
    data_top10 = data_top10.rename(columns={'Country Name': 'Importer', 'Population': 'pop_20'})
    # Select columns in this order: Exporter, partner_code, partner, import_value, description
    data_top10 = data_top10[['Importer', 'pop_2020','partner_code', 'import_value', 'description']]

    # Drop duplicated rows 
    data_top10 = data_top10.reset_index().drop_duplicates()

    # Select first row by group 
    data_top10 = data_top10.groupby(['Importer', 'pop_2020','partner_code', 'description']).first().reset_index()

    # Append location_code to the title
    #st.title('''Imports by ''' + str(location_code[0]) + ''' from ''' + str(location_code[0]) + ''' in 2020''')
    st.write(data_top10)

    def plot_deficits_bycountry(df, location_code):
        # Plot bar plot andsave plot as png to output folder. Use seaborn for styling
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.set_style(style="whitegrid") # set seaborn plot style
        # Convert import_value to numeric
        df["import_value"] = pd.to_numeric(df["import_value"], errors='coerce')
        sizes= df["import_value"].values# proportions of the categories
        #label=df["location_code"]
        squarify.plot(sizes=sizes, label=location_code, alpha=0.6).set(title='Treemap with Squarify')
        plt.axis('off')
        # plt.savefig('../output/top10partners_' + location_code + '.png', dpi=300, bbox_inches='tight')
        st.pyplot(fig)

    #plot_deficits_bycountry(data_top10, location_code)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(data.head(20))


if __name__ == '__main__':
    main()