import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import List 
#from streamlit_searchbox import st_searchbox
import polars as pl
import seaborn as sns
import toml 
import squarify

# Create a config.toml file 
config = { 
    "theme": { 
        "primaryColor": "#f63366", 
        "backgroundColor": "#edf6f7", 
        "secondaryBackgroundColor": "#ffffff", 
        "textColor": "#262730", 
        "font": "sans serif", 
        "fontSize": "10px" 
    } 
} 

def main(): 
     # set streamlit theme to dark by default 
    st.set_page_config(layout="wide", page_icon=":currency_exchange:", initial_sidebar_state="expanded")

    st.title("Trade between Countries")
    #st.sidebar.subtitle("Search by country or product")    

    st.cache(persist=True)
    def load_data():     

        # Read in the data from parquet 
        labelled_df = pq.ParquetDataset('processed_country_partner_df.parquet').read_pandas().to_pandas()

        #labelled_df = pd.read_csv("processed_country_partner_df.csv")
        return labelled_df
    
    data = load_data()

    ## print(data.head(10))

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
    data_top10 = data_top10[['Importer','partner_code', 'import_value', 'description', 'sitc_product_code']]

    # Drop duplicated rows 
    data_top10 = data_top10.reset_index().drop_duplicates()

    # Select first row by group 
    data_top10 = data_top10.groupby(['Importer', 'partner_code', 'description', 'sitc_product_code']).first().reset_index() 

    # convert sitc_product_code to string 
    data_top10['sitc_product_code'] = data_top10['sitc_product_code'].astype(str)

    #df = df.groupby(['partner_code', 'sitc_product_code']).first().reset_index() 
    data_top10 = data_top10.reset_index(drop=True)
    ## print(data_top10)
    data_top10 = data_top10.sort_values(by='import_value', ascending=False)
    data_top10 = data_top10.drop(columns=['index', 'Importer']).drop_duplicates()

    # Select first row by group
    data_top10 = data_top10.groupby(['partner_code', 'sitc_product_code']).first().reset_index()

    # Sort by import_value descending
    data_top10 = data_top10.sort_values(by='import_value', ascending=False)

    # Drop rows where import_value is 0
    data_top10 = data_top10[data_top10['import_value'] != 0]

    # Set table width 
    st.write(data_top10)


    def plot_deficits_bycountry(df, location_code):
        
        # Convert import_value to numeric
        df["import_value"] = pd.to_numeric(df["import_value"], errors='coerce')
        # divide by a millin 
        df["import_value"] = df["import_value"] / 1000000

        # select import_value, partner_code, sitc_product_code
        df = df[['import_value', 'partner_code', 'sitc_product_code']]
        # select first row by group
        df = df.groupby(['partner_code', 'sitc_product_code']).first().reset_index()
        # Sort by import_value descending
        df = df.sort_values(by='import_value', ascending=False)

        # print(df.head())
        # print(df.columns)
         # Plot bar plot andsave plot as png to output folder. Use seaborn for styling
        fig, ax = plt.subplots(figsize=(5, 5))
        sns.set_style(style="dark") # set seaborn plot style
        # List seaborn styles
        # Plot histogram of import_value
        sns.barplot(x="import_value", y="sitc_product_code", data=df.head(), palette="colorblind")

        ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
        ax.tick_params(labelsize=8)
        # Set x-axis label
        plt.xlabel('Import value (Millions USD)')
        # Set y-axis label
        plt.ylabel('Product code')
        # Set title
        st.write(fig)

    plot_deficits_bycountry(data_top10, location_code)

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(data.head(20))


if __name__ == '__main__':
    main()