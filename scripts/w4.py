import pandas as pd
from pathlib import Path


# read in enriched datasets from week 3
cleaned_dir = Path("../data/cleaned_csv")
report_dir = Path("../data/reports")
output_dir = Path("../data/analysis_ready")

report_dir.mkdir(exist_ok=True)
output_dir.mkdir(exist_ok=True)


sold = pd.read_csv(cleaned_dir / "sold_residential_with_rates.csv", low_memory=False)
listing = pd.read_csv(cleaned_dir / "listings_residential_with_rates.csv", low_memory=False)



# convert date fields to dateitime

date_fields = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate"
]

for column in date_fields:
    if column in listing.columns:
        listing[column] = pd.to_datetime(
            listing[column],
            errors="coerce"
        )


for column in date_fields:
    if column in sold.columns:
        sold[column] = pd.to_datetime(
            sold[column],
            errors="coerce"
        )


print("\nSold date field types:")
print(
    sold[
        [
            column
            for column in date_fields
            if column in sold.columns
        ]
    ].dtypes
)

print("\nListing date field types:")
print(
    listing[
        [
            column
            for column in date_fields
            if column in listing.columns
        ]
    ].dtypes
)


# --------------------------------------------------
# remove redundant listing columns
# --------------------------------------------------

listing_drop_columns = [
    "PropertyType.1",
    "ListAgentFirstName.1",
    "DaysOnMarket.1",
    "LivingArea.1",
    "Longitude.1",
    "Latitude.1",
    "ListPrice.1",
    "ListAgentLastName.1",
    "CloseDate.1",
    "UnparsedAddress.1"
]

listing = listing.drop(
    columns=[
        column
        for column in listing_drop_columns
        if column in listing.columns
    ]
)

print("\nDropped listing columns:")
print(listing_drop_columns)


# --------------------------------------------------
# ensure numeric fields are numeric
# --------------------------------------------------

numeric_fields = [
    "OriginalListPrice",
    "ClosePrice",
    "Latitude",
    "Longitude",
    "LivingArea",
    "ListPrice",
    "DaysOnMarket",
    "ListingKeyNumeric",
    "ParkingTotal",
    "LotSizeAcres",
    "YearBuilt",
    "StreetNumberNumeric",
    "BathroomsTotalInteger",
    "BuyerAgencyCompensation",
    "BuildingAreaTotal",
    "BedroomsTotal",
    "BelowGradeFinishedArea",
    "Stories",
    "LotSizeArea",
    "MainLevelBedrooms",
    "GarageSpaces",
    "AssociationFee",
    "LotSizeSquareFeet",
    "rate_30yr_fixed"
]


for column in numeric_fields:
    if column in listing.columns:
        listing[column] = pd.to_numeric(
            listing[column],
            errors="coerce"
        )


for column in numeric_fields:
    if column in sold.columns:
        sold[column] = pd.to_numeric(
            sold[column],
            errors="coerce"
        )


print("\nSold numeric field types:")
print(
    sold[
        [
            column
            for column in numeric_fields
            if column in sold.columns
        ]
    ].dtypes
)


print("\nListing numeric field types:")
print(
    listing[
        [
            column
            for column in numeric_fields
            if column in listing.columns
        ]
    ].dtypes
)


# --------------------------------------------------
# flag invalid numeric values
# --------------------------------------------------

listing["invalid_close_price"] = (
    listing["ClosePrice"] <= 0
)

listing["invalid_living_area"] = (
    listing["LivingArea"] <= 0
)

listing["invalid_days_on_market"] = (
    listing["DaysOnMarket"] < 0
)

listing["invalid_bedrooms"] = (
    listing["BedroomsTotal"] < 0
)

listing["invalid_bathrooms"] = (
    listing["BathroomsTotalInteger"] < 0
)


sold["invalid_close_price"] = (
    sold["ClosePrice"] <= 0
)

sold["invalid_living_area"] = (
    sold["LivingArea"] <= 0
)

sold["invalid_days_on_market"] = (
    sold["DaysOnMarket"] < 0
)

sold["invalid_bedrooms"] = (
    sold["BedroomsTotal"] < 0
)

sold["invalid_bathrooms"] = (
    sold["BathroomsTotalInteger"] < 0
)


# summarize invalid numeric values

invalid_numeric_summary_listing = pd.Series({
    "ClosePrice <= 0":
        listing["invalid_close_price"].sum(),

    "LivingArea <= 0":
        listing["invalid_living_area"].sum(),

    "DaysOnMarket < 0":
        listing["invalid_days_on_market"].sum(),

    "BedroomsTotal < 0":
        listing["invalid_bedrooms"].sum(),

    "BathroomsTotalInteger < 0":
        listing["invalid_bathrooms"].sum()
})


invalid_numeric_summary_sold = pd.Series({
    "ClosePrice <= 0":
        sold["invalid_close_price"].sum(),

    "LivingArea <= 0":
        sold["invalid_living_area"].sum(),

    "DaysOnMarket < 0":
        sold["invalid_days_on_market"].sum(),

    "BedroomsTotal < 0":
        sold["invalid_bedrooms"].sum(),

    "BathroomsTotalInteger < 0":
        sold["invalid_bathrooms"].sum()
})


