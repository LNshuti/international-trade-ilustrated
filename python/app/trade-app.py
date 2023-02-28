import streamlit as st 
import pandas as pd
import pyarrow.parquet as pq
import matplotlib.pyplot as plt
from typing import List 
from streamlit_searchbox import st_searchbox
import polars as pl
from sklearn.svm import SVC 
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import explained_variance_score, r2_score, mean_absolute_error, mean_squared_error, mean_squared_log_error, median_absolute_error, max_error

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
        labelled_df = labelled_df.drop(columns=['year', 'location_id', 'partner_id', 'export_value', 'parent_code', 'description', 'code'])
        
        # Use LabelEncoder to encode the categorical columns: location_code, partner_code
        label = LabelEncoder()
        for col in ['location_code', 'partner_code', 'sitc_product_code']:
            labelled_df[col] = label.fit_transform(labelled_df[col])

        return labelled_df
    
    @st.cache(persist=True)
    def split(df):
        X = df.drop(columns=['import_value'])
        y = df['import_value']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def plot_metrics(metrics_list):
        if 'ROC Curve' in metrics_list:
            st.subheader("ROC Curve")
            plot_roc_curve(model, x_test, y_test, y_pred)
            st.pyplot()
    
    data = load_data()
    X_train, X_test, y_train, y_test = split(data)

    # Implement selector for state 
    location_code = st.sidebar.selectbox('Select location_code', data['location_code'].unique())

    # Implement selector for partner_code 
    partner_code = st.sidebar.selectbox('Select partner_code', data['partner_code'].unique())
    
    data = data[data['location_code'] == location_code]
    data = data[data['partner_code'] == partner_code]

    st.write(data)
    # Plot a histogram of the total award 
    # Write code below 
    # st.write('''Total Government Contract Issuange by Agency''')
    # fig, ax = plt.subplots()
    # ax.hist(data['Total Award($)'], bins=20)
    # ax.set_xlabel('Total Award($Millions)')
    # ax.set_ylabel('Frequency')
    # ax.set_title('Total Award Distribution')
    # st.pyplot(fig)

    st.sidebar.subheader("Choose Model")
    model = st.sidebar.selectbox("Model", ("Xgboost", "Adaboost", "Random Forest"))

    if model == "Xgboost":
        st.sidebar.subheader("Model Hyperparameters")
        eta = st.sidebar.number_input("eta (Shrinkage parameter)", 0.01, 1.0, step=0.01, key="eta")
        gamma = st.sidebar.number_input("Gamma (Minimum loss reduction)", 0, 3, step=1, key="gamma")
        max_depth = st.sidebar.radio("Maxiumum Tree Depth", (1, 6, 10), key='kernel')

        

        if st.sidebar.button("Run Regression", key="Regress"):
            st.subheader("Xgboost Results")
            



    if st.sidebar.checkbox("Show raw data", False):
        st.subheader('Raw data')
        st.write(data.head(20))


if __name__ == '__main__':
    main()