import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import polars as pl
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score 


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
        # Summarize the trade_balance by location_code and product_description
        labelled_df = labelled_df.groupby(['location_code',  'partner_code', 'description'])['trade_balance'].sum().reset_index()

        return labelled_df
    
    @st.cache(persist=True)
    def split(df):
        X = df.drop(columns=['trade_balance'])
        y = df['trade_balance']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    data = load_data()
    X_train, X_test, y_train, y_test = split(data)

    # Filter location_code to the USA, CHN, and RUS (China, Russia, and the United States)
    labelled_df = data[data['location_code'].isin(['RUS', 'CHN', 'UGA'])]

    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(labelled_df)

        st.subheader('Training set')
        st.write(X_train)

        st.subheader('Test set')
        st.write(X_test)

if __name__ == '__main__':
    main()