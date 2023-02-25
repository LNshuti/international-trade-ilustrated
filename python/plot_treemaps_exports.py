# Use python to plot treemaps of exports by country and by product
import pyarrow.parquet as pq
import pandas as pd
import squarify
import matplotlib.pyplot as plt
import dataframe_image as dfi
import seaborn as sns
import polars as pl

# Create a function that returns the top 10 products by trade balance for a given location_code
def top10_products(df, location_code):
    # Filter to the top 10 products by trade balance for CHN 
    top10 = df[df['location_code'] == location_code].sort_values(by='trade_balance_millions', ascending=False).head(10)
    # Select unique values from the parent_code and description columns 
    top10 = top10[['year','parent_code','location_code', 'partner_code', 'description', 'trade_balance_millions', 'trade_balance', 'pop_2020', 'trade_bal_by_population']].drop_duplicates()
    # convert to polars dataframe
    top10 = pl.from_pandas(top10)
    return top10

def parse_sales_tax_data(df):
    # Rename the columns of the DataFrame
    df.columns = ["State", "Rate",  'Rank', 'Avg. Local Tax Rate', 'Combined Rate', 'Rank.1', 'Max Local Tax Rate']

    df.Rate= df.Rate.str.replace('%','',regex=True)
    df.State= df.State.str.replace('.','',regex=True)
    df = df.drop([7,25, 28,36,51])

    df["State"] = df["State"].str.strip().str.upper()

    state_abbrev_map = {
        'ALASKA': 'AK',
        'ARIZ': 'AZ',
        'CONN': 'CT',
        'HAWAII': 'HI',
        'MINN': 'MN',
        'MISS': 'MS',
        'TENN': 'TN',
        'TEX': 'TX',
        'NEV': 'NV'
    }

    df["ST"] = df["State"].map(state_abbrev_map).fillna(df["State"])
    df["ST"] = df["ST"].str[0:2]

    df['Rate_num'] = pd.to_numeric(df['Rate'], errors='coerce')

    # Return the sorted DataFrame
    df_sorted = df.sort_values(by="Rate_num")

    return df_sorted

def plot_sales_tax_data(df):
    # Use the matplotlib library to plot the data in the DataFrame
    fig, ax = plt.subplots()
    df.plot(x="ST", y="Rate_num", kind="scatter", title="Sales Tax Rates by State", ax=ax)

    # Show the plot with the appropriate labels
    plt.xlabel("")
    plt.ylabel("Sales Tax Rate (%)")
    plt.show()

