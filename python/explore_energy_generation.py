# Use python to download energy generation capacity by country and year for the following countries
# Brazil, China, India, Indonesia, Japan, Mexico, Russia, South Africa, United States, and the European Union

# Import libraries
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt

# Define function to download data
def download_data(url, filename):
    # Download data
    r = requests.get(url)
    # Save data to file
    with open(filename, 'wb') as f:
        f.write(r.content)

# Define function to read data
def read_data(filename):
    # Read data
    with open(filename, 'r') as f:
        data = json.load(f)
    # Convert data to dataframe
    df = pd.DataFrame(data)
    # Return dataframe
    return df

# Define function to clean data
def clean_data(df):
    # Remove rows with missing values
    df = df.dropna()
    # Remove rows with no data
    df = df[df['value'] != 'No data']
    # Convert value column to numeric
    df['value'] = pd.to_numeric(df['value'])
    print(df)
    # Return dataframe
    return df

# Define function to plot data
# def plot_data(df):
#     # Plot data
#     df.plot(kind='bar', x='country', y='value', title='Energy Generation Capacity by Country')
#     # Show plot
#     plt.show()

# Define function to run all functions
def run():
    # Download data
    #download_data('https://datahub.io/core/energy-generation/r/energy-generation-capacity-by-country.json', 'energy-generation-capacity-by-country.json')
    # Read data
    df = read_data('energy-generation-capacity-by-country.json')
    # Clean data
    print(df)
   #df = clean_data(df)
    # Plot data
    # plot_data(df)

# Run all functions 
run()