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

    rwa_df = top10_products(labelled_df, 'RWA')


    ### ASEAN 
    vnm_df = top10_products(labelled_df, 'VNM')
    sgp_df = top10_products(labelled_df, 'SGP')
    tha_df = top10_products(labelled_df, 'THA')
    phl_df = top10_products(labelled_df, 'PHL')
    mys_df = top10_products(labelled_df, 'MYS')
    idn_df = top10_products(labelled_df, 'IDN')
    khm_df = top10_products(labelled_df, 'KHM')

    ### OPEC 
    #### Algeria, Angola, Congo, Equatorial Guinea, Gabon, Iran, Iraq, Kuwait, Libya, Nigeria, Qatar, Saudi Arabia, 
    #### United Arab Emirates, Venezuela, and Yemen
    dza_df = top10_products(labelled_df, 'DZA')
    ago_df = top10_products(labelled_df, 'AGO')
    cog_df = top10_products(labelled_df, 'COG')
    gnq_df = top10_products(labelled_df, 'GNQ')
    gab_df = top10_products(labelled_df, 'GAB')
    irn_df = top10_products(labelled_df, 'IRN')
    irq_df = top10_products(labelled_df, 'IRQ')
    kwt_df = top10_products(labelled_df, 'KWT')
    lby_df = top10_products(labelled_df, 'LBY')
    nga_df = top10_products(labelled_df, 'NGA')
    qat_df = top10_products(labelled_df, 'QAT')
    sau_df = top10_products(labelled_df, 'SAU')
    are_df = top10_products(labelled_df, 'ARE')
    ven_df = top10_products(labelled_df, 'VEN')
    yem_df = top10_products(labelled_df, 'YEM')

    ### EU 
    aut_df = top10_products(labelled_df, 'AUT')
    bel_df = top10_products(labelled_df, 'BEL')
    bgr_df = top10_products(labelled_df, 'BGR')
    hrv_df = top10_products(labelled_df, 'HRV')
    cyp_df = top10_products(labelled_df, 'CYP')
    cze_df = top10_products(labelled_df, 'CZE')
    dnk_df = top10_products(labelled_df, 'DNK')
    est_df = top10_products(labelled_df, 'EST')
    fin_df = top10_products(labelled_df, 'FIN')
    fra_df = top10_products(labelled_df, 'FRA')
    deu_df = top10_products(labelled_df, 'DEU')
    grc_df = top10_products(labelled_df, 'GRC')
    hun_df = top10_products(labelled_df, 'HUN')
    irl_df = top10_products(labelled_df, 'IRL')
    ita_df = top10_products(labelled_df, 'ITA')
    lva_df = top10_products(labelled_df, 'LVA')
    ltu_df = top10_products(labelled_df, 'LTU')
    lux_df = top10_products(labelled_df, 'LUX')
    mlt_df = top10_products(labelled_df, 'MLT')
    nld_df = top10_products(labelled_df, 'NLD')
    pol_df = top10_products(labelled_df, 'POL')
    prt_df = top10_products(labelled_df, 'PRT')
    rou_df = top10_products(labelled_df, 'ROU')
    svk_df = top10_products(labelled_df, 'SVK')
    svn_df = top10_products(labelled_df, 'SVN')
    esp_df = top10_products(labelled_df, 'ESP')
    swe_df = top10_products(labelled_df, 'SWE')

    ### BRICS
    rus_df = top10_products(labelled_df, 'RUS')
    ind_df = top10_products(labelled_df, 'IND')
    chn_df = top10_products(labelled_df, 'CHN')
    bra_df = top10_products(labelled_df, 'BRA')
    zaf_df = top10_products(labelled_df, 'ZAF')

    ### NATO 
    aut_df = top10_products(labelled_df, 'AUT')
    bel_df = top10_products(labelled_df, 'BEL')
    bgr_df = top10_products(labelled_df, 'BGR')
    hrv_df = top10_products(labelled_df, 'HRV')
    cyp_df = top10_products(labelled_df, 'CYP')
    cze_df = top10_products(labelled_df, 'CZE')
    dnk_df = top10_products(labelled_df, 'DNK')
    est_df = top10_products(labelled_df, 'EST')
    fin_df = top10_products(labelled_df, 'FIN')
    fra_df = top10_products(labelled_df, 'FRA')
    deu_df = top10_products(labelled_df, 'DEU')
    grc_df = top10_products(labelled_df, 'GRC')
    hun_df = top10_products(labelled_df, 'HUN')
    irl_df = top10_products(labelled_df, 'IRL')
    ita_df = top10_products(labelled_df, 'ITA')
    lva_df = top10_products(labelled_df, 'LVA')
    ltu_df = top10_products(labelled_df, 'LTU')
    lux_df = top10_products(labelled_df, 'LUX')
    mlt_df = top10_products(labelled_df, 'MLT')
    nld_df = top10_products(labelled_df, 'NLD')
    pol_df = top10_products(labelled_df, 'POL')
    prt_df = top10_products(labelled_df, 'PRT')
    rou_df = top10_products(labelled_df, 'ROU')
    svk_df = top10_products(labelled_df, 'SVK')
    svn_df = top10_products(labelled_df, 'SVN')
    esp_df = top10_products(labelled_df, 'ESP')
    swe_df = top10_products(labelled_df, 'SWE')
    usa_df = top10_products(labelled_df, 'USA')
    cana_df = top10_products(labelled_df, 'CAN')
    isr_df = top10_products(labelled_df, 'ISR')
    swit_df = top10_products(labelled_df, 'CHE')
    norw_df = top10_products(labelled_df, 'NOR')
    turk_df = top10_products(labelled_df, 'TUR')
    jor_df = top10_products(labelled_df, 'JOR')
    alb_df = top10_products(labelled_df, 'ALB')
    arm_df = top10_products(labelled_df, 'ARM')
    aze_df = top10_products(labelled_df, 'AZE')
    bhr_df = top10_products(labelled_df, 'BHR')
    geo_df = top10_products(labelled_df, 'GEO')
    kaz_df = top10_products(labelled_df, 'KAZ')
    kwt_df = top10_products(labelled_df, 'KWT')
    kgz_df = top10_products(labelled_df, 'KGZ')
    lbn_df = top10_products(labelled_df, 'LBN')
    lby_df = top10_products(labelled_df, 'LBY')
    mkd_df = top10_products(labelled_df, 'MKD')

    asean_df = pl.concat([vnm_df, sgp_df, tha_df, phl_df, mys_df, idn_df, khm_df])
    aggregated_asean_df = (
        asean_df
        .groupby(['location_code'])
        .agg(
            pl.col('trade_bal_by_population').mean().alias('avg_trade_bal_per_capita')
        ) )

    print(aggregated_asean_df)
    # Convert polars table to png and save to output
    # Write the code
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.set_style("whitegrid")
    sns.factorplot(x='avg_trade_bal_per_capita', y='location_code', data=aggregated_asean_df.to_pandas(), kind='bar')
    plt.title('Trade balance per capita in USD')
    plt.xlabel('USD')
    plt.ylabel('Country')
    plt.savefig('../output/avg_trade_bal_per_capita_asean.png', dpi=300, bbox_inches='tight')

    brics_df = pl.concat([rus_df, ind_df, chn_df, bra_df, zaf_df])
    aggregated_brics_df = (
        asean_df
        .groupby(['location_code'])
        .agg(
            pl.col('trade_bal_by_population').mean().alias('avg_trade_bal_per_capita')
        ) )

    print(aggregated_brics_df)
    # Convert polars table to png and save to output
    # Write the code
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.set_style("whitegrid")
    sns.factorplot(x='avg_trade_bal_per_capita', y='location_code', data=aggregated_brics_df.to_pandas(), kind='bar')
    plt.title('Trade balance per capita in USD')
    plt.xlabel('USD')
    plt.ylabel('Country')
    plt.savefig('../output/avg_trade_bal_per_capita_brics.png', dpi=300, bbox_inches='tight')


    eu_df = pl.concat([aut_df, bel_df, bgr_df, cyp_df, cze_df, deu_df, dnk_df, est_df, fin_df, fra_df, grc_df, hun_df, irl_df, ita_df, lva_df, ltu_df, lux_df, mlt_df, nld_df, pol_df, prt_df, rou_df, svk_df, svn_df, esp_df, swe_df])
    aggregated_eu_df = (
        asean_df
        .groupby(['location_code'])
        .agg(
            pl.col('trade_bal_by_population').mean().alias('avg_trade_bal_per_capita')
        ) )

    print(aggregated_eu_df)
    # Convert polars table to png and save to output
    # Write the code
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.set_style("whitegrid")
    sns.factorplot(x='avg_trade_bal_per_capita', y='location_code', data=aggregated_eu_df.to_pandas(), kind='bar')
    plt.title('Trade balance per capita in USD')
    plt.xlabel('USD')
    plt.ylabel('Country')
    plt.savefig('../output/avg_trade_bal_per_capita_eu.png', dpi=300, bbox_inches='tight')

    ############################################

    nato_df = pl.concat([aut_df, bel_df, bgr_df, cyp_df, cze_df, deu_df, dnk_df, est_df, fin_df, fra_df, grc_df, hun_df, irl_df, ita_df, lva_df, ltu_df, lux_df, mlt_df, nld_df, pol_df, prt_df, rou_df, svk_df, svn_df, esp_df, swe_df, dza_df, ago_df, cog_df, gnq_df, gab_df, irn_df, irq_df, kwt_df, lby_df, nga_df, qat_df, sau_df, are_df, ven_df, yem_df, rus_df, ind_df, chn_df, bra_df, zaf_df, vnm_df, sgp_df, tha_df, phl_df, mys_df, idn_df, khm_df])
    aggregated_nato_df = (
        asean_df
        .groupby(['location_code'])
        .agg(
            pl.col('trade_bal_by_population').mean().alias('avg_trade_bal_per_capita')
        ) )

    print(aggregated_nato_df)
    # Convert polars table to png and save to output
    # Write the code
    fig, ax = plt.subplots(figsize=(5, 3))
    sns.set_style("whitegrid")
    sns.factorplot(x='avg_trade_bal_per_capita', y='location_code', data=aggregated_nato_df.to_pandas(), kind='bar')
    plt.title('Trade balance per capita in USD')
    plt.xlabel('USD')
    plt.ylabel('Country')
    plt.savefig('../output/avg_trade_bal_per_capita_nato.png', dpi=300, bbox_inches='tight')

    def plot_top10_partners(df, location_code):
        # Plot bar plot andsave plot as png to output folder. Use seaborn for styling
        fig, ax = plt.subplots(figsize=(5, 3))
        sns.set_style("whitegrid")
        sns.catplot(x='trade_balance_millions', y='partner_code', data=df.to_pandas(), palette='Blues_d', kind='bar')
        plt.title(location_code)
        plt.xlabel('Trade Balance In Millions of USD')
        plt.ylabel('')
        plt.savefig('../output/top10partners_' + location_code + '.png', dpi=300, bbox_inches='tight')

    # Call the function
    plot_top10_partners(rwa_df, 'RWA')

    all_countries = pl.concat([aut_df, bel_df, bgr_df, cyp_df, cze_df, deu_df, dnk_df, est_df, fin_df, fra_df, grc_df, hun_df, irl_df,
                                ita_df, lva_df, ltu_df, lux_df, mlt_df, nld_df, pol_df, prt_df, rou_df, svk_df, svn_df, esp_df, swe_df,
                                dza_df, ago_df, cog_df, gnq_df, gab_df, irn_df, irq_df, kwt_df, lby_df, nga_df, qat_df, sau_df, are_df,
                                ven_df, yem_df, rus_df, ind_df, chn_df, bra_df, zaf_df, vnm_df, sgp_df, tha_df, phl_df, mys_df, 
                                idn_df, khm_df, rwa_df, usa_df, cana_df, isr_df])
    all_countries_df = (
        all_countries
        .groupby(['location_code'])
        .agg(
            pl.col('trade_bal_by_population').mean().alias('avg_trade_bal_per_capita')
        ) )

    print(all_countries_df)

    fig, ax = plt.subplots(figsize=(5, 3))
    sns.set_style("whitegrid")
    sns.factorplot(x='avg_trade_bal_per_capita', y='location_code', data=all_countries_df.to_pandas(), kind='bar', height=10)
    plt.title('Trade balance per capita in USD')
    plt.xlabel('USD')
    plt.ylabel('Country')
    plt.savefig('../output/trade_bal_all_countries_df.png', dpi=300, bbox_inches='tight')

    def plot_top10_partners(df, location_code):
        # Plot bar plot andsave plot as png to output folder. Use seaborn for styling

        print(dir(df))
        # Sort df by avg_trade_bal_per_capita in descending order
        df = df.sort(by='avg_trade_bal_per_capita', reverse=True)

        # Make the font human readable 
        sns.set(font_scale=1.5)

        fig, ax = plt.subplots(figsize=(5, 8))
        sns.set_style("whitegrid")
        sns.catplot(x='avg_trade_bal_per_capita', y='location_code', data=all_countries_df.to_pandas(), palette='Blues_d', kind='bar')
        plt.title('')
        plt.xlabel('Trade Balance Per Capita in USD')
        plt.ylabel('')
        # Seaborn decreasethe font size of y labels 
        plt.yticks(fontsize=8, color='grey')
        plt.savefig('../output/top10partners_all_countries_df_' + location_code + '.png', dpi=900)

    # Call the function
    plot_top10_partners(all_countries_df, 'ESP')

        # # Parse the HTML content and get the data as a DataFrame
        # df = parse_sales_tax_data(df)

        # # Plot the data in the DataFrame
        # plot_sales_tax_data(df)

    
