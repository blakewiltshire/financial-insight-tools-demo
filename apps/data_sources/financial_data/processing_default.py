# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, unused-variable
# pylint: disable=invalid-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Processing Default — Single Asset Financial Data Cleaning

This module prepares individual asset files (e.g., Tesla.csv) for use in trend/volatility apps.
It applies renaming, volume cleaning, return calculations, and resampling logic — without
handling bulk correlation or economic series.

Dependencies:
- Shared utils: `shared_utils.py`
- Asset mapping: `asset_map.py`

Used by:
- 04_📊_Price_Action_and_Trend_Confirmation.py
- Trade and volatility apps focused on single security input

Key Functions:
- clean_data: Full pipeline for renaming, cleaning, and calculating metrics
- calculate_atr: Computes ATR + rolling windows
- resample_and_calculate_returns: Resamples for returns across multiple timeframes
- resample_data: Resamples OHLC data into timeframes
- load_data_from_file: Load and clean user CSV uploads
- load_asset_data: Load and clean preloaded asset by name/category

Aligned to path: `/apps/data_sources/financial_data/`
"""
# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
from .shared_utils import (
    convert_date_to_us_format,
    clean_volume,
    sanitize_numeric_columns,
    drop_incomplete_rows,
)
from .asset_map import asset_files

# -------------------------------------------------------------------------------------------------
# ATR Calculation
# -------------------------------------------------------------------------------------------------
def calculate_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Calculates Average True Range (ATR) and additional volatility bands.
    """
    df["Previous Close"] = df["close"].shift(1)
    df["High-Low"] = df["high"] - df["low"]
    df["High-PrevClose"] = (df["high"] - df["Previous Close"]).abs()
    df["Low-PrevClose"] = (df["low"] - df["Previous Close"]).abs()
    df["True Range"] = df[["High-Low", "High-PrevClose", "Low-PrevClose"]].max(axis=1)
    df["ATR"] = df["True Range"].rolling(window=window).mean()
    return df

# -------------------------------------------------------------------------------------------------
# Returns: Weekly, Monthly, Quarterly, etc.
# -------------------------------------------------------------------------------------------------
def resample_and_calculate_returns(df: pd.DataFrame):
    """
    Resample data and calculate returns across multiple timeframes.

    Parameters:
        processed_df (pd.DataFrame): DataFrame with 'date' and 'close' columns.

    Returns:
        tuple: DataFrames with calculated returns for:
               - Weekly
               - Monthly
               - Quarterly
               - Six-Month
               - Yearly
    """
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    returns = {}
    rules = {
        "weekly": "W",
        "monthly": "ME",
        "quarterly": "3ME",
        "six_month": "6ME",
        "yearly": "12ME",
    }
    for label, rule in rules.items():
        temp = df.resample(rule, on="date")["close"].last().pct_change() * 100
        returns[label] = temp.reset_index().rename(columns={"close": f"{label}_return"})
    return returns

