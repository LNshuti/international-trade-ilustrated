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

**FIgure 0: United States Global Market Share**

![United States of America’s Global Market Share, 1995 – 2020](https://user-images.githubusercontent.com/13305262/234189278-91c88385-a54b-43a6-870c-213d8caa33c4.png)


**Figure 1: United States Economic Size**

![What did United States of America export in 2020](https://user-images.githubusercontent.com/13305262/234188787-d6185e20-bfcb-40a8-9d8d-b93fa9b614c1.png)


Below we plot trade relationships between the United States, China, and Russia. For this plot, we sum data for the latest available year, 2020. The trade balance is measured in Billions of US dollars.

In 2020, China exported $200+ Billion dollars worth of products and services in excess of the value of products/services China imported from the United States. Interestingly, Russia and the US had negligible differences in terms of the monetary value of their bilateral imports/exports.

**Figure 2: 2020 US Exports to China**

![What did United States of America export to China in 2020](https://user-images.githubusercontent.com/13305262/233839682-0bfd688d-83e3-41f1-aa77-b246768751a5.png)

**Figure 3: 2020 Chinese Exports to the US**

![What did United States of America import from China in 2020](https://user-images.githubusercontent.com/13305262/233839790-0c38a57b-1e1b-46b3-a893-2830cfc4df81.png)

**Figure 4: Russian Exports to the US**

![What did United States of America import from Russia in 2020](https://user-images.githubusercontent.com/13305262/233840120-b46a86d5-1cff-459d-b06a-dfa8ed2c0abd.png)

**Figure 5: US exports to Russia** 

![What did United States of America export to Russia in 2020](https://user-images.githubusercontent.com/13305262/233840141-e48b1b5f-59c1-458b-b41e-9d5dda461713.png)

**Figure 6: Chinese Exports to France**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/f67bd2b8-bf46-4c33-81f5-2a93162ccd4b)

**Figure 7: US Exports to France**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/dc894a6e-4d2f-4a80-8187-59f688bbae4f)

**Figure 8: French Exports**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/9d76bb68-3b2b-4757-8c64-fa747a40f0a9)

**Figure 9: French Imports**

![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/1337bf49-ce43-4b8c-bb2c-fd2a5ff8742c)



**Interactive Application**

https://www.loom.com/share/3a51af3bd7f64a10a6db2eee8c78a872


![image](https://github.com/LNshuti/international-trade-ilustrated/assets/13305262/0c08202b-f662-45a7-a9aa-aa7134c579d4)


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
