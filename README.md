# 📚 Books Data Analysis & Exploratory Insights

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-3.0%2B-150458.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557c.svg)](https://matplotlib.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end **Exploratory Data Analysis (EDA)** and data cleaning project analyzing **1,000 book records** systematically extracted from [Books to Scrape](https://books.toscrape.com/) via the companion web scraping pipeline [`books-web-scraping`](https://github.com/ranjithbrs/books-web-scraping).

This project cleans messy web-scraped data, engineers analytical attributes, uncovers pricing patterns, tests price-to-rating correlations, and presents publication-grade visual insights.

---

## 📑 Table of Contents
- [Project Architecture](#-project-architecture)
- [Key Analytical Findings](#-key-analytical-findings)
- [Visual Insights](#-visual-insights)
- [Data Pipeline & Schema](#-data-pipeline--schema)
- [Repository Structure](#-repository-structure)
- [Quickstart: How to Run Locally](#-quickstart-how-to-run-locally)
- [Key Engineering & Analytical Takeaways](#-key-engineering--analytical-takeaways)
- [Author & Connect](#-author--connect)
- [License](#-license)

---

## 📐 Project Architecture

```
Raw Web Data (1,000 Rows x 4 Cols)
   [books_all_pages.csv]
           │
           ▼
 Data Cleaning Pipeline (src/clean_data.py)
   ├── 1. Title Encoding Repair (UTF-8 / Latin-1 Mojibake fix)
   ├── 2. Regex Numeric Price Extraction (£51.77 -> 51.77 float)
   ├── 3. Ordinal Rating Mapping ("One".."Five" -> 1..5 int)
   └── 4. Feature Engineering (Price Tiers, Title Length & Words)
           │
           ▼
 Cleaned Analytical Dataset (data/processed/books_cleaned.csv)
           │
     ┌─────┴────────────────────────┐
     ▼                              ▼
Jupyter EDA Notebook         Publication Figures
(notebooks/exploratory_      (figures/*.png & src/generate_charts.py)
 data_analysis.ipynb)
```

---

## 💡 Key Analytical Findings

| Metric / Question | Finding | Analytical Takeaway |
| :--- | :--- | :--- |
| **Catalog Price Range** | **£10.00 – £59.99** | Continuous uniform price distribution with no outliers. |
| **Average & Median Price** | **Mean: £35.07** \| **Median: £35.98** | Highly symmetrical distribution (Mean $\approx$ Median). |
| **Price vs. Rating Correlation** | **Pearson $r = 0.028$ (Near Zero)** | **Disproved assumption:** Higher customer ratings do NOT correlate with higher retail prices. |
| **Market Segment Breakdown** | Premium: **40.3%** \| Mid-Range: **40.1%** \| Budget: **19.6%** | Over 80% of books fall between £20 and £60. |
| **Rating Balance** | 1★ (22.6%), 2★ (19.6%), 3★ (20.3%), 4★ (17.9%), 5★ (19.6%) | Uniform rating distribution across all 5 tiers. |
| **Most Expensive Title** | *The Perfect Play (Play by Play #1)* — **£59.99** (Rated 3★) | Premium-priced fiction. |
| **Most Affordable Title** | *An Abundance of Katherines* — **£10.00** (Rated 5★) | Top-rated book available at lowest price point. |

---

## 📊 Visual Insights

### 1. Catalog Price Distribution
Prices span smoothly between £10 and £60 with an average price of **£35.07**.
![Price Distribution](figures/01_price_distribution.png)

### 2. Rating Breakdown Across Tiers
The catalog displays a balanced rating distribution across all five tiers (~18% to 23% per tier).
![Rating Distribution](figures/02_rating_distribution.png)

### 3. Price Spread Grouped by Star Rating (Box Plot)
Box-and-whisker distributions demonstrate that quartile spreads and median prices are virtually identical across all star levels ($r = 0.028$).
![Price by Rating Boxplot](figures/03_price_by_rating_boxplot.png)

### 4. Consumer Retail Price Tiers
Segmented into Budget (< £20), Mid-Range (£20 - £40), and Premium (> £40).
![Price Tiers Breakdown](figures/04_price_tiers_breakdown.png)

### 5. Top 5 Most Expensive vs. Top 5 Most Affordable Books
A side-by-side comparison of the catalog extremes.
![Top Expensive vs Affordable](figures/05_top_cheapest_and_expensive.png)

---

## 🗃️ Data Pipeline & Schema

### Cleaned Dataset Schema (`data/processed/books_cleaned.csv`)

| Column Name | Data Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `title` | `string` | Full book title with repaired encoding | *A Light in the Attic* |
| `price_gbp` | `float64` | Numeric book price in British Pounds (£) | `51.77` |
| `rating_numeric` | `int64` | Ordinal star rating (1 to 5) | `3` |
| `rating_text` | `string` | Original textual rating | `Three` |
| `in_stock` | `bool` | In-stock inventory indicator | `True` |
| `title_length` | `int64` | Character count of the cleaned title | `20` |
| `title_word_count` | `int64` | Word count of the title | `5` |
| `price_tier` | `category` | Retail tier (`Budget`, `Mid-Range`, `Premium`) | `Premium (> £40)` |

---

## 📁 Repository Structure

```text
books-data-analysis/
├── data/
│   ├── raw/
│   │   └── books_all_pages.csv           # Original 1,000-row scraped dataset
│   └── processed/
│       └── books_cleaned.csv             # Cleaned analytical dataset (1,000 x 8)
├── figures/                              # High-resolution exported figures (300 DPI)
│   ├── 01_price_distribution.png
│   ├── 02_rating_distribution.png
│   ├── 03_price_by_rating_boxplot.png
│   ├── 04_price_tiers_breakdown.png
│   └── 05_top_cheapest_and_expensive.png
├── notebooks/
│   └── exploratory_data_analysis.ipynb    # Comprehensive Jupyter Notebook with full EDA
├── src/
│   ├── clean_data.py                     # Automated cleaning & feature engineering pipeline
│   └── generate_charts.py                # Visual figure generation script
├── analysis.py                           # Quick terminal summary statistics runner
├── requirements.txt                      # Project Python dependencies
├── .gitignore                            # Environment & cache ignore rules
├── LICENSE                               # MIT License
└── README.md                             # Project documentation & visual report
```

---

## 🚀 Quickstart: How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/ranjithbrs/books-data-analysis.git
cd books-data-analysis
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate       # On macOS/Linux
.venv\Scripts\activate          # On Windows

# Install required packages
pip install -r requirements.txt
```

### 3. Run the Data Pipeline
```bash
# Step 1: Clean raw data and engineer features
python src/clean_data.py

# Step 2: Generate all visual figures
python src/generate_charts.py

# Step 3: Run quick terminal summary
python analysis.py
```

### 4. Explore the Interactive Notebook
```bash
jupyter notebook notebooks/exploratory_data_analysis.ipynb
```

---

## 💡 Key Engineering & Analytical Takeaways

1. **Defensive Encoding Normalization**: Web-scraped content frequently mixes byte interpretations (e.g. UTF-8 multi-byte characters like smart quotes `’` misread as Windows-1252 `â€™`). Handled gracefully through bidirectional byte decoding (`latin1` $\rightarrow$ `utf-8`).
2. **Robust Currency Parsing**: Extracted clean floating-point numbers via regular expressions (`r'(\d+\.\d+)'`), insulating the pipeline from currency symbol rendering quirks.
3. **Statistical Independence Verification**: Confirmed that customer ratings and prices operate independently ($r = 0.028$), an essential finding when building downstream recommendation models or market analyses.
4. **Reproducible Pipeline**: Structured raw versus processed data directories according to industry standard data engineering workflows.

---

## 👨‍💻 Author

**Ranjith B**  
🎓 B.Tech Computer Science & Business Systems (CSBS)  
🏛️ Nehru Institute of Engineering and Technology, Coimbatore  

- 💼 **LinkedIn:** [linkedin.com/in/ranjith-b-csbs](https://linkedin.com/in/ranjith-b-csbs)  
- 🐙 **GitHub:** [github.com/ranjithbrs](https://github.com/ranjithbrs)  
- 🌐 **Portfolio:** [ranjithbrs.github.io/portfolio](https://ranjithbrs.github.io/portfolio/)  
- 📧 **Email:** [ranjithb2k06@gmail.com](mailto:ranjithb2k06@gmail.com)  

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
