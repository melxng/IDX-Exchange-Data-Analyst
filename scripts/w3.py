import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path


# read in files
cleaned_dir = Path("../data/cleaned_csv")
cleaned_dir.mkdir(exist_ok=True)


sold = pd.read_csv(
    cleaned_dir / "sold_residential_cleaned.csv",
    low_memory=False
)

listing = pd.read_csv(
    cleaned_dir / "listings_residential_cleaned.csv",
    low_memory=False
)

print("Sold shape:", sold.shape)
print("Listing shape:", listing.shape)


url = (
    "https://fred.stlouisfed.org/"
    "graph/fredgraph.csv?id=MORTGAGE30US"
)

mortgage = pd.read_csv(
    url,
    parse_dates=["observation_date"]
)

mortgage.columns = [
    "date",
    "rate_30yr_fixed"
]


# convert the weekly mortgage rates to monthly averages
mortgage["year_month"] = (
    mortgage["date"]
    .dt.to_period("M")
)

mortgage_monthly = (
    mortgage
    .groupby("year_month")["rate_30yr_fixed"]
    .mean()
    .reset_index()
)


# clean up the dates --> get year-month dates for sold and listing datasets

sold["CloseDate"] = pd.to_datetime(sold["CloseDate"], errors="coerce")
listing["ListingContractDate"] = pd.to_datetime(listing["ListingContractDate"],errors="coerce")
sold["year_month"] = (sold["CloseDate"].dt.to_period("M"))

listing["year_month"] = (listing["ListingContractDate"].dt.to_period("M"))


# merge the mortgage rates onto the sold and listing datasets (that we cleaned from w2)

sold_with_rates = sold.merge(mortgage_monthly,on="year_month",how="left")
listing_with_rates = listing.merge(mortgage_monthly,on="year_month",how="left")

# validate the missing mortgage rates
sold_missing_rates = (sold_with_rates["rate_30yr_fixed"].isnull().sum())
listing_missing_rates = (listing_with_rates["rate_30yr_fixed"].isnull().sum())


# save datasets
sold_with_rates.to_csv(
    cleaned_dir / "sold_residential_with_rates.csv",
    index=False
)

listing_with_rates.to_csv(
    cleaned_dir / "listings_residential_with_rates.csv",
    index=False
)