"""
analysis.py
===========
Quick Exploratory Data Analysis & Summary Runner

Run this script to quickly view key insights and summary statistics
from the cleaned books dataset.

Usage:
    python analysis.py
"""

import os
import sys
import pandas as pd

# Ensure standard UTF-8 console output for cross-platform compatibility
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Load cleaned data (fallback to cleaning if not generated yet)
cleaned_file = os.path.join("data", "processed", "books_cleaned.csv")

if not os.path.exists(cleaned_file):
    print("Cleaned file not found. Running data cleaning pipeline first...")
    from src.clean_data import clean_books_data
    raw_file = os.path.join("data", "raw", "books_all_pages.csv")
    if not os.path.exists(raw_file):
        raw_file = "books_all_pages.csv"
    df = clean_books_data(raw_file, cleaned_file)
else:
    df = pd.read_csv(cleaned_file)

print("=" * 60)
print("BOOKS DATA ANALYSIS - SUMMARY REPORT")
print("=" * 60)

# 1. Dataset Shape
print("\n1. DATASET OVERVIEW:")
print(f"   * Total Books: {df.shape[0]:,}")
print(f"   * Total Features: {df.shape[1]}")
print(f"   * Columns: {', '.join(df.columns)}")

# 2. Price Statistics
mean_p = df['price_gbp'].mean()
median_p = df['price_gbp'].median()
min_p = df['price_gbp'].min()
max_p = df['price_gbp'].max()

print("\n2. PRICE METRICS (GBP):")
print(f"   * Average Price: GBP {mean_p:.2f}")
print(f"   * Median Price:  GBP {median_p:.2f}")
print(f"   * Price Range:   GBP {min_p:.2f} to GBP {max_p:.2f}")

# 3. Rating Distribution
print("\n3. STAR RATING BREAKDOWN:")
rating_counts = df['rating_numeric'].value_counts().sort_index()
for stars, count in rating_counts.items():
    pct = (count / len(df)) * 100
    stars_str = "*" * stars
    print(f"   * {stars} Stars ({stars_str:<5}): {count} books ({pct:.1f}%)")

# 4. Average Price per Rating Tier
print("\n4. AVERAGE PRICE BY RATING:")
avg_price_by_rating = df.groupby('rating_numeric')['price_gbp'].mean()
for stars, p in avg_price_by_rating.items():
    print(f"   * {stars} Star Average Price: GBP {p:.2f}")

# 5. Price Tiers Breakdown
print("\n5. MARKET SEGMENTATION (PRICE TIERS):")
tier_counts = df['price_tier'].value_counts()
for tier, count in tier_counts.items():
    pct = (count / len(df)) * 100
    print(f"   * {tier:<22}: {count} books ({pct:.1f}%)")

# 6. Top 5 Most Expensive Books
print("\n6. TOP 5 MOST EXPENSIVE BOOKS:")
top_exp = df.sort_values(by='price_gbp', ascending=False).head(5)
for idx, row in top_exp.iterrows():
    print(f"   * GBP {row['price_gbp']:.2f} | {row['rating_numeric']} Stars | {row['title']}")

# 7. Top 5 Most Affordable Books
print("\n7. TOP 5 MOST AFFORDABLE BOOKS:")
top_cheap = df.sort_values(by='price_gbp', ascending=True).head(5)
for idx, row in top_cheap.iterrows():
    print(f"   * GBP {row['price_gbp']:.2f} | {row['rating_numeric']} Stars | {row['title']}")

print("\n" + "=" * 60)
print("Analysis complete! Open notebooks/exploratory_data_analysis.ipynb")
print("or check the 'figures/' folder to view charts.")
print("=" * 60)