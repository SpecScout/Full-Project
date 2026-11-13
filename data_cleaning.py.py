"""
SpecScout Smartphone Dataset - Data Cleaning Script
--------------------------------------------------
Input:
    SpecScout-Dataset-Cleaned-Updated.xlsx

Output:
    SpecScout_Dataset_Fully_Cleaned.xlsx
    SpecScout_Dataset_Fully_Cleaned.csv

Install:
    pip install pandas openpyxl

This is a reconstructed, rule-based cleaning script based on the
SpecScout cleaned workbook. It identifies common misplaced specification
values, extracts numeric fields, derives analysis columns, and removes
rows that are missing required information.

Important:
- Review the "Removed Rows" and "Data Quality Report" sheets.
- Rule-based classification cannot safely identify every unusual value.
- Keep the original workbook as a backup.
"""

from pathlib import Path
import re
import pandas as pd

# -------------------------- SETTINGS --------------------------

INPUT_FILE = "SpecScout-Dataset-Cleaned-Updated.xlsx"
OUTPUT_EXCEL = "SpecScout_Dataset_Fully_Cleaned.xlsx"
OUTPUT_CSV = "SpecScout_Dataset_Fully_Cleaned.csv"

# Fields required for a row to be retained.
REQUIRED_FIELDS = [
    "model", "price_inr", "rating", "sim", "processor",
    "ram", "battery", "display", "camera", "card", "os"
]

SOURCE_SPEC_COLUMNS = [
    "sim", "processor", "ram", "battery",
    "display", "camera", "card", "os"
]

# ---------------------- HELPER FUNCTIONS ----------------------

def clean_text(value):
    """Convert a cell to clean text; treat blanks and NaN as empty."""
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def first_number(value):
    """Extract the first number from text such as '5000 mAh' or '6.7 inches'."""
    match = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", clean_text(value))
    if not match:
        return None
    return float(match.group(0).replace(",", ""))


def classify_specification(value):
    """
    Identify which specification column a text value belongs to.
    Returns a column name, or None if the value is not confidently classified.
    """
    text = clean_text(value)
    low = text.lower()

    if not text:
        return None

    # Operating system
    if re.search(r"\b(android|ios|harmonyos|kaios|windows phone)\b", low):
        return "os"

    # Battery
    if re.search(r"\bmah\b", low):
        return "battery"

    # Display: size, resolution, or refresh rate
    if (
        re.search(r"\binches?\b", low)
        or re.search(r"\b\d{3,4}\s*x\s*\d{3,4}\b", low)
        or re.search(r"\b\d{2,3}\s*hz\b", low)
    ):
        return "display"

    # Camera
    if re.search(r"\bmp\b", low) and re.search(
        r"(camera|rear|front|quad|triple|dual|selfie|mp)", low
    ):
        return "camera"

    # Memory card support
    if re.search(r"(memory card|microsd|micro sd|tf card)", low):
        return "card"

    # SIM and network details
    if re.search(r"(dual sim|single sim|nano sim|esim|5g|4g|3g|volte)", low):
        return "sim"

    # Processor / chipset
    if re.search(
        r"(snapdragon|dimensity|mediatek|helio|exynos|tensor|bionic|kirin|"
        r"unisoc|spreadtrum|octa core|quad core|processor|chipset)", low
    ):
        return "processor"

    # RAM and internal storage
    if re.search(r"\b(ram|inbuilt|internal storage|gb ram)\b", low):
        return "ram"

    return None


def extract_memory_values(ram_text):
    """Extract RAM and storage sizes in GB from a combined RAM field."""
    text = clean_text(ram_text)
    ram_match = re.search(r"(\d+(?:\.\d+)?)\s*gb\s*ram", text, re.I)
    storage_match = re.search(
        r"(\d+(?:\.\d+)?)\s*gb\s*(?:inbuilt|storage|internal)", text, re.I
    )

    ram_gb = float(ram_match.group(1)) if ram_match else None
    storage_gb = float(storage_match.group(1)) if storage_match else None

    # Some source rows use a compact form such as "8 GB RAM, 128 GB inbuilt".
    if ram_gb is None:
        numbers = re.findall(r"(\d+(?:\.\d+)?)\s*gb", text, re.I)
        if numbers:
            ram_gb = float(numbers[0])
    if storage_gb is None:
        numbers = re.findall(r"(\d+(?:\.\d+)?)\s*gb", text, re.I)
        if len(numbers) >= 2:
            storage_gb = float(numbers[1])

    return ram_gb, storage_gb


def extract_display_values(display_text):
    """Extract screen size, resolution, and refresh rate."""
    text = clean_text(display_text)

    size = re.search(r"(\d+(?:\.\d+)?)\s*inches?", text, re.I)
    resolution = re.search(r"(\d{3,4})\s*x\s*(\d{3,4})", text, re.I)
    refresh = re.search(r"(\d{2,3})\s*hz", text, re.I)

    return (
        float(size.group(1)) if size else None,
        int(resolution.group(1)) if resolution else None,
        int(resolution.group(2)) if resolution else None,
        f"{refresh.group(1)} Hz" if refresh else "Not specified"
    )


