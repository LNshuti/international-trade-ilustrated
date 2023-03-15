# Summarize Eonomic Strength measured in terms of Deficits and Currencies

**Introduction**
---------------
The purpose of this repository is to use available data to analyze the relative strength of countries. With the increasing geopolitical uncertainty notably the war in Ukraine and associated chatter about WW3, competition between powerful countries is heating up. According to Ray Dalio's book The Changing World Order, the five most important measures that determine a Nation's present and future changes in wealth and income are the following:

* Innovation
* The capital market cycle
* Internal order/disorder cycle
* External order-disorder cycle
* Acts of Nature

Attempting to measure innovation by country is too difficult a task to approach in this exercise. One interesting study on innovation which focuses mostly on US corporations is Kai Wu's paper on Investing in Innovation. Similarly, we won't attempt to explain the relative order/disorder between countries nor do we have the capability to predict Acts of Nature. Using macroeconomic literature and open source data, this repo attempts to rank countries by 1) the value of exported goods and services, 2) debt levels(both public and private), and 3) the strength of each country's currency.
**Data Source**

---------------
We use the Atlas of Economic Complexity from the Growth Lab at Harvard University because this data source is: 1) Detailed down to the product level that each country in the World trades from 1962 to 2020. 2) Standardized to simplify the process of building a time series to track changes over time. 3) Regularly used and highly cited source with over eighty thousand downloads. It is also publicly available and can be downloaded here.


**Exploratory Data Analysis**
--------------------------------

Below we plot trade relationships between the United States, China, and Russia. For this plot, we sum data for the latest available year, 2020. The trade balance is measured in Billions of US dollars.

In 2020, China had a surplus relative to the United States, Hong Kong, Great Britain, India, and the Netherlands. With the United States, China exported $200+ Billion dollars worth of products and services in excess of the value of products/services China imported from the United States. Interestingly, Russia and the US had negligible differences in terms of the monetary value of their bilateral imports/exports.

**Figure 1: 2020 Trade Balance**
![](output/deficit_plot_us_chn_rus.png)

Not all products are created equal. The plot above shows aggregated measures of exports but does not include details on what these traded products are. In the table below, we show the top exports for each of the countries from figure 1 classified by Maslow's hierarchy of needs. 

**Interactive Application**

https://www.loom.com/share/3a51af3bd7f64a10a6db2eee8c78a872


**How to run Interactive App on your local machine**
```{python}
git clone https://github.com/LNshuti/international-trade-ilustrated.git
cd international-trade-ilustrated
pip install -r requirements.txt

cd python/app
streamlit run trade-app.py
```
**United States Trade Balance: 2020**
```{python}
    2.13 T - 2.72 T = 0.59 T Trade Deficit
    
    0.59 T / 330 M = $1788 Deficit Per Person
```


**Figure 2: Top 20 Indebtness by Country**

