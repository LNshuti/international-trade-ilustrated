# Use python to plot treemaps of exports by country and by product

import pandas as pd
import squarify
import matplotlib.pyplot as plt

# Read in the data
product_labs = pd.read_csv('../data/processed/SITCCodeandDescription.csv')
print(product_labs.head())


