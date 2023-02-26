# Summarize Eonomic Strength measured in terms of Deficits and Currencies

**Introduction**
The purpose of this repository is to use available data to analyze the relative strength of countries. With the increasing geopolitical uncertaincy notably the war in Ukraine and associated chatter about WW3, competition between powerful countries is heating up. Using macroeconomic literature and open source data, this repo attempts to connect the dots with two goals in mind: 

1. Visualizing historical trade between countries
2. Developing hypotheses on what might happen were trade to be restricted or drastically reduced going forward. 

According to Ray Dalio's book [The Changing World Order](https://www.youtube.com/watch?v=xguam0TKMw8), the five most important measures that determine a Nation's present and future changes in wealth and income are the following: 

* Innovation 
* The capital market cycle 
* Internal order/disorder cycle
* External order disorder cycle 
* Acts of Nature 

Attempting to measure innovation by country is too difficult a task to approach in this exercise. One interesting study on innovation which focuses mostly on US corporations is Kai Wu's paper on [Investing in Innovation](https://sparklinecapital.files.wordpress.com/2022/04/sparkline-innovation.pdf). The primary goal of of this exercise is to rank countries by 1) the value of exported goods and services, debts levels(both public and private), and the strength of each country's currency.  

**Data Source**
---------------
As in my [other work](https://github.com/LNshuti/LNSHUTI.github.io), I use the Atlas of Economic Complexity from the Growth Lab at Harvard University because this data source is: 1) Detailed down to the product level that each country in the World trades from 1962 to 2020. 2) Standardized to simplify the process of building time series to track changes over time. 3) Regularly used and highly cited source with over *eighty thousand downloads*. It is also publicly available and can be downloaded [**here.**](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2)


**Exploratory Data Analysis**
--------------------------------

Below we plot trade relationships between the United States, China,and Russia. For this plot, we sum data for the latest available year, 2020.  **Trade balance** is measured in **Billions US dollars**.

In 2020, China had a surplus relative to the United States, Hong Kong, Great Britain, India and the Netherlands. With the United States, China exported $200+ Billion dollars' worth of products and services **in excess** to the value of products/services China imported from the United States. Interestingly, Russia and the US had negligible differences in terms of the monetary value of their bilateral imports/exports. 


**Figure 1: 2020 Trade Balance**
![](output/deficit_plot_us_chn_rus.png)


**Figure 2: Product labels**

|parent_code | description |
:-----------------|:-----------|
|7643| Transmission apparatus|      
|6589| Clothing Products|      
|7599| Parts & accessories|
|6812| Rare Earth Metals(Platinum, Base metals, silver/gold, clad with platinum) |      
|9710| Gold (including gold plated with platinum), Waste & scrap of gold |      
|0342| Frozen Fish Products |     
|6821| Copper |      
|3222| Lignite |
|6672| Diamonds |      
|3352| Oils & other products |
|5621| Ammonium nitrate |
|5629| Fertilizers |
|6841| Aluminium |

# Energy Generation 
How do these major economic powers compare in terms of energy generation and consumption. 
According to the 2021 TAEBC Economic impact report, Advanced Energy is a $1.4 trillion market.  


### References 
1. The Growth Lab at Harvard University. International Trade Data (SITC, Rev. 2). 2019-05-31. 2019. V5. Harvard Dataverse. URL. https://doi.org/10.7910/DVN/H8SFD2. doi/10.7910/DVN/H8SFD2

2. Wu, Kai. September 2022. Liquid Venture Capital. Sparkline Capital. https://www.sparklinecapital.com/post/liquid-venture-capital
