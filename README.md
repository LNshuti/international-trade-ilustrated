# Summarize Eonomic Strength measured in terms of Deficits and Currencies

**Introduction**
---------------
The purpose of this repository is to use available data to analyze the relative strength of countries. With the increasing geopolitical uncertainty notably the war in Ukraine and associated chatter about WW3, competition between powerful countries is heating up. According to Ray Dalio's book The Changing World Order, the five most important measures that determine a Nation's present and future changes in wealth and income are the following:

1. Innovation
2. The capital market cycle
3. Internal order/disorder cycle
4. External order-disorder cycle
5. Acts of Nature

Attempting to measure innovation by country is too difficult a task to approach in this exercise. One interesting study on innovation which focuses mostly on US corporations is Kai Wu's paper on Investing in Innovation. Similarly, we won't attempt to explain the relative order/disorder between countries nor do we have the capability to predict Acts of Nature. Using macroeconomic literature and open source data, this repo attempts to rank countries by 1) the value of exported goods and services, 2) debt levels(both public and private), and 3) the strength of each country's currency.

**Data Source**
---------------
We use the Atlas of Economic Complexity from the Growth Lab at Harvard University because this data source is: 1) Detailed down to the product level that each country in the World trades from 1962 to 2020. 2) Standardized to simplify the process of building a time series to track changes over time. 3) Regularly used and highly cited source with over eighty thousand downloads. It is also publicly available and can be downloaded here.


**Exploratory Data Analysis**
--------------------------------

Below we plot trade relationships between the China, France, and Russia. For this plot, we sum data for the latest available year, 2020. The trade balance is measured in Billions of US dollars.

**Figure 1:French Exports**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/9d76bb68-3b2b-4757-8c64-fa747a40f0a9)

**Figure 2: French Imports**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/1337bf49-ce43-4b8c-bb2c-fd2a5ff8742c)

**How to run Interactive App on your local machine**
```{python}
git clone https://github.com/LNshuti/international-trade-ilustrated.git
cd international-trade-ilustrated
pip install -r requirements.txt

cd python/app
streamlit run trade-app.py
```

### References 
1. The Growth Lab at Harvard University. International Trade Data (SITC, Rev. 2). 2019-05-31. 2019. V5. Harvard Dataverse. URL. https://doi.org/10.7910/DVN/H8SFD2. doi/10.7910/DVN/H8SFD2

2. Wu, Kai. September 2022. Liquid Venture Capital. Sparkline Capital. https://www.sparklinecapital.com/post/liquid-venture-capital

3. Replicate Canada Export Plot. https://atlas.cid.harvard.edu/explore 