# -------------------------------------------------------------------------------------------------
# Main Cleaning Function (Single Asset)
# -------------------------------------------------------------------------------------------------
def clean_data(
    df: pd.DataFrame,
    timeline: str = "Interday",
    desired_profit_target: float | None = None
) -> tuple[pd.DataFrame, dict]:
    """
    Core data cleaning and feature engineering pipeline for a single financial asset.

    Applies standard cleaning and transformation steps to prepare price-action data for
    statistical analysis, visualisation, and trade signal generation. Converts raw price
    series into structured returns, volatility, and profit-target indicators based on the
    selected timeline.

    Cleaning and transformations:
    - Column renaming (standardises headers like 'Date', 'Open', 'Close')
    - Date formatting and validation
    - Volume conversion (handles K/M/B suffixes)
    - Numeric coercion for key columns
    - Removal of incomplete or structurally invalid rows
    - Timeline-specific return calculations: Intraday, Overnight, Interday, Daily H-L
    - Universal return, volatility, and standard deviation (% and absolute)
    - Volatility category (Low / Medium / High) using 14-period rolling STDdev%
    - ATR calculation via `calculate_atr`
    - Optional: DPT (Desired Profit Target) achievement flag

    Args:
        df (pd.DataFrame): Raw asset-level price data.
        timeline (str): Timeline for derived returns ('Intraday', 'Overnight', etc.).
        desired_profit_target (float | None): Optional DPT percentage for strategy tagging.

    Returns:
        tuple:
            pd.DataFrame: Cleaned and feature-rich DataFrame.
            dict: Summary metadata including date range and shape.
    """
    df.rename(columns={
        "Date": "date", "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Price": "close", "Last": "close",
        "Volume": "volume", "Vol.": "volume"
    }, inplace=True)

    df = convert_date_to_us_format(df, "date")
    df = clean_volume(df)
    df = sanitize_numeric_columns(df, ["open", "high", "low", "close", "volume"])
    df = drop_incomplete_rows(df, ["date", "open", "high", "low", "close"])

    df = df[df["high"] != df["low"]]  # Remove flat bars
    df = df[~((df["close"] == df["high"]) & (df["open"] == df["low"]))]
    df.drop_duplicates(inplace=True)
    df.sort_values("date", inplace=True)

    if timeline == "Intraday":
        df["Intraday"] = df["close"] / df["open"] - 1
    elif timeline == "Overnight":
        df["Overnight"] = df["open"] / df["close"].shift() - 1
    elif timeline == "Interday":
        df["Interday"] = df["close"].pct_change()
    elif timeline == "Daily H-L":
        df["Daily H-L"] = (df["high"] - df["low"]) / df["low"]

    df["return"] = df["close"].pct_change()
    df["volatility"] = df["return"].rolling(window=14).std()
    df["STDdev"] = df["close"].rolling(window=14).std()
    df["STDdev%"] = (df["STDdev"] / df["close"]) * 100

    bins = [-float("inf"), 2, 5, float("inf")]
    labels = ["Low", "Medium", "High"]
    df["Volatility Category"] = pd.cut(df["STDdev%"], bins=bins, labels=labels)

    df = calculate_atr(df)

    if "Interday" in df.columns and desired_profit_target is not None:
        df["DPT_achieved"] = (df["Interday"] * desired_profit_target) / 100

    dataset_info = {
        "start_date": df["date"].min().strftime("%m/%d/%Y"),
        "end_date": df["date"].max().strftime("%m/%d/%Y"),
        "rows": len(df),
        "columns": df.shape[1]
    }

    return df, dataset_info

