from __future__ import annotations

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def _save_if_needed(fig: plt.Figure, output_path: Optional[str]) -> None:
    if output_path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, bbox_inches="tight", dpi=150)


def plot_basket_size_distribution(
    basket_counts: pd.DataFrame,
    output_path: Optional[str] = None,
) -> plt.Axes:
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(basket_counts["unique_items"], bins=range(1, 20), color="#4472C4", edgecolor="white")
    ax.set_xlabel("Unique items per basket")
    ax.set_ylabel("Number of baskets")
    ax.set_title("Basket size distribution (by unique products)")
    _save_if_needed(fig, output_path)
    return ax


def plot_category_support(
    support_df: pd.DataFrame,
    value_col: str = "support_pct",
    label_col: str = "COMMODITY_DESC",
    output_path: Optional[str] = None,
) -> plt.Axes:
    fig, ax = plt.subplots(figsize=(8, 6))
    data = support_df.sort_values(value_col)
    ax.barh(data[label_col], data[value_col], color="#70AD47")
    ax.set_xlabel("Share of baskets (%)")
    ax.set_ylabel(label_col.replace("_", " ").title())
    ax.set_title("Top categories by basket penetration")
    for i, val in enumerate(data[value_col]):
        ax.text(val + 0.1, i, f"{val:.1f}%", va="center", fontsize=8)
    _save_if_needed(fig, output_path)
    return ax


def plot_rule_network(
    rules: pd.DataFrame,
    output_path: Optional[str] = None,
    top_k: int = 15,
    label_col: str = "rule_text",
) -> plt.Axes:
    fig, ax = plt.subplots(figsize=(8, 6))
    top_rules = rules.head(top_k).copy()
    scatter = ax.scatter(
        top_rules["support_pct"],
        top_rules["confidence_pct"],
        s=top_rules["lift"] * 30,
        c=top_rules["lift"],
        cmap="viridis",
        alpha=0.8,
    )
    ax.set_xlabel("Support (%)")
    ax.set_ylabel("Confidence (%)")
    ax.set_title("Rule landscape (circle size = lift)")
    for _, row in top_rules.iterrows():
        ax.text(
            row["support_pct"] + 0.1,
            row["confidence_pct"],
            row.get(label_col, row["rule_text"]),
            fontsize=7,
            alpha=0.7,
        )
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Lift")
    _save_if_needed(fig, output_path)
    return ax