def main():
 
    # Read in the data
    product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')

    # Read in the data
    trade_data_all_years = pq.ParquetDataset('../data/country_partner_sitcproduct4digit_year_2020.parquet').read_pandas().to_pandas()

    trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
    trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
    trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

    labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')
    #print(labelled_df.head(10))
    # Filter location_code to the USA, CHN, and RUS (China, Russia, and the United States)
    labelled_df = labelled_df[labelled_df['location_code'].isin(['USA', 'CHN', 'RUS'])]

    # Summarize the trade_balance by location_code and product_description
    labelled_df = labelled_df.groupby(['location_code', 'parent_code', 'description'])['trade_balance'].sum().reset_index()

    # Filter to the top 10 products by trade balance for CHN 
    usa_df = labelled_df[labelled_df['location_code'] == 'RUS'].sort_values(by='trade_balance', ascending=False)

    # Select unique values from the parent_code and description columns 
    usa_df = usa_df[['parent_code', 'description']].drop_duplicates()

    usa_df = usa_df[usa_df['parent_code'].isin(['0342'])]

    print(usa_df.reset_index(drop=True))

    # Read in the data
    product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')
    trade_data_all_years = pq.ParquetDataset('../data/processed/country_partner_sitcproduct4digit_year_all.parquet').read_pandas().to_pandas()
    # Import the population data
    # It is in csv format. Skip first four rows 
    # Fifth row contains the column names
    # Write the code 
    pop_data = pd.read_csv('../data/processed/API_SP_POP_TOTL_DS2.csv', skiprows=4)

    #print(trade_data_all_years.head(10))

    # COnvert numeric columns to numeric data type
    trade_data_all_years['export_value'] = pd.to_numeric(trade_data_all_years['export_value'], errors='coerce')
    trade_data_all_years['import_value'] = pd.to_numeric(trade_data_all_years['import_value'], errors='coerce')
    trade_data_all_years['trade_balance'] = trade_data_all_years['export_value'] - trade_data_all_years['import_value']

    # Merge the product labels to the trade data
    labelled_df = trade_data_all_years.merge(product_labs, left_on='sitc_product_code', right_on='parent_code', how='inner')

    # Summarize the trade_balance by location_code and product_description
    labelled_df = labelled_df.groupby(['year','location_code', 'parent_code', 'partner_code', 'description'])['trade_balance'].sum().reset_index()

    # Merge the population data to the trade data
    # Only keep the population data for 2020 
    # Write the code
    pop_data = pop_data[['Country Code', 'Country Name', '2020']]

    # Rename 2020 to pop_2020
    pop_data = pop_data.rename(columns={'2020': 'pop_2020'})

    # Create a new variable trade_balance_millions to make the numbers more readable
    labelled_df['trade_balance_millions'] = labelled_df['trade_balance'] / 1000000

    # Join pop_data 
    labelled_df = labelled_df.merge(pop_data, left_on='location_code', right_on='Country Code', how='inner')

    # Create a trade_bal_by_population variable. This variable is the trade balance divided by the population 
    # Write the code
    labelled_df['trade_bal_by_population'] = labelled_df['trade_balance'] / labelled_df['pop_2020']
    
    def plot_top10_partners(df, location_code):
        # Plot bar plot andsave plot as png to output folder. Use seaborn for styling
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.set_style("whitegrid")
        sns.catplot(x='trade_balance_millions', y='partner_code', data=df.to_pandas(), palette='Blues_d', kind='bar')
        plt.title(location_code)
        plt.xlabel('Trade Balance In Millions of USD')
        plt.ylabel('')
        # plt.savefig('../output/top10partners_' + location_code + '.png', dpi=300, bbox_inches='tight')

    def plot_top10_partners(df, location_code):
        # Plot bar plot andsave plot as png to output folder. Use seaborn for styling

        print(dir(df))
        # Sort df by avg_trade_bal_per_capita in descending order
        #df = df.sort(by='avg_trade_bal_per_capita', reverse=True)

        # Make the font human readable 
        sns.set(font_scale=1.5)

        fig, ax = plt.subplots(figsize=(5, 8))
        sns.set_style("whitegrid")
        sns.catplot(x='avg_trade_bal_per_capita', y='location_code', data=df.to_pandas(), palette='Blues_d', kind='bar')
        plt.title('')
        plt.xlabel('Trade Balance Per Capita in USD')
        plt.ylabel('')
        # Seaborn decreasethe font size of y labels 
        plt.yticks(fontsize=8, color='grey')
        plt.show()
        # plt.savefig('../output/top10partners_all_countries_df_' + location_code + '.png', dpi=900)

    # Call the function
    plot_top10_partners(labelled_df, 'ESP')

        # # Parse the HTML content and get the data as a DataFrame
        # df = parse_sales_tax_data(df)

        # # Plot the data in the DataFrame
        # plot_sales_tax_data(df)

    
    # # Filter all_countries_df by location_code using the following locations 
    # all_countries = ["REU", "RWA", "STP",	"SEN", 	"SYC", 	"SLE", "SOM","ZAF", "SSD", "SDN", "SWZ", "TZA", "NGA", "NER",
    #                 "TGO", "TUN",	"UGA", "ESH",	"ZMB", "ZWE", "LSO",	"LBR",	"LBY", "MDG", "MLI", "MWI",	"MRT",	"MUS",	
    #                 "MYT",	"MAR",	"MOZ","NAM", "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV","CAF",	"TCD", "COM", 
    #                 "COG", "COD", "CIV", "DJI",	"EGY","GNQ", "ERI",	"ETH", "GAB", "GMB", "GHA", "GIN", "GNB", "KEN"]
    # # Write the code
    # all_countries_df = all_countries_df[all_countries_df['location_code'].isin(all_countries)]

    # all_africa_df = all_countries_df.sort_values(by='trade_balance_millions', ascending=False)

    # # Calculate the average trade balance per country 
    # # Write the code
    # all_africa_df_sum = all_africa_df.groupby(['location_code'])['trade_balance_millions'].sum().reset_index()
    # # Sort by descending trade balance
    # all_africa_df_sum = all_africa_df_sum.sort_values(by='trade_balance_millions', ascending=False)


    # # convert to polars dataframe
    # all_africa_pl = pl.from_pandas(all_africa_df)

    # # all_countries_df_agg = (
    # #     top10
    # #     .groupby(['location_code'])
    # #     .agg(
    # #         pl.col('trade_balance_millions').mean().alias('avg_trade_balance_millions'), 
    # #         pl.col('trade_balance').mean().alias("avg_trade_balance")
    # #         )
    # #         .sort('avg_trade_balance_millions', reverse=True)
    # # )
    # print(all_africa_pl)

    # # Convert polars table to png and save to output 
    # fig, ax = plt.subplots(figsize=(8, 8))
    # sns.set_style("whitegrid")
    # #sns.catplot(x='trade_balance_millions', y='location_code', data=all_africa_pl.to_pandas(), kind='bar', height=8, aspect=0.8)
    # plt.title('')
    # plt.xlabel('Trade balance $ Millions USD')
    # plt.ylabel('')
    # ax2 = plt.twinx()
    # sns.catplot(x='pop_2020', y='location_code', data=all_africa_pl.to_pandas(), kind='bar', height=8, aspect=0.8)
    # #sns.lineplot(data=all_africa_pl.column2, color="b", ax=ax2)
    # # plt.savefig('../output/population_2020_allafrica.png', dpi=300, bbox_inches='tight')



if __name__ == "__main__":
    main()

# Using squarify to plot treemaps
# Save plot as png file
# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=china_df['trade_balance'], label=china_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# # plt.savefig('../output/china_exports_treemap.png', bbox_inches='tight')

# Increase font size for the text in the table 

# Save the plot as a png file
#dfi.export(df_styled,"../output/china_exports_table.png")


#dfi.export(df_styled,"../output/china_exports_table.png")
#dfi.export(df_styled,"../output/china_exports_labels.png")


# Filter to the top 10 products by trade balance for CHN 
# usa_df = labelled_df[labelled_df['location_code'] == 'USA'].sort_values(by='trade_balance', ascending=False).head(10)

# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=usa_df['trade_balance'], label=usa_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# # plt.savefig('../output/usa_exports_treemap.png', bbox_inches='tight')

# print(usa_df.head(10))


# # Filter to the top 10 products by trade balance for CHN 
# rus_df = labelled_df[labelled_df['location_code'] == 'RUS'].sort_values(by='trade_balance', ascending=False).head(10)

# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=rus_df['trade_balance'], label=rus_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# # plt.savefig('../output/russia_exports_treemap.png', bbox_inches='tight')

# print(rus_df.head(10))