# Filter all_countries_df by location_code using the following locations 
all_countries = ["REU", "RWA", "STP",	"SEN", 	"SYC", 	"SLE", "SOM","ZAF", "SSD", "SDN", "SWZ", "TZA", "NGA", "NER",
                 "TGO", "TUN",	"UGA", "ESH",	"ZMB", "ZWE", "LSO",	"LBR",	"LBY", "MDG", "MLI", "MWI",	"MRT",	"MUS",	
                 "MYT",	"MAR",	"MOZ","NAM", "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV","CAF",	"TCD", "COM", 
                 "COG", "COD", "CIV", "DJI",	"EGY","GNQ", "ERI",	"ETH", "GAB", "GMB", "GHA", "GIN", "GNB", "KEN"]
# Write the code
all_countries_df = all_countries_df[all_countries_df['location_code'].isin(all_countries)]

all_africa_df = all_countries_df.sort_values(by='trade_balance_millions', ascending=False)

# Calculate the average trade balance per country 
# Write the code
all_africa_df_sum = all_africa_df.groupby(['location_code'])['trade_balance_millions'].sum().reset_index()
# Sort by descending trade balance
all_africa_df_sum = all_africa_df_sum.sort_values(by='trade_balance_millions', ascending=False)


# convert to polars dataframe
all_africa_pl = pl.from_pandas(all_africa_df)

