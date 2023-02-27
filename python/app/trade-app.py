import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import polars as pl
from sklearn.svm import SVC 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score 


def main(): 
    st.title("Trading Partners by Country")
    st.sidebar.title("Trading Partners by Country")
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
        # Summarize the trade_balance by location_code and product_description
        labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'partner_code', 'description'])['trade_balance'].sum().reset_index()
