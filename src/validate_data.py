"""
validate_data.py
=================
Automated Data Quality & Schema Validation Suite for Books Dataset

Validates data integrity, completeness, and consistency across both
raw and processed datasets.

Checks Performed:
1. File Existence & Row/Column Dimensions (1,000 records)
2. Missing Value (Null) Audit
3. Exact Row Duplicates & Title-Level Duplicate Audit
4. Price Range & Data Type Sanity Checks
5. Star Rating Mapping & Ordinal Consistency (1 to 5)
6. MECE Segmentation Validation (Price Tiers)
"""

import os
import sys
import pandas as pd

# Reconfigure stdout for utf-8 on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


def run_validation():
    print("=" * 65)
    print("RUNNING DATA QUALITY & INTEGRITY VALIDATION SUITE")
    print("=" * 65)

    raw_path = os.path.join("data", "raw", "books_all_pages.csv")
    if not os.path.exists(raw_path):
        raw_path = "books_all_pages.csv"

    proc_path = os.path.join("data", "processed", "books_cleaned.csv")

    passed_checks = 0
    total_checks = 7

    # ---------------------------------------------------------
    # Check 1: File Existence & Dimensions
    # ---------------------------------------------------------
    print("\n[Check 1/7] Verifying file existence and record counts...")
    assert os.path.exists(raw_path), f"Raw dataset not found at {raw_path}"
    assert os.path.exists(proc_path), f"Processed dataset not found at {proc_path}"

    df_raw = pd.read_csv(raw_path)
    df_proc = pd.read_csv(proc_path)

    assert df_raw.shape == (1000, 4), f"Unexpected raw shape: {df_raw.shape}"
    assert df_proc.shape == (1000, 8), f"Unexpected processed shape: {df_proc.shape}"
    print(f"  --> PASS: Raw is (1000, 4) and Processed is (1000, 8).")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 2: Missing Values (Null) Audit
    # ---------------------------------------------------------
    print("\n[Check 2/7] Auditing missing values (null/NaN)...")
    raw_nulls = df_raw.isnull().sum().sum()
    proc_nulls = df_proc.isnull().sum().sum()
    assert raw_nulls == 0, f"Raw data has {raw_nulls} null values!"
    assert proc_nulls == 0, f"Processed data has {proc_nulls} null values!"
    print(f"  --> PASS: Zero nulls found across both raw and processed datasets.")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 3: Duplication Analysis
    # ---------------------------------------------------------
    print("\n[Check 3/7] Auditing row duplicates and duplicate titles...")
    raw_exact_dups = df_raw.duplicated().sum()
    proc_exact_dups = df_proc.duplicated().sum()
    assert raw_exact_dups == 0, f"Found {raw_exact_dups} exact duplicate rows in raw data!"
    assert proc_exact_dups == 0, f"Found {proc_exact_dups} exact duplicate rows in processed data!"

    # Title-level check (verify the known 1 duplicate title has different prices)
    title_dups = df_proc[df_proc['title'].duplicated(keep=False)]
    dup_titles = title_dups['title'].unique().tolist()
    assert len(dup_titles) == 1, f"Expected 1 duplicate title, found {len(dup_titles)}"
    assert dup_titles[0] == "The Star-Touched Queen", f"Unexpected duplicate title: {dup_titles}"

    prices_for_dup = title_dups['price_gbp'].tolist()
    assert len(set(prices_for_dup)) == 2, f"Duplicate titles share identical prices: {prices_for_dup}"
    print(f"  --> PASS: 0 exact duplicate rows. 1 legitimate multi-edition title documented: {dup_titles[0]} (Prices: £{prices_for_dup[0]:.2f}, £{prices_for_dup[1]:.2f}).")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 4: Price Conversion & Bounds
    # ---------------------------------------------------------
    print("\n[Check 4/7] Validating price conversion and mathematical bounds...")
    assert pd.api.types.is_float_dtype(df_proc['price_gbp']), "price_gbp is not float64!"
    min_p = df_proc['price_gbp'].min()
    max_p = df_proc['price_gbp'].max()
    mean_p = df_proc['price_gbp'].mean()

    assert min_p == 10.00, f"Expected min price 10.00, got {min_p}"
    assert max_p == 59.99, f"Expected max price 59.99, got {max_p}"
    assert 35.0 <= mean_p <= 35.2, f"Expected mean price around 35.07, got {mean_p}"
    print(f"  --> PASS: Price is float64, bounded strictly between £{min_p:.2f} and £{max_p:.2f} (Mean: £{mean_p:.2f}).")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 5: Star Rating Normalization
    # ---------------------------------------------------------
    print("\n[Check 5/7] Validating star rating mapping and ordinal consistency...")
    unique_ratings = sorted(df_proc['rating_numeric'].unique().tolist())
    assert unique_ratings == [1, 2, 3, 4, 5], f"Unexpected ratings: {unique_ratings}"

    # Verify 1-to-1 mapping with text ratings
    for num, txt in [(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')]:
        subset = df_proc[df_proc['rating_numeric'] == num]
        assert (subset['rating_text'] == txt).all(), f"Mismatch between rating {num} and text {txt}"
    print(f"  --> PASS: Star ratings map 1-to-1 with text ordinals across all 1,000 records.")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 6: MECE Price Tier Segmentation
    # ---------------------------------------------------------
    print("\n[Check 6/7] Validating price tier segmentation (MECE partitions)...")
    expected_tiers = {'Budget (< £20)': 196, 'Mid-Range (£20 - £40)': 401, 'Premium (> £40)': 403}
    actual_tiers = df_proc['price_tier'].value_counts().to_dict()

    assert actual_tiers == expected_tiers, f"Tier mismatch! Expected {expected_tiers}, got {actual_tiers}"
    assert sum(actual_tiers.values()) == 1000, "Tiers do not sum to 1,000!"
    print(f"  --> PASS: Price tiers are Mutually Exclusive & Collectively Exhaustive (Budget: 196, Mid-Range: 401, Premium: 403).")
    passed_checks += 1

    # ---------------------------------------------------------
    # Check 7: Feature Engineering Sanity
    # ---------------------------------------------------------
    print("\n[Check 7/7] Validating engineered features (title length & word count)...")
    assert (df_proc['title_length'] > 0).all(), "Found empty titles!"
    assert (df_proc['title_word_count'] > 0).all(), "Found titles with zero word count!"
    assert df_proc['in_stock'].all(), "Found books flagged as out of stock!"
    print(f"  --> PASS: Feature engineering checks validated. 100% of books are in stock.")
    passed_checks += 1

    print("\n" + "=" * 65)
    print(f"ALL {passed_checks}/{total_checks} DATA QUALITY CHECKS PASSED SUCCESSFULLY!")
    print("=" * 65)
    return True


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