def brand_from_model(model):
    """Infer brand from the beginning of the model name."""
    model = clean_text(model)
    first = model.split()[0].lower() if model else ""

    known_brands = {
        "apple": "Apple",
        "samsung": "Samsung",
        "google": "Google",
        "motorola": "Motorola",
        "moto": "Motorola",
        "oneplus": "OnePlus",
        "xiaomi": "Xiaomi",
        "redmi": "Xiaomi",
        "poco": "Poco",
        "oppo": "OPPO",
        "vivo": "vivo",
        "realme": "realme",
        "infinix": "Infinix",
        "tecno": "Tecno",
        "itel": "itel",
        "nokia": "Nokia",
        "iqoo": "iQOO",
        "huawei": "Huawei",
        "honor": "Honor",
        "nothing": "Nothing",
        "lava": "Lava",
        "micromax": "Micromax",
        "lyf": "Lyf",
        "asus": "ASUS",
        "sony": "Sony",
        "lg": "LG",
        "lenovo": "Lenovo",
        "blackberry": "BlackBerry",
        "meizu": "Meizu",
        "zte": "ZTE",
        "nubia": "Nubia",
        "coolpad": "Coolpad",
        "leeco": "LeEco",
        "le": "LeEco",
        "karbonn": "Karbonn",
        "panasonic": "Panasonic",
        "sharp": "Sharp",
        "cat": "CAT",
        "doogee": "Doogee",
        "ulefone": "Ulefone",
        "ikall": "iKall",
        "xolo": "Xolo",
        "gionee": "Gionee",
        "jio": "Jio",
    }
    return known_brands.get(first, model.split()[0] if model else "Not specified")


# ---------------------- LOAD SOURCE DATA ----------------------

input_path = Path(INPUT_FILE)
if not input_path.exists():
    raise FileNotFoundError(
        f"Cannot find {INPUT_FILE}. Place it in the same folder as this script "
        "or update INPUT_FILE with its full path."
    )

original = pd.read_excel(input_path)
original.columns = [clean_text(c).lower() for c in original.columns]

# Ensure the expected source columns exist.
for col in ["model", "price_inr", "rating"] + SOURCE_SPEC_COLUMNS:
    if col not in original.columns:
        original[col] = None

df = original.copy()

# Clean basic text fields.
for col in ["model"] + SOURCE_SPEC_COLUMNS:
    df[col] = df[col].apply(clean_text)

# Convert price and rating to numeric values.
for col in ["price_inr", "rating"]:
    df[col] = pd.to_numeric(
        df[col].astype(str).str.replace(",", "", regex=False)
        .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False),
        errors="coerce"
    )

# ---------------- REPAIR MISPLACED SPECIFICATION VALUES ----------------

repaired_rows = []

for index, row in df.iterrows():
    # Start with values already present in their expected columns.
    values = {col: clean_text(row.get(col, "")) for col in SOURCE_SPEC_COLUMNS}
    unclassified = []

    # Examine all specification cells and move recognizable values
    # into the correct destination column when that destination is empty.
    for source_col in SOURCE_SPEC_COLUMNS:
        value = values[source_col]
        if not value:
            continue

        detected_column = classify_specification(value)

        if detected_column and detected_column != source_col:
            if not values[detected_column]:
                values[detected_column] = value
                values[source_col] = ""
            else:
                # Preserve a second recognized value rather than overwrite it.
                unclassified.append(value)

        elif detected_column is None:
            unclassified.append(value)

    for col in SOURCE_SPEC_COLUMNS:
        df.at[index, col] = values[col]

    repaired_rows.append("; ".join(dict.fromkeys(unclassified)) or "Not specified")

df["unclassified_spec_text"] = repaired_rows

# ---------------------- DERIVED COLUMNS ----------------------

df["brand"] = df["model"].apply(brand_from_model)

df["has_5g"] = df["sim"].str.contains(r"\b5g\b", case=False, na=False)

df["ram_gb"], df["storage_gb"] = zip(
    *df["ram"].apply(extract_memory_values)
)

df["battery_mah"] = df["battery"].apply(first_number)

display_results = df["display"].apply(extract_display_values)
df["display_inches"] = display_results.apply(lambda x: x[0])
df["resolution_width_px"] = display_results.apply(lambda x: x[1])
df["resolution_height_px"] = display_results.apply(lambda x: x[2])
df["refresh_rate"] = display_results.apply(lambda x: x[3])

df["os_family"] = df["os"].apply(
    lambda x: (
        "Android" if "android" in clean_text(x).lower()
        else "iOS" if "ios" in clean_text(x).lower()
        else "Other" if clean_text(x) else "Not specified"
    )
)

