# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Shared Utilities — Financial Data Preprocessing

This module provides common utility functions used across financial data pipelines,
including:
- Date formatting
- Volume cleaning
- Lightweight column transformations
- Value sanitation for returns, volatility, and general numeric fields

Functions in this module are safe to use across both individual and bulk asset processors:
- Used by: `processing_default.py` and `processing_correlation.py`
- Aligned to: `/apps/data_sources/financial_data/`

Standard Usage:
- `convert_date_to_us_format`: Converts any date column to datetime (safe coercion)
- `clean_volume`: Converts 'K', 'M', 'B' suffixed volume to integer values
- `sanitize_numeric_columns`: Strips characters and coerces to numeric for selected columns
- `drop_incomplete_rows`: Drops rows with null in required columns

This utility layer is deliberately lightweight and stable — no third-party dependencies
outside of `pandas`.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Convert Date Column to US Format (MM/DD/YYYY)
# -------------------------------------------------------------------------------------------------
def convert_date_to_us_format(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    """
    Converts a specified date column to datetime (US format), coercing invalid entries.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        date_column (str): Name of the column containing date values

    Returns:
        pd.DataFrame: DataFrame with converted datetime column
    """
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    return df

# -------------------------------------------------------------------------------------------------
# Clean Volume Column (K, M, B suffix support)
# -------------------------------------------------------------------------------------------------
def clean_volume(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts volume entries containing suffixes (K, M, B) to numeric values.

    Parameters:
        df (pd.DataFrame): Input DataFrame with 'volume' column

    Returns:
        pd.DataFrame: Cleaned DataFrame with numeric volume column
    """
    def convert(v):
        if isinstance(v, str):
            v = v.replace(",", "")
            if "K" in v:
                return float(v.replace("K", "")) * 1_000
            if "M" in v:
                return float(v.replace("M", "")) * 1_000_000
            if "B" in v:
                return float(v.replace("B", "")) * 1_000_000_000
            return float(v)
        return v

    df["volume"] = df.get("volume", pd.Series([0] * len(df))).apply(convert)
    return df

# -------------------------------------------------------------------------------------------------
# Strip %, Commas, Quotes from Specified Columns (Safe Numeric Coercion)
# -------------------------------------------------------------------------------------------------
def sanitize_numeric_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Sanitises selected columns by removing %, commas, quotes, and coercing to numeric.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        columns (list[str]): List of column names to process

    Returns:
        pd.DataFrame: DataFrame with sanitised numeric columns
    """
    for col in columns:
        df[col] = df[col].astype(str).replace({",": "", "%": "", "'": "", " ": ""}, regex=True)
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

# -------------------------------------------------------------------------------------------------
# Drop Rows with Missing Values in Required Columns
# -------------------------------------------------------------------------------------------------
def drop_incomplete_rows(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """
    Drops rows that are missing values in specified required columns.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        required_columns (list[str]): List of columns that must not be null

    Returns:
        pd.DataFrame: Cleaned DataFrame with complete rows
    """
    return df.dropna(subset=required_columns)
