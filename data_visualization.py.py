"""
SPECScout - DATA VISUALIZATION

Creates 10 visualizations from:
    SpecScout_Dataset_Fully_Cleaned.csv

This is a separate file from DATA_ANALYTICS.py.
It creates graph images only when you run this script.

Required libraries:
    pip install pandas matplotlib

Run:
    python visualization.py

Keep this file and the CSV dataset in the same folder.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. LOAD DATASET
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "SpecScout_Dataset_Fully_Cleaned.csv")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "SpecScout_Visualizations")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError(
        "Dataset not found. Keep SpecScout_Dataset_Fully_Cleaned.csv "
        "in the same folder as visualization.py."
    )

df = pd.read_csv(FILE_PATH)
df.columns = df.columns.str.strip()
df = df.dropna(how="all")

# Convert numeric columns
numeric_columns = [
    "price_inr", "rating", "ram_gb", "storage_gb",
    "battery_mah", "display_inches"
]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Consistent graph formatting
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 15
plt.rcParams["axes.labelsize"] = 11
plt.rcParams["font.size"] = 10


def has_columns(*columns):
    missing = [col for col in columns if col not in df.columns]
    if missing:
        print("Skipped graph. Missing columns:", ", ".join(missing))
        return False
    return True


def save_graph(filename):
    """Save the current graph as a high-resolution PNG image."""
    plt.tight_layout()
    path = os.path.join(OUTPUT_FOLDER, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Created:", filename)


print("\n========== SPECScout VISUALIZATION ==========")
print("Dataset records:", len(df))
print("Generating 10 graphs...\n")

# ---------------------------------------------------------
# GRAPH 1 - TOP 10 SMARTPHONE BRANDS
# ---------------------------------------------------------
if has_columns("brand"):
    data = df["brand"].dropna().value_counts().head(10).sort_values()
    plt.figure()
    data.plot(kind="barh")
    plt.title("Top 10 Smartphone Brands")
    plt.xlabel("Number of Smartphones")
    plt.ylabel("Brand")
    save_graph("01_top_10_brands.png")


# ---------------------------------------------------------
# GRAPH 2 - AVERAGE PRICE BY TOP 10 BRANDS
# ---------------------------------------------------------
if has_columns("brand", "price_inr"):
    data = (
        df.groupby("brand")["price_inr"].mean()
        .dropna().sort_values(ascending=False).head(10).sort_values()
    )
    plt.figure()
    data.plot(kind="barh")
    plt.title("Top 10 Brands by Average Smartphone Price")
    plt.xlabel("Average Price (INR)")
    plt.ylabel("Brand")
    save_graph("02_average_price_by_brand.png")


# ---------------------------------------------------------
# GRAPH 3 - PRICE SEGMENT DISTRIBUTION
# ---------------------------------------------------------
if has_columns("price_segment"):
    data = df["price_segment"].dropna().value_counts()
    plt.figure()
    data.plot(kind="bar")
    plt.title("Smartphone Price Segment Distribution")
    plt.xlabel("Price Segment")
    plt.ylabel("Number of Smartphones")
    plt.xticks(rotation=30, ha="right")
    save_graph("03_price_segment_distribution.png")


# ---------------------------------------------------------
# GRAPH 4 - RATING BAND DISTRIBUTION
# ---------------------------------------------------------
if has_columns("rating_band"):
    data = df["rating_band"].dropna().value_counts()
    plt.figure()
    data.plot(kind="bar")
    plt.title("Smartphone Rating Band Distribution")
    plt.xlabel("Rating Band")
    plt.ylabel("Number of Smartphones")
    plt.xticks(rotation=30, ha="right")
    save_graph("04_rating_band_distribution.png")


# ---------------------------------------------------------
# GRAPH 5 - PRICE VS RATING
# ---------------------------------------------------------
if has_columns("price_inr", "rating"):
    data = df[["price_inr", "rating"]].dropna()
    plt.figure()
    plt.scatter(data["price_inr"], data["rating"], alpha=0.65)
    plt.title("Smartphone Price vs Rating")
    plt.xlabel("Price (INR)")
    plt.ylabel("Rating")
    save_graph("05_price_vs_rating.png")


# ---------------------------------------------------------
# GRAPH 6 - 5G AVAILABILITY
# ---------------------------------------------------------
if has_columns("has_5g"):
    values = df["has_5g"].map({True: "Yes", False: "No"})
    values = values.fillna(df["has_5g"].astype(str).str.strip())
    values = values.replace({
        "1": "Yes", "0": "No",
        "true": "Yes", "false": "No",
        "yes": "Yes", "no": "No"
    })
    data = values.value_counts()
    plt.figure()
    plt.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("5G Availability in Smartphones")
    save_graph("06_5g_availability.png")


# ---------------------------------------------------------
# GRAPH 7 - RAM CAPACITY DISTRIBUTION
# ---------------------------------------------------------
if has_columns("ram_gb"):
    data = df["ram_gb"].dropna().value_counts().sort_index()
    plt.figure()
    data.plot(kind="bar")
    plt.title("Smartphone RAM Capacity Distribution")
    plt.xlabel("RAM (GB)")
    plt.ylabel("Number of Smartphones")
    plt.xticks(rotation=0)
    save_graph("07_ram_capacity_distribution.png")


# ---------------------------------------------------------
# GRAPH 8 - STORAGE CAPACITY DISTRIBUTION
# ---------------------------------------------------------
if has_columns("storage_gb"):
    data = df["storage_gb"].dropna().value_counts().sort_index()
    plt.figure()
    data.plot(kind="bar")
    plt.title("Smartphone Storage Capacity Distribution")
    plt.xlabel("Storage (GB)")
    plt.ylabel("Number of Smartphones")
    plt.xticks(rotation=0)
    save_graph("08_storage_capacity_distribution.png")


# ---------------------------------------------------------
# GRAPH 9 - BATTERY CAPACITY DISTRIBUTION
# ---------------------------------------------------------
if has_columns("battery_mah"):
    data = df["battery_mah"].dropna()
    plt.figure()
    plt.hist(data, bins=15, edgecolor="black")
    plt.title("Smartphone Battery Capacity Distribution")
    plt.xlabel("Battery Capacity (mAh)")
    plt.ylabel("Number of Smartphones")
    save_graph("09_battery_capacity_distribution.png")


# ---------------------------------------------------------
# GRAPH 10 - DISPLAY SIZE DISTRIBUTION
# ---------------------------------------------------------
if has_columns("display_inches"):
    data = df["display_inches"].dropna()
    plt.figure()
    plt.hist(data, bins=12, edgecolor="black")
    plt.title("Smartphone Display Size Distribution")
    plt.xlabel("Display Size (inches)")
    plt.ylabel("Number of Smartphones")
    save_graph("10_display_size_distribution.png")


# ---------------------------------------------------------
# FINAL MESSAGE
# ---------------------------------------------------------
print("\n============================================")
print("VISUALIZATION COMPLETED SUCCESSFULLY!")
print("============================================")
print("Graph images are saved in:")
print(OUTPUT_FOLDER)
print("Open that folder to view the generated graphs.")
