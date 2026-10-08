import pandas as pd
from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns
from pathlib import Path


CORE_FIELDS = [
    "PropertyType",
    "ClosePrice",
    "OriginalListPrice",
    "ListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "CountyOrParish",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "CloseDate",
    "ListingContractDate"
]

NUMERIC_FIELDS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt"
]

MARKET_FIELDS = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
    "CloseDate",
    "ListingContractDate",
    "CountyOrParish",
    "PropertyType"
]

DELIVERABLE_FIELDS = [
    "ClosePrice",
    "LivingArea",
    "DaysOnMarket"
]



data_dir = Path("../data/processed_csv")
report_dir = Path("../data/reports")

report_dir.mkdir(exist_ok=True)

listing_path = data_dir / "listings_residential.csv"
sold_path = data_dir / "sold_residential.csv"

listing = pd.read_csv(listing_path, low_memory=False)
sold = pd.read_csv(sold_path, low_memory=False)


print("Listings shape:", listing.shape) 
print("Sold shape:", sold.shape)

# Listings shape: (522931, 84) -- checking this later idk why it did that.
# Sold shape: (414054, 84)


# generate missing report for listing  dataset
missing_report_listing = pd.DataFrame({
    "MissingCount": listing.isnull().sum(),
    "MissingPercent": listing.isnull().mean() * 100
})

missing_report_listing["Above90PercentMissing"] = (missing_report_listing["MissingPercent"] > 90)
missing_report_listing = missing_report_listing.sort_values("MissingPercent",ascending=False)

fully_missing_listing = missing_report_listing[missing_report_listing["MissingPercent"] == 100]
high_missing_listing = missing_report_listing[missing_report_listing["Above90PercentMissing"]]



#generate missing rpport for sold dataset
missing_report_sold = pd.DataFrame({
    "MissingCount": sold.isnull().sum(),
    "MissingPercent": sold.isnull().mean() * 100
})

missing_report_sold["Above90PercentMissing"] = (missing_report_sold["MissingPercent"] > 90)
missing_report_sold = missing_report_sold.sort_values("MissingPercent",ascending=False)


# cols with more than 90% missing values
high_missing_sold = missing_report_sold[missing_report_sold["Above90PercentMissing"]]


# remove cfully empty cols from sold dataset
fully_missing_sold = missing_report_sold[missing_report_sold["MissingPercent"] == 100].index.tolist()

sold = sold.drop(columns=fully_missing_sold)

numeric_summary = pd.DataFrame({
    "min": sold[DELIVERABLE_FIELDS].min(),
    "max": sold[DELIVERABLE_FIELDS].max(),
    "mean": sold[DELIVERABLE_FIELDS].mean(),
    "med": sold[DELIVERABLE_FIELDS].median(),
    "25th percentile": sold[DELIVERABLE_FIELDS].quantile(0.25),
    "75th percentile": sold[DELIVERABLE_FIELDS].quantile(0.75),
    "95th percentile": sold[DELIVERABLE_FIELDS].quantile(0.95),
    "99th percentile": sold[DELIVERABLE_FIELDS].quantile(0.99)
})


# save the reports to csv
missing_report_sold.to_csv(
    report_dir / "sold_missing_report.csv"
)

missing_report_listing.to_csv(
    report_dir / "listing_missing_report.csv"
)

numeric_summary.to_csv(
    report_dir / "sold_numeric_summary.csv"
)

sold.to_csv(
    data_dir / "sold_residential_validated.csv",
    index=False
)
