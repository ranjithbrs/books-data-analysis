"""
generate_charts.py
===================
Visualizations Generator for Books Data Analysis

Generates high-resolution, presentation-ready visualizations from the
cleaned dataset and saves them into the 'figures/' directory.

Visualizations:
1. 01_price_distribution.png: Histogram & KDE of book prices
2. 02_rating_distribution.png: Star ratings count & percentage breakdown
3. 03_price_by_rating_boxplot.png: Price distribution across rating tiers
4. 04_price_tiers_breakdown.png: Market segment breakdown (Budget, Mid, Premium)
5. 05_top_cheapest_and_expensive.png: Top 5 most expensive vs least expensive books
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set professional visualization style
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 14,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 16,
})

FIGURES_DIR = "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)


def load_data(csv_path="data/processed/books_cleaned.csv") -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cleaned dataset not found at {csv_path}. Please run clean_data.py first.")
    return pd.read_csv(csv_path)


def plot_price_distribution(df: pd.DataFrame):
    """Figure 1: Price Distribution with Mean and Median markers."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    mean_price = df["price_gbp"].mean()
    median_price = df["price_gbp"].median()

    sns.histplot(
        df["price_gbp"],
        kde=True,
        bins=25,
        color="#2b5c8f",
        edgecolor="white",
        linewidth=1.2,
        ax=ax,
    )

    # Add vertical lines for mean and median
    ax.axvline(
        mean_price,
        color="#d9534f",
        linestyle="--",
        linewidth=2,
        label=f"Mean: £{mean_price:.2f}",
    )
    ax.axvline(
        median_price,
        color="#5cb85c",
        linestyle="-.",
        linewidth=2,
        label=f"Median: £{median_price:.2f}",
    )

    ax.set_title("Distribution of Book Prices (£ GBP)", pad=15, weight="bold")
    ax.set_xlabel("Price (£)")
    ax.set_ylabel("Number of Books")
    ax.legend(frameon=True, facecolor="white", loc="upper right")

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "01_price_distribution.png")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[+] Saved: {output_path}")


def plot_rating_distribution(df: pd.DataFrame):
    """Figure 2: Star Rating Counts and Percentages."""
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    counts = df["rating_numeric"].value_counts().sort_index()
    palette = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#1abc9c"]

    bars = ax.bar(counts.index, counts.values, color=palette, edgecolor="#333333", linewidth=0.8, width=0.6)

    # Add count and percentage labels above each bar
    total_books = len(df)
    for bar in bars:
        height = bar.get_height()
        pct = (height / total_books) * 100
        ax.annotate(
            f"{height}\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
            weight="bold",
        )

    ax.set_title("Catalog Distribution Across Star Ratings (1 to 5)", pad=15, weight="bold")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Book Count")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xticklabels(["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
    ax.set_ylim(0, max(counts.values) * 1.18)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "02_rating_distribution.png")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[+] Saved: {output_path}")


def plot_price_by_rating(df: pd.DataFrame):
    """Figure 3: Price Box Plot grouped by Star Rating."""
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    palette = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#1abc9c"]
    sns.boxplot(
        x="rating_numeric",
        y="price_gbp",
        hue="rating_numeric",
        data=df,
        palette=palette,
        ax=ax,
        fliersize=4,
        linewidth=1.3,
        width=0.55,
        legend=False,
    )

    # Overlay mean points
    means = df.groupby("rating_numeric")["price_gbp"].mean()
    ax.plot(
        range(len(means)),
        means.values,
        color="#2c3e50",
        marker="D",
        markersize=7,
        linestyle="--",
        linewidth=1.5,
        label="Group Mean Price",
    )

    ax.set_title("Book Price Spread Across Rating Levels", pad=15, weight="bold")
    ax.set_xlabel("Star Rating")
    ax.set_ylabel("Price (£ GBP)")
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
    ax.legend(loc="lower right", frameon=True)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "03_price_by_rating_boxplot.png")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[+] Saved: {output_path}")


def plot_price_tiers(df: pd.DataFrame):
    """Figure 4: Consumer Retail Price Tiers Breakdown (Donut Chart)."""
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)

    tier_counts = df["price_tier"].value_counts()[
        ["Budget (< £20)", "Mid-Range (£20 - £40)", "Premium (> £40)"]
    ]
    colors = ["#3498db", "#f39c12", "#9b59b6"]

    wedges, texts, autotexts = ax.pie(
        tier_counts.values,
        labels=tier_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        pctdistance=0.75,
    )

    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_weight("bold")
        autotext.set_color("white")

    ax.set_title("Book Inventory by Price Tier", pad=20, weight="bold")

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "04_price_tiers_breakdown.png")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[+] Saved: {output_path}")


def plot_top_books(df: pd.DataFrame):
    """Figure 5: Top 5 Most Expensive vs Top 5 Least Expensive Books."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=300)

    # Top 5 most expensive
    top_expensive = df.sort_values(by="price_gbp", ascending=False).head(5).copy()
    top_expensive["short_title"] = top_expensive["title"].apply(
        lambda t: t[:28] + "..." if len(t) > 28 else t
    )

    # Top 5 cheapest
    top_cheapest = df.sort_values(by="price_gbp", ascending=True).head(5).copy()
    top_cheapest["short_title"] = top_cheapest["title"].apply(
        lambda t: t[:28] + "..." if len(t) > 28 else t
    )

    # Plot Most Expensive
    bars1 = ax1.barh(
        top_expensive["short_title"][::-1],
        top_expensive["price_gbp"][::-1],
        color="#c0392b",
        edgecolor="#333333",
    )
    for bar in bars1:
        w = bar.get_width()
        ax1.text(w - 6, bar.get_y() + 0.25, f"£{w:.2f}", color="white", weight="bold")
    ax1.set_title("Top 5 Most Expensive Books", weight="bold")
    ax1.set_xlabel("Price (£)")
    ax1.set_xlim(0, 65)

    # Plot Cheapest
    bars2 = ax2.barh(
        top_cheapest["short_title"][::-1],
        top_cheapest["price_gbp"][::-1],
        color="#27ae60",
        edgecolor="#333333",
    )
    for bar in bars2:
        w = bar.get_width()
        ax2.text(w + 0.5, bar.get_y() + 0.25, f"£{w:.2f}", color="#27ae60", weight="bold")
    ax2.set_title("Top 5 Most Affordable Books", weight="bold")
    ax2.set_xlabel("Price (£)")
    ax2.set_xlim(0, 20)

    plt.tight_layout()
    output_path = os.path.join(FIGURES_DIR, "05_top_cheapest_and_expensive.png")
    fig.savefig(output_path)
    plt.close(fig)
    print(f"[+] Saved: {output_path}")


def main():
    print("Generating analysis figures...")
    df = load_data()
    plot_price_distribution(df)
    plot_rating_distribution(df)
    plot_price_by_rating(df)
    plot_price_tiers(df)
    plot_top_books(df)
    print("\nAll figures generated successfully in 'figures/'!")


if __name__ == "__main__":
    main()
