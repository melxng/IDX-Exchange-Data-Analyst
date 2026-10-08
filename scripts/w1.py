import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


# set path to data folder
data_dir = Path("../data/raw_csv")

# grab all the "listing" csv files in the data folder
listing_files = sorted(data_dir.glob("CRMLSListing*.csv")) # avoid hard coding the file names
sold_files = sorted(data_dir.glob("CRMLSSold*.csv"))


# empty list to hold the dataframes for each listing file
listing_df = []

# read in each listing file, then append it to listing_df
for file in listing_files:
    df = pd.read_csv(file, low_memory=False)
    listing_df.append(df)


# get the total number of rows in all the listing files
listings_rows_before = sum(len(df) for df in listing_df)
listings = pd.concat(listing_df, ignore_index=True)

# number of listing rows before concatenation is 822087 (this is incorrect idk why i have the wrong number uhh what)
#it's supposed to be 860898 rows before filter
listings_before_filter = len(listings)

listings_residential = listings[listings["PropertyType"] == "Residential"].copy()



sold_dfs = []

for file in sold_files:
    df = pd.read_csv(file, low_memory=False)
    sold_dfs.append(df)

sold_rows_before = sum(len(df) for df in sold_dfs)
sold = pd.concat(sold_dfs, ignore_index=True)

sold_before_filter = len(sold)
sold_residential = sold[sold["PropertyType"] == "Residential"].copy()

# LISTING --> 547162 rows after filter (this needs to be 547162)
# SOLD --> 414054 rows after filter


# create the csv 
output_dir = Path("../data/processed_csv")
output_dir.mkdir(exist_ok=True)

listings_residential.to_csv(output_dir / "listings_residential.csv", index=False)

sold_residential.to_csv(output_dir / "sold_residential.csv",index=False)