print("\nInvalid numeric values - listing:")
print(invalid_numeric_summary_listing)

print("\nInvalid numeric values - sold:")
print(invalid_numeric_summary_sold)


# --------------------------------------------------
# date consistency checks
# --------------------------------------------------

listing["listing_after_close_flag"] = (
    listing["ListingContractDate"] >
    listing["CloseDate"]
)

listing["purchase_after_close_flag"] = (
    listing["PurchaseContractDate"] >
    listing["CloseDate"]
)

listing["negative_timeline_flag"] = (
    listing["ListingContractDate"] >
    listing["PurchaseContractDate"]
)


sold["listing_after_close_flag"] = (
    sold["ListingContractDate"] >
    sold["CloseDate"]
)

sold["purchase_after_close_flag"] = (
    sold["PurchaseContractDate"] >
    sold["CloseDate"]
)

sold["negative_timeline_flag"] = (
    sold["ListingContractDate"] >
    sold["PurchaseContractDate"]
)


date_summary_listing = pd.Series({
    "listing_after_close_flag":
        listing["listing_after_close_flag"].sum(),

    "purchase_after_close_flag":
        listing["purchase_after_close_flag"].sum(),

    "negative_timeline_flag":
        listing["negative_timeline_flag"].sum()
})


date_summary_sold = pd.Series({
    "listing_after_close_flag":
        sold["listing_after_close_flag"].sum(),

    "purchase_after_close_flag":
        sold["purchase_after_close_flag"].sum(),

    "negative_timeline_flag":
        sold["negative_timeline_flag"].sum()
})


print("\nDate consistency flags - listing:")
print(date_summary_listing)

print("\nDate consistency flags - sold:")
print(date_summary_sold)


# --------------------------------------------------
# geographic data quality checks
# --------------------------------------------------

listing["missing_coordinates_flag"] = (
    listing["Latitude"].isnull()
    |
    listing["Longitude"].isnull()
)

listing["zero_coordinates_flag"] = (
    (listing["Latitude"] == 0)
    |
    (listing["Longitude"] == 0)
)

listing["positive_longitude_flag"] = (
    listing["Longitude"] > 0
)

listing["implausible_coordinates_flag"] = (
    (listing["Latitude"] < 32.3)
    |
    (listing["Latitude"] > 42.2)
    |
    (listing["Longitude"] > -113.9)
    |
    (listing["Longitude"] < -124.7)
)


sold["missing_coordinates_flag"] = (
    sold["Latitude"].isnull()
    |
    sold["Longitude"].isnull()
)

sold["zero_coordinates_flag"] = (
    (sold["Latitude"] == 0)
    |
    (sold["Longitude"] == 0)
)

sold["positive_longitude_flag"] = (
    sold["Longitude"] > 0
)

sold["implausible_coordinates_flag"] = (
    (sold["Latitude"] < 32.3)
    |
    (sold["Latitude"] > 42.2)
    |
    (sold["Longitude"] > -113.9)
    |
    (sold["Longitude"] < -124.7)
)


geo_summary_listing = pd.Series({
    "Missing coordinates":
        listing["missing_coordinates_flag"].sum(),

    "Zero coordinates":
        listing["zero_coordinates_flag"].sum(),

    "Positive longitude":
        listing["positive_longitude_flag"].sum(),

    "Implausible California coordinates":
        listing["implausible_coordinates_flag"].sum()
})


geo_summary_sold = pd.Series({
    "Missing coordinates":
        sold["missing_coordinates_flag"].sum(),

    "Zero coordinates":
        sold["zero_coordinates_flag"].sum(),

    "Positive longitude":
        sold["positive_longitude_flag"].sum(),

    "Implausible California coordinates":
        sold["implausible_coordinates_flag"].sum()
})


print("\nGeographic data quality - listing:")
print(geo_summary_listing)

print("\nGeographic data quality - sold:")
print(geo_summary_sold)


# --------------------------------------------------
# combine invalid numeric flags
# --------------------------------------------------

listing["invalid_numeric_flag"] = (
    listing["invalid_close_price"]
    |
    listing["invalid_living_area"]
    |
    listing["invalid_days_on_market"]
    |
    listing["invalid_bedrooms"]
    |
    listing["invalid_bathrooms"]
)


sold["invalid_numeric_flag"] = (
    sold["invalid_close_price"]
    |
    sold["invalid_living_area"]
    |
    sold["invalid_days_on_market"]
    |
    sold["invalid_bedrooms"]
    |
    sold["invalid_bathrooms"]
)


# save reports

invalid_numeric_summary_listing.to_csv(
    report_dir / "week4_5_listing_invalid_numeric_summary.csv"
)

invalid_numeric_summary_sold.to_csv(
    report_dir / "week4_5_sold_invalid_numeric_summary.csv"
)

date_summary_listing.to_csv(
    report_dir / "week4_5_listing_date_summary.csv"
)