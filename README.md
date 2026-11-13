# 📱 SpecScout – Mobile Specification Tracker

**A data-driven smartphone specification analysis and comparison project using Python and Power BI.**

## 📌 Project Overview

SpecScout is a data analytics and visualization project designed to help users explore, analyse, and compare smartphones based on their specifications, prices, ratings, and brands.

The project transforms raw smartphone data into a structured dataset using Python and presents meaningful insights through interactive Power BI dashboards and graphical visualizations.

The main objective is to make smartphone comparison easier and help users make informed purchasing decisions based on their requirements and budget.

## 🎯 Problem Statement

Choosing a smartphone can be difficult because of the large number of available models, brands, specifications, and price ranges.

Users often need to compare multiple factors, such as RAM, storage, battery capacity, display, ratings, and price.

SpecScout addresses this problem by organising smartphone information and presenting it through data analysis, visualizations, and interactive dashboard filters.

## ✨ Key Features

- Smartphone specification analysis.
- Brand-wise smartphone distribution.
- Average price comparison across brands.
- Smartphone price segment analysis.
- Rating distribution and comparison.
- RAM and storage capacity analysis.
- Battery capacity comparison.
- 5G availability analysis.
- Operating system distribution.
- Interactive Power BI dashboard with filtering options.
- Python-based data cleaning and visualization.

## 📊 Dataset Information

| Description | Details |
|---|---|
| Dataset source | Kaggle |
| Original records | 1,074 |
| Cleaned records | 789 |
| Unique brands | 42 |
| Cleaned columns | 25 |
| Dataset format | CSV |

### Important Dataset Attributes

- Brand and Model
- Price (INR)
- Rating
- RAM (GB)
- Storage (GB)
- Battery Capacity (mAh)
- Display Size
- Camera Specifications
- Processor
- 5G Availability
- Operating System

## 🛠️ Technologies Used

| Technology / Library | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data cleaning, manipulation and analysis |
| NumPy | Numerical computing where applicable |
| Regular Expressions (`re`) | Extracting smartphone specifications from text |
| Matplotlib | Creating graphical visualizations |
| OpenPyXL | Reading and writing Excel workbooks |
| Power BI | Interactive dashboard and data visualization |
| CSV / Excel | Dataset storage and processing |

## 📂 Project Structure

```text
SpecScout/
│
├── SpecScout Project Proposal.pdf
│
├── SpecScout-Dataset-Collection.xlsx
│
├── SpecScout_Dataset_Fully_Cleaned.csv
│
├── SpecScout PBI Dashboard.pbix
│
├── data_cleaning.py.py
│
├── data_analytics.py.py
│
├── data_visualization.py.py
│
└── README.md
```

## 🧹 Data Cleaning

The raw smartphone dataset was processed using Python and Pandas.

Major cleaning operations include:

1. Reading the original Excel dataset.
2. Standardising column names and text values.
3. Cleaning price and rating values.
4. Identifying misplaced smartphone specifications.
5. Extracting RAM and storage values using regular expressions.
6. Extracting battery capacity and display information.
7. Identifying smartphone brands from model names.
8. Creating additional analytical columns, such as price segments and rating bands.
9. Identifying and removing rows with missing required information.
10. Removing duplicate records.
11. Exporting the cleaned dataset into CSV and Excel formats.

## 📈 Data Analysis

The Python analytics script performs 10 different analyses:

1. Smartphone Count by Brand
2. Average Price by Brand
3. Price Segment Distribution
4. Rating Band Distribution
5. 5G Availability
6. Rating Statistics by Brand
7. RAM Capacity Distribution
8. Storage Capacity Distribution
9. Average Battery Capacity by Brand
10. Operating System Distribution

The analysis results are displayed in the terminal and saved as CSV files.

## 📊 Data Visualization

The project uses Matplotlib to generate 10 graphical visualizations from the cleaned smartphone dataset.

These visualizations help identify patterns, distributions, comparisons, and relationships within the smartphone data.

The generated graph images are saved in the `SpecScout_Visualizations` folder.

## 📉 Power BI Dashboard

The Power BI dashboard provides an interactive way to explore the cleaned smartphone dataset.

**Dashboard capabilities include:**

- Brand-based filtering.
- Smartphone price comparisons.
- Specification-based exploration.
- Rating analysis.
- RAM and storage comparisons.
- 5G availability insights.
- Visual representation of smartphone market segments.

The `.pbix` file is included in this repository and can be opened using Microsoft Power BI Desktop.

## 🚀 Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/SpecScout.git
```

### 2. Navigate to the Project Folder

```bash
cd SpecScout
```

### 3. Install Required Libraries

```bash
pip install pandas matplotlib openpyxl
```

### 4. Run Data Cleaning

```bash
python data_cleaning.py.py
```

**Note:** The cleaning script currently expects an input Excel file named `SpecScout-Dataset-Cleaned-Updated.xlsx`. Update the `INPUT_FILE` variable in the script to match the Excel filename in this repository before running it.

### 5. Run Data Analysis

```bash
python data_analytics.py.py
```

Analysis results will be generated in:

```text
SpecScout_Analysis_CSV/
```

### 6. Run Data Visualization

```bash
python data_visualization.py.py
```

Generated graph images will be saved in:

```text
SpecScout_Visualizations/
```

### 7. Open the Power BI Dashboard

Open `SpecScout PBI Dashboard.pbix` using Microsoft Power BI Desktop.

## 🔍 Key Project Insights

Some of the key findings from the cleaned dataset and dashboard include:

- Samsung has the highest number of smartphone models in the dataset.
- The ₹10,000–₹20,000 price segment has the largest representation.
- The 80–89 rating band is the most common.
- 128 GB is the most common storage capacity.
- 8 GB RAM is among the most common RAM configurations.
- Approximately 48.2% of the records indicate 5G availability.

## ⚠️ Project Limitations

- The dataset represents a snapshot and does not provide live smartphone market prices.
- The dataset does not contain dated historical price records.
- Some original specification fields contain incomplete or inconsistent information.
- Observed relationships between specifications and ratings do not necessarily establish causation.

## 🔮 Future Enhancements

- Integration of regularly updated smartphone prices.
- Historical price tracking and price-drop alerts.
- Advanced processor and camera comparisons.
- Smartphone recommendation functionality.
- Improved model-to-model comparison features.
- Additional interactive dashboard capabilities.

## 🏁 Conclusion

SpecScout demonstrates how Python-based data cleaning and analysis can transform raw smartphone information into meaningful insights.

By combining Python, Pandas, Matplotlib, and Power BI, the project provides a structured way to explore smartphone specifications, understand price segments, compare brands, and analyse smartphone trends.

The project aims to make smartphone research simpler through data-driven analysis and interactive visualizations.

---

**Developed by:**  
B. Sathwik | T. HariswaraBrahmam | A. Saiteja

**Project:** SpecScout – Mobile Specification Tracker  
**Institution:** SR University
