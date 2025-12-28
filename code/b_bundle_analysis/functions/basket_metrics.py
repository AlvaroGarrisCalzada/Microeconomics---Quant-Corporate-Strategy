from __future__ import annotations

from typing import Iterable, Tuple

import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def summarize_basket_sizes(
    df: pd.DataFrame, level: str = "PRODUCT_ID"
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Return the number of unique items per basket and descriptive stats.
    """

    basket_counts = (
        df.groupby("BASKET_ID")[level].nunique().rename("unique_items").reset_index()
    )
    summary = basket_counts["unique_items"].describe(
        percentiles=[0.5, 0.75, 0.9, 0.95]
    )
    return basket_counts, summary


def compute_category_support(
    df: pd.DataFrame,
    level: str = "COMMODITY_DESC",
    top_n: int = 15,
) -> pd.DataFrame:
    """
    Calculate the share of baskets that contain each category.
    """

    total_baskets = df["BASKET_ID"].nunique()
    basket_item = (
        df.dropna(subset=[level])
        .groupby(["BASKET_ID", level])
        .size()
        .reset_index(name="line_items")
    )
    support = (
        basket_item.groupby(level)["BASKET_ID"].nunique().sort_values(ascending=False)
        / total_baskets
    )
    support = support.reset_index(name="support")
    support["support_pct"] = support["support"] * 100
    return support.head(top_n)


def prepare_basket_matrix(
    df: pd.DataFrame,
    level: str = "COMMODITY_DESC",
    min_item_support: float = 0.01,
    top_n: int | None = 30,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Transform the transaction dataset into a transaction-item matrix.
    """

    total_baskets = df["BASKET_ID"].nunique()
    basket_item = (
        df.dropna(subset=[level])
        .groupby(["BASKET_ID", level])
        .size()
        .reset_index(name="line_items")
    )
    support = (
        basket_item.groupby(level)["BASKET_ID"].nunique().sort_values(ascending=False)
        / total_baskets
    )
    support = support.loc[support >= min_item_support]
    if top_n is not None:
        support = support.head(top_n)
    if support.empty:
        return pd.DataFrame(), pd.DataFrame()

    items_to_keep = support.index.tolist()
    matrix = (
        basket_item[basket_item[level].isin(items_to_keep)]
        .assign(present=1)
        .pivot_table(
            index="BASKET_ID",
            columns=level,
            values="present",
            aggfunc="max",
            fill_value=0,
        )
    )
    basket_ids = df["BASKET_ID"].drop_duplicates()
    matrix = matrix.reindex(basket_ids, fill_value=0).astype(np.uint8)

    support = support.reset_index(name="support")
    support["support_pct"] = support["support"] * 100
    return matrix, support


def _format_itemset(itemset: Iterable[str]) -> str:
    return ", ".join(sorted(itemset))


def generate_rules(
    matrix: pd.DataFrame,
    min_support: float = 0.005,
    min_confidence: float = 0.15,
    min_lift: float = 1.05,
    max_len: int = 3,
    bundle_size: int | None = None,
) -> pd.DataFrame:
    """
    Run Apriori and derive association rules that pass the chosen thresholds.
    """

    if matrix.empty:
        return pd.DataFrame()

    frequent_sets = apriori(
        matrix.astype(bool),
        min_support=min_support,
        use_colnames=True,
        max_len=bundle_size or max_len,
    )
    if frequent_sets.empty:
        return pd.DataFrame()

    rules = association_rules(
        frequent_sets, metric="confidence", min_threshold=min_confidence
    )
    rules = rules.loc[rules["lift"] >= min_lift].copy()
    if rules.empty:
        return rules

    total_baskets = len(matrix)
    rules["antecedent_str"] = rules["antecedents"].apply(_format_itemset)
    rules["consequent_str"] = rules["consequents"].apply(_format_itemset)
    rules["rule_text"] = rules["antecedent_str"] + " \u2192 " + rules["consequent_str"]
    rules["support_pct"] = (rules["support"] * 100).round(2)
    rules["confidence_pct"] = (rules["confidence"] * 100).round(2)
    rules["coverage_baskets"] = (rules["support"] * total_baskets).round(0).astype(int)
    rules["lift"] = rules["lift"].round(2)
    rules = rules.sort_values(["lift", "confidence"], ascending=False)
    return rules


def describe_rule_clusters(rules: pd.DataFrame, top_k: int = 10) -> pd.DataFrame:
    """
    Provide a tidy view of the strongest rules for storytelling tables.
    """

    if rules.empty:
        return pd.DataFrame()

    cols = [
        "rule_text",
        "support_pct",
        "confidence_pct",
        "lift",
        "coverage_baskets",
    ]
    table = rules[cols].head(top_k).copy()
    table.columns = [
        "Rule",
        "Support (%)",
        "Confidence (%)",
        "Lift",
        "Baskets Covered",
    ]
    return table


def top_rules_by_consequent(rules: pd.DataFrame, top_k: int = 10) -> pd.DataFrame:
    """
    Return the strongest rule per consequent to avoid repetition and surface
    diverse bundle ideas.
    """

    if rules.empty:
        return pd.DataFrame()

    subset = (
        rules.sort_values(["lift", "support"], ascending=False)
        .groupby("consequent_str", as_index=False)
        .head(1)
        .sort_values("support_pct", ascending=False)
        .head(top_k)
    )
    cols = [
        "rule_text",
        "support_pct",
        "confidence_pct",
        "lift",
        "coverage_baskets",
    ]
    subset = subset[cols].copy()
    subset.columns = [
        "Rule",
        "Support (%)",
        "Confidence (%)",
        "Lift",
        "Baskets Covered",
    ]
    return subset