# -------------------------------------------------------------------------------------------------
# Minimal Cleaning Function (Single Asset)
# -------------------------------------------------------------------------------------------------
def clean_data_minimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    Minimal cleaning for currency conversion and structural reuse.

    Keeps only: date, open, high, low, close, volume — with standard formatting.
    No returns, volatility, or derived metrics are calculated.

    Args:
        df (pd.DataFrame): Raw asset-level price data from CSV or upload.

    Returns:
        pd.DataFrame: Cleaned DataFrame with standardised format.
    """
    # Standardise column names
    df.rename(columns={
        "Date": "date", "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Price": "close", "Last": "close",
        "Volume": "volume", "Vol.": "volume"
    }, inplace=True)

    # Format dates
    df = convert_date_to_us_format(df, "date")

    # Clean volume (e.g. '1.5K', '2.1M' → float)
    df = clean_volume(df)

    # Ensure numeric fields are float
    df = sanitize_numeric_columns(df, ["open", "high", "low", "close", "volume"])

    # Drop any structurally invalid or incomplete rows
    df = drop_incomplete_rows(df, ["date", "open", "high", "low", "close"])

    # Drop exact duplicates
    df.drop_duplicates(inplace=True)

    # Sort chronologically
    df.sort_values("date", inplace=True)

    # Reorder and return minimal columns
    return df[["date", "open", "high", "low", "close", "volume"]]

# -------------------------------------------------------------------------------------------------
# Resample OHLC Data to Selected Timeframe
# -------------------------------------------------------------------------------------------------
def resample_data(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample data and aggregation operations across multiple timeframes.

    Parameters:
        processed_df (pd.DataFrame): DataFrame with 'date', 'open', 'first', 'high', 'max', 'low',
        'min', 'close', 'last', 'volume', 'sum' columns.

    Returns:
        tuple: DataFrames with aggregation operations for timeframes:
               - Intraday
               - Daily
               - Weekly
               - Monthly
    """
    if "date" not in df.columns:
        raise ValueError("Missing 'date' column. Ensure your dataset includes proper dates.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    df.sort_values("date", ascending=True, inplace=True)
    df.set_index("date", inplace=True)

    resample_map = {
        "Intraday": df,
        "Daily": df,
        "Weekly": df.resample("W").agg({
            "open": "first", "high": "max", "low": "min",
            "close": "last", "volume": "sum"
        }).dropna(),
        "Monthly": df.resample("ME").agg({
            "open": "first", "high": "max", "low": "min",
            "close": "last", "volume": "sum"
        }).dropna(),
    }

    return resample_map.get(timeframe, df).reset_index()

# -------------------------------------------------------------------------------------------------
# Load Data from CSV (Uploaded or Local)
# -------------------------------------------------------------------------------------------------
def load_data_from_file(file):
    """
    Load and clean data from a CSV file.

    Parameters:
        file: Path to the CSV file or a file-like object (e.g., from Streamlit upload).

    Returns:
        pd.DataFrame: Cleaned DataFrame ready for analysis.
    """
    try:
        processed_df = pd.read_csv(file)
        processed_df, dataset_info = clean_data(processed_df)
        return processed_df

    except Exception as error:
        raise ValueError(f"Error loading data from file: {error}") from error

# -------------------------------------------------------------------------------------------------
# Load Predefined Asset (from asset_map)
# -------------------------------------------------------------------------------------------------
def load_asset_data(asset_category: str, asset_sample: str) -> tuple[pd.DataFrame, str, str]:
    """"
    Loads a preconfigured asset file from the asset map and returns its content.

    This function retrieves the full path of a selected asset based on its category
    and sample name. If the asset is not found, it defaults to Tesla under
    'Equities - Magnificent Seven'. The returned data is raw and unprocessed.

    Args:
        asset_category (str): Category of the asset (e.g., "Equities - Magnificent Seven").
        asset_sample (str): Specific asset name within the category (e.g., "NVIDIA").

    Returns:
        tuple:
            - pd.DataFrame: Raw asset data loaded from CSV.
            - str: Final resolved asset name (after defaulting if needed).
            - str: Final resolved asset category (after defaulting if needed).
    """
    asset_file = asset_files.get(asset_category, {}).get(asset_sample)
    if asset_file is None:
        asset_file = asset_files["Equities - Magnificent Seven"]["Tesla"]
        asset_sample = "Tesla"
        asset_category = "Equities - Magnificent Seven"

    df = pd.read_csv(asset_file)
    return df, asset_sample, asset_category


# -------------------------------------------------------------------------------------------------
# Data Resampling Function (Weekly & Monthly)
# -------------------------------------------------------------------------------------------------

def resample_spread_data(df, timeframe):
    """
    . Used by Spread & Pair Analysis
    """
    if 'date' not in df.columns:
        raise ValueError("Missing 'date' column. Ensure your dataset includes proper dates.")

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df.dropna(subset=['date'], inplace=True)
    df.sort_values('date', ascending=True, inplace=True)
    df.set_index('date', inplace=True)

    resample_map = {
        "Daily": df,
        "Weekly": df.resample('W').agg({
            'close_long': 'last',
            'close_short': 'last',
            'Spread Ratio': 'last'
        }).dropna(),
        "Monthly": df.resample('ME').agg({
            'close_long': 'last',
            'close_short': 'last',
            'Spread Ratio': 'last'
        }).dropna()
    }

    return resample_map.get(timeframe, df).reset_index()

# -------------------------------------------------------------------------------------------------
# General-Purpose Resample Handler
# -------------------------------------------------------------------------------------------------
def resample_to_frequency(df: pd.DataFrame, column: str, timeframe: str) -> pd.DataFrame:
    """
    Resample a dataframe on 'date' column to a chosen frequency using the specified column.

    Args:
        df (pd.DataFrame): Dataframe with a 'date' and value column.
        column (str): Column to use for value aggregation.
        timeframe (str): One of 'Daily', 'Weekly', 'Monthly'.

    Returns:
        pd.DataFrame: Resampled dataframe with 'date' and value column.
    """
    if 'date' not in df.columns:
        raise ValueError("Input dataframe must contain a 'date' column.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    df = df.set_index("date")

    rule = {
        "Daily": "D",
        "Weekly": "W",
        "Monthly": "M"
    }.get(timeframe, "D")

    resampled = df[[column]].resample(rule).last().dropna().reset_index()
    return resampled