# all_countries_df_agg = (
#     top10
#     .groupby(['location_code'])
#     .agg(
#         pl.col('trade_balance_millions').mean().alias('avg_trade_balance_millions'), 
#         pl.col('trade_balance').mean().alias("avg_trade_balance")
#         )
#         .sort('avg_trade_balance_millions', reverse=True)
# )
print(all_africa_pl)

# Convert polars table to png and save to output 
fig, ax = plt.subplots(figsize=(8, 8))
sns.set_style("whitegrid")
#sns.catplot(x='trade_balance_millions', y='location_code', data=all_africa_pl.to_pandas(), kind='bar', height=8, aspect=0.8)
plt.title('')
plt.xlabel('Trade balance $ Millions USD')
plt.ylabel('')
ax2 = plt.twinx()
sns.catplot(x='pop_2020', y='location_code', data=all_africa_pl.to_pandas(), kind='bar', height=8, aspect=0.8)
#sns.lineplot(data=all_africa_pl.column2, color="b", ax=ax2)
plt.savefig('../output/population_2020_allafrica.png', dpi=300, bbox_inches='tight')



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
# plt.savefig('../output/china_exports_treemap.png', bbox_inches='tight')

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
# plt.savefig('../output/usa_exports_treemap.png', bbox_inches='tight')

# print(usa_df.head(10))


# # Filter to the top 10 products by trade balance for CHN 
# rus_df = labelled_df[labelled_df['location_code'] == 'RUS'].sort_values(by='trade_balance', ascending=False).head(10)

# plt.figure(figsize=(8,6))
# # Plot the treemap
# squarify.plot(sizes=rus_df['trade_balance'], label=rus_df['parent_code'], alpha=.8 )
# # Remove the axis
# plt.axis('off')
# # Save the plot as a png file
# plt.savefig('../output/russia_exports_treemap.png', bbox_inches='tight')

# print(rus_df.head(10))


