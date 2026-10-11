"""
clean_data.py
==============
Data Cleaning & Feature Engineering Pipeline for Books Dataset

This script transforms the raw scraped data from 'data/raw/books_all_pages.csv'
into a cleaned, structured, and feature-engineered dataset saved to
'data/processed/books_cleaned.csv'.

Key Transformations:
1. Title Cleaning & Encoding Repair (fixes smart quotes, accented characters)
2. Price Parsing (extracts numeric float value from currency strings)
3. Rating Mapping (maps string ratings 'One'..'Five' to integers 1..5)
4. Availability Normalization (cleans whitespace and flags stock status)
5. Feature Engineering:
   - title_length (character count)
   - title_word_count (word count)
   - price_tier (Budget, Mid-Range, Premium)
"""

import os
import re
import pandas as pd


def repair_text_encoding(text: str) -> str:
    """
    Repairs common UTF-8 bytes that were misread as Latin-1/CP1252.
    Example: 'Shakespeareâ€™s' -> 'Shakespeare’s'
    """
    if not isinstance(text, str):
        return text
    try:
        # Re-encode as latin1 and decode as utf-8
        return text.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text.strip()


def clean_books_data(raw_csv_path: str, output_csv_path: str) -> pd.DataFrame:
    """
    Reads raw CSV, performs cleaning, feature engineering, and saves cleaned data.
    """
    print(f"[1/5] Loading raw data from: {raw_csv_path}")
    df = pd.read_csv(raw_csv_path)
    initial_rows = len(df)
    print(f"      Loaded {initial_rows} rows and {len(df.columns)} columns.")

    # 1. Clean Title
    print("[2/5] Cleaning and repairing title text...")
    df['title_cleaned'] = df['Title'].apply(repair_text_encoding).str.strip()

    # 2. Extract numeric price (in GBP £)
    print("[3/5] Parsing price into numeric float values...")
    # Extract digits and decimal point: handles '£51.77', 'Â£51.77', etc.
    df['price_gbp'] = (
        df['Price']
        .astype(str)
        .str.extract(r'(\d+\.\d+)')[0]
        .astype(float)
    )

    # 3. Map textual star rating to numeric integer (1 to 5)
    print("[4/5] Mapping star ratings to numeric values (1-5)...")
    rating_map = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    df['rating_numeric'] = df['Rating'].map(rating_map).astype(int)

    # 4. Clean availability
    df['in_stock'] = df['Availability'].str.contains('In stock', case=False, na=False)

    # 5. Feature Engineering
    print("[5/5] Engineering analytical features...")
    df['title_length'] = df['title_cleaned'].str.len()
    df['title_word_count'] = df['title_cleaned'].apply(lambda s: len(s.split()))

    # Categorize price into standard consumer retail tiers
    bins = [0, 20.0, 40.0, float('inf')]
    labels = ['Budget (< £20)', 'Mid-Range (£20 - £40)', 'Premium (> £40)']
    df['price_tier'] = pd.cut(df['price_gbp'], bins=bins, labels=labels, right=False)

    # Reorder columns into a clean, professional schema
    columns_order = [
        'title_cleaned',
        'price_gbp',
        'rating_numeric',
        'Rating',
        'in_stock',
        'title_length',
        'title_word_count',
        'price_tier'
    ]
    df_cleaned = df[columns_order].rename(columns={
        'title_cleaned': 'title',
        'Rating': 'rating_text'
    })

    # Ensure output directory exists and save
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df_cleaned.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"\n[DONE] Cleaned dataset successfully saved to: {output_csv_path}")
    print(f"       Final shape: {df_cleaned.shape}")

    return df_cleaned


if __name__ == '__main__':
    raw_path = os.path.join('data', 'raw', 'books_all_pages.csv')
    # Fallback to current directory if running standalone without data/ folder
    if not os.path.exists(raw_path):
        raw_path = 'books_all_pages.csv'

    processed_path = os.path.join('data', 'processed', 'books_cleaned.csv')
    cleaned_df = clean_books_data(raw_path, processed_path)

    # Display concise summary for validation
    print("\n" + "=" * 50)
    print("Cleaned Dataset Info:")
    print("=" * 50)
    print(cleaned_df.info())
    print("\nSummary Statistics for Numerical Columns:")
    print(cleaned_df.describe())