def price_segment(price):
    if pd.isna(price):
        return "Not specified"
    if price <= 10000:
        return "Budget (≤₹10K)"
    if price <= 20000:
        return "Entry (₹10K–₹20K)"
    if price <= 40000:
        return "Mid-range (₹20K–₹40K)"
    if price <= 70000:
        return "Premium (₹40K–₹70K)"
    return "Ultra-premium (>₹70K)"

df["price_segment"] = df["price_inr"].apply(price_segment)

def rating_band(rating):
    if pd.isna(rating):
        return "Not specified"
    if rating < 70:
        return "Below 70"
    if rating < 80:
        return "70–79"
    if rating < 90:
        return "80–89"
    return "90+"

df["rating_band"] = df["rating"].apply(rating_band)

def memory_card_details(value):
    text = clean_text(value)
    low = text.lower()

    if not text:
        return "Not specified", "Not specified"

    if "not supported" in low or "no memory card" in low:
        return "Not supported", "Not specified"

    capacity = re.search(r"(?:upto|up to)\s*(\d+(?:\.\d+)?)\s*(tb|gb)", low)
    max_capacity = "Not specified"
    if capacity:
        amount = float(capacity.group(1))
        unit = capacity.group(2).upper()
        max_capacity = f"{int(amount * 1024) if unit == 'TB' else int(amount)} GB"

    if "hybrid" in low:
        kind = "Hybrid"
    elif "supported" in low or "memory card" in low or "microsd" in low:
        kind = "Supported"
    else:
        kind = "Not specified"

    return kind, max_capacity

card_results = df["card"].apply(memory_card_details)
df["memory_card_type"] = card_results.apply(lambda x: x[0])
df["memory_card_max_capacity"] = card_results.apply(lambda x: x[1])

# Keep the original descriptive fields and derived numeric fields.
df["additional_features"] = "Not specified"
df["additional_spec_notes"] = "Not specified"

# ---------------------- REMOVE INCOMPLETE ROWS ----------------------

# Treat empty strings and common text placeholders as missing for required fields.
cleaned = df.copy()
for col in REQUIRED_FIELDS:
    cleaned[col] = cleaned[col].replace(
        r"^\s*(|nan|none|null|not specified)\s*$",
        pd.NA,
        regex=True
    )

missing_mask = cleaned[REQUIRED_FIELDS].isna().any(axis=1)

removed = cleaned.loc[missing_mask].copy()
removed["removal_reason"] = removed[REQUIRED_FIELDS].apply(
    lambda row: ", ".join(row.index[row.isna()]),
    axis=1
)

cleaned = cleaned.loc[~missing_mask].copy()

# Remove exact duplicate records only.
duplicate_count = int(cleaned.duplicated().sum())
cleaned = cleaned.drop_duplicates().copy()

# Keep a consistent column order.
final_columns = [
    "model", "brand", "price_inr", "rating", "price_segment", "rating_band",
    "sim", "has_5g", "processor", "ram", "ram_gb", "storage_gb",
    "battery", "battery_mah", "display", "display_inches",
    "resolution_width_px", "resolution_height_px", "refresh_rate",
    "camera", "card", "memory_card_type", "memory_card_max_capacity",
    "os", "os_family", "additional_features", "additional_spec_notes",
    "unclassified_spec_text"
]

cleaned = cleaned[final_columns]

# ---------------------- QUALITY REPORT ----------------------

quality_report = pd.DataFrame({
    "Metric": [
        "Original row count",
        "Final cleaned row count",
        "Rows removed for missing required values",
        "Exact duplicate rows removed",
        "Columns in final dataset",
        "Blank cells in final dataset"
    ],
    "Value": [
        len(original),
        len(cleaned),
        len(removed),
        duplicate_count,
        len(cleaned.columns),
        int(cleaned.isna().sum().sum())
    ]
})

# ---------------------- EXPORT RESULTS ----------------------

with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
    cleaned.to_excel(writer, sheet_name="Cleaned Data", index=False)
    quality_report.to_excel(writer, sheet_name="Data Quality Report", index=False)
    removed.to_excel(writer, sheet_name="Removed Rows", index=False)
    original.to_excel(writer, sheet_name="Original Data Backup", index=False)

cleaned.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("DATA CLEANING COMPLETED")
print("----------------------")
print(f"Original rows: {len(original)}")
print(f"Cleaned rows:  {len(cleaned)}")
print(f"Removed rows:  {len(removed)}")
print(f"Duplicate rows removed: {duplicate_count}")
print(f"Blank cells remaining: {int(cleaned.isna().sum().sum())}")
print(f"\nExcel saved as: {OUTPUT_EXCEL}")
print(f"CSV saved as:   {OUTPUT_CSV}")