![image](https://user-images.githubusercontent.com/13305262/225175665-afd602ce-0a14-4957-9b7e-aaff10be89a0.png)


**Figure 3 GDP per capita (current US$)**

<img width="587" alt="image" src="https://user-images.githubusercontent.com/13305262/225187962-8233cdde-02da-4e50-912c-48935734320b.png">


**USA Imports**
![image](https://user-images.githubusercontent.com/13305262/222725045-b9e8ff4b-c6f5-496e-9002-5a51225c6dce.png)

**USA Exports**
![image](https://user-images.githubusercontent.com/13305262/222726256-b249f3e8-595b-4852-b320-a00e11505707.png)

**China Trade Balance:**
```{python}
2.01 T - 2.81 T = 0.8 T Trade Deficit
0.8 T /  1.41 B = $57 Deficit Per Person
```

**China Imports**
![image](https://user-images.githubusercontent.com/13305262/222733866-612d0724-408e-450e-ac37-238903e94eb2.png)

**China Exports**
![image](https://user-images.githubusercontent.com/13305262/222734074-e476b741-0aa5-4b0a-9aa1-b526288ad4ee.png)

**Mexico Imports**
![image](https://user-images.githubusercontent.com/13305262/224182208-6521af51-d492-4a6f-8285-2d4812fccf81.png)

**Mexico Exports**
![image](https://user-images.githubusercontent.com/13305262/224182564-e7808558-97f1-46ed-bb2d-dd38fd37fd2f.png)

**Mexico Opportunities**
![image](https://user-images.githubusercontent.com/13305262/224183500-945feb10-d81d-4960-8818-efdf7677f22c.png)


### Global Market Share
-----------------------

**China**
![image](https://user-images.githubusercontent.com/13305262/223608271-1ad12f22-2359-4eda-8866-ad275714e2de.png)

**USA**
![image](https://user-images.githubusercontent.com/13305262/223609254-be20685e-f174-41d5-ad37-f0500a8b3f95.png)

**Russian Federation**
![image](https://user-images.githubusercontent.com/13305262/223883135-25d3f7a7-dd83-462a-a12c-3a087478fe1d.png)

**Mexico**
![image](https://user-images.githubusercontent.com/13305262/224182961-da9d4faf-eff1-409b-a045-857b3ccfbc24.png)

**Rising Asia**
<img width="1100" alt="image" src="https://user-images.githubusercontent.com/13305262/224469997-41a1d565-b298-4b8b-b802-83d12ee99fef.png">

**Declining Museum**
<img width="1097" alt="image" src="https://user-images.githubusercontent.com/13305262/224470336-2fe72fb6-1c3d-4a59-b85e-2e8820b8e78b.png">

**South America**
<img width="1100" alt="image" src="https://user-images.githubusercontent.com/13305262/224470461-f6f5e8a9-6c7e-433f-b6f8-5413cc8fddd1.png">

**USA USA USA**
<img width="823" alt="image" src="https://user-images.githubusercontent.com/13305262/224470573-a55adc14-3199-4c84-8eaa-76fb5bccb723.png">

**SouthEastern Asia**
<img width="1089" alt="image" src="https://user-images.githubusercontent.com/13305262/224470902-cd4c5514-73ee-453d-ac8b-a03e84b28873.png">

**North Europe**
<img width="1099" alt="image" src="https://user-images.githubusercontent.com/13305262/224471002-e1a04cd6-912e-4c0f-9ecc-90001ee7b855.png">


**Figure 2: Top 10 Product Imports**

![](output/usa_brics_top10_imports.png)

**Global Currencies and Reserves**

<img width="823" alt="image" src="https://user-images.githubusercontent.com/13305262/222988079-7a5db2d7-b1f5-4f00-8aef-2fb2f5f53561.png">

<img width="813" alt="image" src="https://user-images.githubusercontent.com/13305262/222987949-74974087-0077-43ec-91d5-ed9f72de9213.png">
 
**Source:** https://data.imf.org/?sk=E6A5F467-C14B-4AA8-9F6D-5A09EC4E62A4

![App](https://www.loom.com/share/3a51af3bd7f64a10a6db2eee8c78a872)

**Appendix:**
-------------

The charts below are taken from the Atlas for Economic Complexity website at Harvard University. For more details follow this [link](https://atlas.cid.harvard.edu/explore ).

**Canadian Exports**
![image](https://user-images.githubusercontent.com/13305262/222723723-ab2710a0-22a9-43cb-9d91-34ec055d9c32.png)

**Canadian Imports**
![image](https://user-images.githubusercontent.com/13305262/222724364-f1d06c2f-a038-418f-a15b-5add1aa597dc.png)

**France Exports**
![image](https://user-images.githubusercontent.com/13305262/223588654-0f44b1f3-1e16-44e9-9946-d4f2f2610bbf.png)

**France Imports**
![image](https://user-images.githubusercontent.com/13305262/223589164-a3ad54ed-a9e7-47df-a237-43866d0859c5.png)

**France Trade Partners**

**Exports**
![image](https://user-images.githubusercontent.com/13305262/223589349-f752df34-a921-4efd-a392-fe1c16569444.png)

**Imports**
![image](https://user-images.githubusercontent.com/13305262/223589730-6c730a59-802c-479d-af12-e210882d23fb.png)

**Russian Exports**
![image](https://user-images.githubusercontent.com/13305262/222796825-141d333a-1d75-40b8-822a-45e247b88d49.png)

**Russian Imports**
![image](https://user-images.githubusercontent.com/13305262/222797098-7d85e1b0-4b21-4925-9c5f-db75ef910d7a.png)

**Russian Trade Partners Circa 2020. Imports by Russia**
![image](https://user-images.githubusercontent.com/13305262/222797482-2f3be7e8-1763-4f63-b24e-36d1d08af964.png)

**Russian Trade Partners Circa 2020. Exports by Russia**
![image](https://user-images.githubusercontent.com/13305262/222798408-4eff9d74-004b-419a-b809-2fca04cfdec2.png)

**German Imports**
![image](https://user-images.githubusercontent.com/13305262/222731468-13c021cb-0aed-430f-a7a6-88c28db9acb5.png)

**German Exports**
![image](https://user-images.githubusercontent.com/13305262/222840334-14816075-056f-422d-b998-ad85ec50b034.png)

### References 
1. The Growth Lab at Harvard University. International Trade Data (SITC, Rev. 2). 2019-05-31. 2019. V5. Harvard Dataverse. URL. https://doi.org/10.7910/DVN/H8SFD2. doi/10.7910/DVN/H8SFD2

2. Wu, Kai. September 2022. Liquid Venture Capital. Sparkline Capital. https://www.sparklinecapital.com/post/liquid-venture-capital

3. Replicate Canada Export Plot. https://atlas.cid.harvard.edu/explore 
