"""
SPECScout - DATA ANALYTICS (TEXT / TABLE OUTPUT ONLY)

This program performs 10 data analyses on:
SpecScout_Dataset_Fully_Cleaned.csv

No charts, plots, or visualization image files are created.

Keep this Python file and the CSV dataset in the same folder.
Run:
    python DATA_ANALYTICS.py
"""

import os
import pandas as pd

# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "SpecScout_Dataset_Fully_Cleaned.csv")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "SpecScout_Analysis_CSV")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(
        "Dataset not found. Keep SpecScout_Dataset_Fully_Cleaned.csv "
        "in the same folder as DATA_ANALYTICS.py."
    )

df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()
df = df.dropna(how="all")

# Convert important numeric fields safely
numeric_columns = [
    "price_inr", "rating", "ram_gb", "storage_gb",
    "battery_mah", "display_inches",
    "resolution_width_px", "resolution_height_px"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


def save_result(data, filename, title):
    """Print an analysis table and save it as a CSV file."""
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)
    if data.empty:
        print("No data available for this analysis.")
    else:
        print(data.to_string(index=False))
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    data.to_csv(output_path, index=False)
    print("\nSaved:", output_path)


def has_columns(*columns):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        print("\nSkipped analysis. Missing columns:", ", ".join(missing))
        return False
    return True


print("\n========== SPECScout DATASET INFORMATION ==========")
print("Total records:", len(df))
print("Total columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())

# Save a general dataset summary
summary = pd.DataFrame({
    "Metric": ["Total Records", "Total Columns", "Duplicate Rows"],
    "Value": [len(df), len(df.columns), int(df.duplicated().sum())]
})
save_result(summary, "00_dataset_summary.csv", "DATASET SUMMARY")

# ---------------------------------------------------------
# ANALYSIS 1 - SMARTPHONE COUNT BY BRAND
# ---------------------------------------------------------
if has_columns("brand"):
    result = (
        df["brand"].dropna().value_counts()
        .rename_axis("Brand").reset_index(name="Number of Smartphones")
    )
    save_result(result, "01_smartphone_count_by_brand.csv",
                "ANALYSIS 1 - SMARTPHONE COUNT BY BRAND")

# ---------------------------------------------------------
# ANALYSIS 2 - AVERAGE PRICE BY BRAND
# ---------------------------------------------------------
if has_columns("brand", "price_inr"):
    result = (
        df.groupby("brand", dropna=True)["price_inr"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
        .rename(columns={
            "brand": "Brand",
            "count": "Number of Models",
            "mean": "Average Price (INR)",
            "min": "Minimum Price (INR)",
            "max": "Maximum Price (INR)"
        })
        .sort_values("Average Price (INR)", ascending=False)
        .round(2)
    )
    save_result(result, "02_average_price_by_brand.csv",
                "ANALYSIS 2 - AVERAGE PRICE BY BRAND")

# ---------------------------------------------------------
# ANALYSIS 3 - PRICE SEGMENT DISTRIBUTION
# ---------------------------------------------------------
if has_columns("price_segment"):
    result = (
        df["price_segment"].dropna().value_counts()
        .rename_axis("Price Segment")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "03_price_segment_distribution.csv",
                "ANALYSIS 3 - PRICE SEGMENT DISTRIBUTION")

# ---------------------------------------------------------
# ANALYSIS 4 - RATING BAND DISTRIBUTION
# ---------------------------------------------------------
if has_columns("rating_band"):
    result = (
        df["rating_band"].dropna().value_counts()
        .rename_axis("Rating Band")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "04_rating_band_distribution.csv",
                "ANALYSIS 4 - RATING BAND DISTRIBUTION")

# ---------------------------------------------------------
# ANALYSIS 5 - 5G AVAILABILITY
# ---------------------------------------------------------
if has_columns("has_5g"):
    values = df["has_5g"].map({True: "Yes", False: "No"})
    values = values.fillna(df["has_5g"].astype(str))
    result = (
        values.value_counts()
        .rename_axis("5G Availability")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "05_5g_availability.csv",
                "ANALYSIS 5 - 5G AVAILABILITY")

# ---------------------------------------------------------
# ANALYSIS 6 - RATING STATISTICS BY BRAND
# ---------------------------------------------------------
if has_columns("brand", "rating"):
    result = (
        df.groupby("brand")["rating"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
        .rename(columns={
            "brand": "Brand",
            "count": "Number of Models",
            "mean": "Average Rating",
            "min": "Minimum Rating",
            "max": "Maximum Rating"
        })
        .sort_values("Average Rating", ascending=False)
        .round(2)
    )
    save_result(result, "06_rating_statistics_by_brand.csv",
                "ANALYSIS 6 - RATING STATISTICS BY BRAND")

# ---------------------------------------------------------
# ANALYSIS 7 - RAM CAPACITY DISTRIBUTION
# ---------------------------------------------------------
if has_columns("ram_gb"):
    result = (
        df["ram_gb"].dropna().value_counts().sort_index()
        .rename_axis("RAM (GB)")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "07_ram_capacity_distribution.csv",
                "ANALYSIS 7 - RAM CAPACITY DISTRIBUTION")

# ---------------------------------------------------------
# ANALYSIS 8 - STORAGE CAPACITY DISTRIBUTION
# ---------------------------------------------------------
if has_columns("storage_gb"):
    result = (
        df["storage_gb"].dropna().value_counts().sort_index()
        .rename_axis("Storage (GB)")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "08_storage_capacity_distribution.csv",
                "ANALYSIS 8 - STORAGE CAPACITY DISTRIBUTION")

# ---------------------------------------------------------
# ANALYSIS 9 - AVERAGE BATTERY CAPACITY BY BRAND
# ---------------------------------------------------------
if has_columns("brand", "battery_mah"):
    result = (
        df.groupby("brand")["battery_mah"]
        .agg(["count", "mean", "min", "max"])
        .reset_index()
        .rename(columns={
            "brand": "Brand",
            "count": "Number of Models",
            "mean": "Average Battery (mAh)",
            "min": "Minimum Battery (mAh)",
            "max": "Maximum Battery (mAh)"
        })
        .sort_values("Average Battery (mAh)", ascending=False)
        .round(2)
    )
    save_result(result, "09_battery_capacity_by_brand.csv",
                "ANALYSIS 9 - BATTERY CAPACITY BY BRAND")

# ---------------------------------------------------------
# ANALYSIS 10 - OPERATING SYSTEM DISTRIBUTION
# ---------------------------------------------------------
if has_columns("os_family"):
    result = (
        df["os_family"].dropna().value_counts()
        .rename_axis("Operating System")
        .reset_index(name="Number of Smartphones")
    )
    result["Percentage"] = (
        result["Number of Smartphones"] / result["Number of Smartphones"].sum() * 100
    ).round(2)
    save_result(result, "10_operating_system_distribution.csv",
                "ANALYSIS 10 - OPERATING SYSTEM DISTRIBUTION")

# ---------------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------------
print("\n" + "=" * 65)
print("DATA ANALYTICS COMPLETED SUCCESSFULLY!")
print("=" * 65)
print("No graphs or visualization images were generated.")
print("Analysis tables are saved as CSV files in:")
print(OUTPUT_FOLDER)
print("\nGenerated CSV files:")
for filename in sorted(os.listdir(OUTPUT_FOLDER)):
    if filename.lower().endswith(".csv"):
        print("-", filename)
