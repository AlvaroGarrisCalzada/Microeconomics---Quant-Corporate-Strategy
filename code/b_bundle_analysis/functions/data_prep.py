from __future__ import annotations

from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd


PathLike = Union[str, Path]
BASE_DATE = pd.Timestamp("2017-01-01")


def _ensure_path(path: PathLike) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

#test
def build_and_save_basket_dataset(
    raw_data_dir: PathLike,
    output_path: PathLike,
    min_net_spend: float = 0.01,
    drop_returns: bool = True,
) -> pd.DataFrame:
    """
    Create a tidy basket-level dataset that links transactions with product meta data.

    Parameters
    ----------
    raw_data_dir
        Directory that stores the raw CSV extracts delivered with the course.
    output_path
        File (parquet) where we store the curated dataset for the notebook.
    min_net_spend
        Removes negligible transactions where the net spend is close to zero.
    drop_returns
        Removes rows where spend < 0 or quantity <= 0. These rows make association
        rules noisy because they represent corrections rather than true purchases.
    """

    raw_data_dir = Path(raw_data_dir)
    output_path = _ensure_path(output_path)

    transactions = pd.read_csv(raw_data_dir / "transaction_data.csv")
    products = pd.read_csv(raw_data_dir / "product.csv")

    df = transactions.merge(
        products,
        on="PRODUCT_ID",
        how="left",
        validate="many_to_one",
    )

    discount_cols = ["RETAIL_DISC", "COUPON_DISC", "COUPON_MATCH_DISC"]
    for col in discount_cols:
        df[col] = df[col].fillna(0.0)

    df["NET_SPEND"] = df["SALES_VALUE"] - df[discount_cols].sum(axis=1)
    df["NET_SPEND"] = df["NET_SPEND"].round(2)
    df["IS_RETURN"] = (df["NET_SPEND"] < 0) | (df["QUANTITY"] <= 0)
    if drop_returns:
        df = df.loc[~df["IS_RETURN"]].copy()

    df = df.loc[df["NET_SPEND"] >= min_net_spend].copy()
    df["PRICE_PER_UNIT"] = np.where(
        df["QUANTITY"] > 0, df["NET_SPEND"] / df["QUANTITY"], np.nan
    )
    df["PRICE_PER_UNIT"] = df["PRICE_PER_UNIT"].round(2)
    df["TXN_DATE"] = BASE_DATE + pd.to_timedelta(df["DAY"] - 1, unit="D")

    selected_cols = [
        "household_key",
        "BASKET_ID",
        "DAY",
        "TXN_DATE",
        "WEEK_NO",
        "STORE_ID",
        "PRODUCT_ID",
        "DEPARTMENT",
        "COMMODITY_DESC",
        "SUB_COMMODITY_DESC",
        "BRAND",
        "MANUFACTURER",
        "QUANTITY",
        "SALES_VALUE",
        "NET_SPEND",
        "PRICE_PER_UNIT",
    ]
    df = df[selected_cols].copy()

    df.to_parquet(output_path, index=False)
    return df


def load_basket_dataset(output_path: PathLike) -> pd.DataFrame:
    """
    Load the curated dataset created by build_and_save_basket_dataset.
    """

    return pd.read_parquet(output_path)
