# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# unused-variable

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
processing_correlation.py

This module prepares financial asset datasets specifically for use in correlation-based
analysis workflows. It handles standardised loading, cleaning, and formatting of
historical price data — ensuring readiness for correlation matrix generation, heatmaps,
and pairwise statistical evaluations.

This file is tailored for the Market & Volatility Scanner (Statistical Analysis module)
and differs from `processing_default.py` by structuring outputs to support:
- Normalised return series comparison
- Alignment across asset groups (e.g., ETFs, currencies, equities)
- Readiness for dynamic correlation mapping and heatmap rendering

It relies on:
- `shared_utils.py`: Core cleaning helpers (e.g., volume, numeric sanitisation)
- `asset_map.py`: Declarative paths for all structured asset datasets

Used by:
- Market & Volatility Scanner: Correlation panels, statistical calculators
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Internal Imports — Reusable Data Processing Components
# -------------------------------------------------------------------------------------------------
from .shared_utils import (
    convert_date_to_us_format,
    clean_volume,
    sanitize_numeric_columns,
    drop_incomplete_rows,
)
from .asset_map import asset_files

# -------------------------------------------------------------------------------------------------
# Internal Imports — Reusable Data Processing Components
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.asset_map import asset_files

# -------------------------------------------------------------------------------------------------
# ATR Calculation
# -------------------------------------------------------------------------------------------------
def calculate_atr(processed_df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Calculate the Average True Range (ATR) for the provided DataFrame.

    ATR measures market volatility using the greatest of three metrics: high-low range,
    high to previous close, and low to previous close.

    Parameters:
        processed_df (pd.DataFrame): Asset price data including 'high', 'low', and 'close'.
        window (int): The rolling window size for ATR calculation (default is 14).

    Returns:
        pd.DataFrame: The input DataFrame with added 'ATR', '1d_atr', '1w_atr', '1m_atr' columns.
    """
    try:
        # Calculate previous close for comparison
        processed_df['Previous Close'] = processed_df['close'].shift(1)

        # Calculate the high-low range for each trading day
        processed_df['High-Low'] = processed_df['high'] - processed_df['low']

        # Calculate the high to previous close range
        processed_df['High-Previous Close'] = abs(
            processed_df['high'] - processed_df['Previous Close']
        )

        # Calculate the low to previous close range
        processed_df['Low-Previous Close'] = abs(
            processed_df['low'] - processed_df['Previous Close']
        )

        # The True Range (TR) is the maximum of the high-low range, high-previous close,
        # and low-previous close
        processed_df['True Range'] = processed_df[[
            'High-Low', 'High-Previous Close', 'Low-Previous Close'
        ]].max(axis=1)

        # Calculate the rolling ATR with the default 14-day window
        processed_df['ATR'] = processed_df['True Range'].rolling(window=window).mean()

        # Calculate the rolling ATR for 1-day, 1-week, and 1-month periods
        # Required for Volatility vs DPT Achievement Charts
        processed_df['1d_atr'] = processed_df['True Range'].rolling(window=window).mean()
        processed_df['1w_atr'] = processed_df['True Range'].rolling(window=window * 5).mean()
        processed_df['1m_atr'] = processed_df['True Range'].rolling(window=window * 20).mean()

        # Clean the ATR and other related columns to remove unwanted characters (if any)
        for col in ['True Range', 'ATR', '1d_atr', '1w_atr', '1m_atr']:
            processed_df[col] = processed_df[col].astype(str)  # Ensure it's string type
            # Remove unwanted characters (e.g., commas, '%', quotes, spaces)
            processed_df[col] = processed_df[col].replace(
            {',': '', '%': '', "'": '', ' ': ''}, regex=True)
            # Convert to numeric, handling errors with 'coerce'
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')

    except Exception as error:
        # Raise a more specific error if calculation fails
        raise ValueError(f"Error calculating ATR: {error}") from error

    return processed_df

# -------------------------------------------------------------------------------------------------
# Returns: Weekly, Monthly, Quarterly, etc.
# -------------------------------------------------------------------------------------------------
def resample_and_calculate_returns(processed_df: pd.DataFrame):
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
    try:
        processed_df["date"] = pd.to_datetime(processed_df["date"], errors="coerce")

        weekly_df = processed_df.resample("W", on="date")["close"].last().pct_change()
        monthly_df = processed_df.resample("ME", on="date")["close"].last().pct_change()
        quarterly_df = processed_df.resample("3ME", on="date")["close"].last().pct_change()
        six_month_df = processed_df.resample("6ME", on="date")["close"].last().pct_change()
        yearly_df = processed_df.resample("12ME", on="date")["close"].last().pct_change()

        weekly_returns_df = weekly_df.reset_index().rename(
        columns={"close": "weekly_return"})
        monthly_returns_df = monthly_df.reset_index().rename(
        columns={"close": "monthly_return"})
        quarterly_returns_df = quarterly_df.reset_index().rename(
        columns={"close": "quarterly_return"})
        six_month_returns_df = six_month_df.reset_index().rename(
        columns={"close": "six_month_return"})
        yearly_returns_df = yearly_df.reset_index().rename(
        columns={"close": "yearly_return"})

        return (
            weekly_returns_df,
            monthly_returns_df,
            quarterly_returns_df,
            six_month_returns_df,
            yearly_returns_df
        )

    except Exception as error:
        raise ValueError(f"Error calculating resampled returns: {error}") from error

# -------------------------------------------------------------------------------------------------
# Main Cleaning Function (Single Asset)
# -------------------------------------------------------------------------------------------------
def clean_data(
    processed_df: pd.DataFrame,
    timeline: str,
    desired_profit_target: float | None = None
):
    """
    Clean and enrich asset data for statistical analysis.

    Parameters:
        processed_df (pd.DataFrame): Raw asset data with columns like 'date',
        'open', 'high', 'low', 'close'.
        timeline (str): One of ['Intraday', 'Overnight', 'Interday', 'Daily H-L']
        for return calculation.
        desired_profit_target (float | None): Optional target for DPT probability analysis.

    Returns:
        tuple: Enriched primary and secondary datasets, including:
            - processed_df: Cleaned and enriched daily dataset
            - [weekly/monthly/quarterly/6mo/yr] returns
            - weekly_df, monthly_df: ATR resampled datasets
            - start_date, end_date: Analysis range
    """
    try:
        # --- Rename Columns ---
        processed_df.rename(columns={
            "Date": "date", "Open": "open", "High": "high", "Low": "low",
            "Close": "close", "Price": "close", "Last": "close",
            "Volume": "volume", "Vol.": "volume"
        }, inplace=True)

        # --- Date Parsing ---
        processed_df = convert_date_to_us_format(processed_df, "date")

        # --- Volume Cleanup ---
        processed_df = clean_volume(processed_df)

        # --- Numeric Sanitisation ---
        processed_df = sanitize_numeric_columns(
            processed_df, ["open", "high", "low", "close", "volume"]
        )

        # --- Drop Incomplete or Redundant Rows ---
        processed_df = drop_incomplete_rows(
        processed_df, ["date", "open", "high", "low", "close"])
        processed_df = processed_df[processed_df["high"] != processed_df["low"]]
        processed_df = processed_df[~((processed_df["close"] == processed_df["high"]) &
                                      (processed_df["open"] == processed_df["low"]))]
        processed_df.drop_duplicates(inplace=True)
        processed_df.sort_values("date", inplace=True)

        # --- Return Calculations by Timeline ---
        if timeline == "Intraday":
            processed_df["Intraday"] = processed_df["close"] / processed_df["open"] - 1
        elif timeline == "Overnight":
            processed_df["Overnight"] = processed_df["open"] / processed_df["close"].shift() - 1
        elif timeline == "Interday":
            processed_df["Interday"] = processed_df["close"].pct_change()
        elif timeline == "Daily H-L":
            processed_df["Daily H-L"] = (
            processed_df["high"] - processed_df["low"]) / processed_df["low"]

        # --- Volatility Features ---
        processed_df["return"] = processed_df["close"].pct_change()
        processed_df["volatility"] = processed_df["return"].rolling(window=14).std()
        processed_df["STDdev"] = processed_df["close"].rolling(window=14).std()
        processed_df["STDdev%"] = (processed_df["STDdev"] / processed_df["close"]) * 100

        processed_df["Volatility Category"] = pd.cut(
            processed_df["STDdev%"],
            bins=[-float("inf"), 2, 5, float("inf")],
            labels=["Low", "Medium", "High"]
        )

        # --- ATR Calculation (Daily) ---
        processed_df = calculate_atr(processed_df, window=14)

        # --- DPT Tracking (If Applicable) ---
        if "Interday" in processed_df.columns and desired_profit_target is not None:
            processed_df["DPT_achieved"] = (processed_df["Interday"] * desired_profit_target) / 100

        # --- Weekly & Monthly Aggregation (High/Low/Close) ---
        weekly_df = processed_df.resample("W", on="date").agg({
            "high": "max", "low": "min", "close": "last"
        }).reset_index()

        monthly_df = processed_df.resample("ME", on="date").agg({
            "high": "max", "low": "min", "close": "last"
        }).reset_index()

        # --- Reapply ATR to Aggregated Frames ---
        weekly_df = calculate_atr(weekly_df, window=14)
        monthly_df = calculate_atr(monthly_df, window=14)

        # --- Multi-Timeline Return Panels ---
        (
            weekly_returns_df,
            monthly_returns_df,
            quarterly_returns_df,
            six_month_returns_df,
            yearly_returns_df
        ) = resample_and_calculate_returns(processed_df)

        # --- Dataset Window Metadata ---
        start_date = processed_df["date"].min().strftime("%m/%d/%Y")
        end_date = processed_df["date"].max().strftime("%m/%d/%Y")

        return (
            processed_df,
            weekly_returns_df, monthly_returns_df, quarterly_returns_df,
            six_month_returns_df, yearly_returns_df,
            weekly_df, monthly_df,
            start_date, end_date
        )

    except Exception as error:
        raise ValueError(f"Error cleaning data: {error}") from error

# -------------------------------------------------------------------------------------------------
# Cleaning Function (Correlation Asset)
# -------------------------------------------------------------------------------------------------
def clean_generic_data(processed_df, name_column: str, name_value: str):  # pylint: disable=unused-argument
    """
    Clean and prepare external asset data for correlation and volatility panels.

    Parameters:
        processed_df (pd.DataFrame): Raw external asset data to align with primary asset.
        name_column (str): Name of the reference asset column (not used here, but
        preserved for signature match).
        name_value (str): Label prefix for volatility/return metrics (e.g., 'gold', 'nasdaq').

    Returns:
        pd.DataFrame: Cleaned dataframe with prefixed return, ATR, and volatility columns.
    """
    try:
        # --- Standardise column names ---
        processed_df.rename(columns={
            "Date": "date", "Open": "open", "High": "high", "Low": "low",
            "Close": "close", "Price": "close", "Last": "close",
            "Volume": "volume", "Vol.": "volume"
        }, inplace=True)

        # --- Date Conversion ---
        processed_df = convert_date_to_us_format(processed_df, "date")

        # --- Volume and Numerics Cleanup ---
        processed_df = clean_volume(processed_df)
        processed_df = sanitize_numeric_columns(
        processed_df, ["open", "high", "low", "close", "volume"])

        # --- Drop incomplete / duplicate rows ---
        processed_df.dropna(subset=["date", "open", "high", "low", "close"], inplace=True)
        processed_df["volume"].fillna(0, inplace=True)
        processed_df = processed_df[processed_df["high"] != processed_df["low"]]
        processed_df = processed_df[~((processed_df["close"] == processed_df["high"]) &
                                      (processed_df["open"] == processed_df["low"]))]
        processed_df.drop_duplicates(inplace=True)
        processed_df.sort_values("date", inplace=True)

        # --- Return and Volatility Metrics ---
        processed_df["return"] = processed_df["close"].pct_change()
        processed_df.rename(columns={"return": f"{name_value}_return"}, inplace=True)

        processed_df.dropna(subset=["date", "close"], inplace=True)

        # --- Return Column Cleanup (string coercion + numeric) ---
        if f"{name_value}_return" in processed_df.columns:
            processed_df[f"{name_value}_return"] = (
                processed_df[f"{name_value}_return"]
                .astype(str)
                .replace({",": "", "%": "", "'": "", " ": ""}, regex=True)
            )
            processed_df[f"{name_value}_return"] = pd.to_numeric(
                processed_df[f"{name_value}_return"], errors="coerce"
            )
            processed_df[f"{name_value}_return"] = processed_df[f"{name_value}_return"].apply(
                lambda x: None if x == 0 else x
            )

        # --- ATR and Rolling Volatility ---
        processed_df = calculate_atr(processed_df, window=14)

        processed_df["STDdev"] = processed_df["close"].rolling(window=14).std()
        processed_df["STDdev%"] = (processed_df["STDdev"] / processed_df["close"]) * 100

        # --- Volatility Rating ---
        processed_df["Volatility Category"] = pd.cut(
            processed_df["STDdev%"],
            bins=[-float("inf"), 2, 5, float("inf")],
            labels=["Low", "Medium", "High"]
        )

        # --- Rename to Prefix with Asset Name ---
        processed_df.rename(columns={
            "STDdev%": f"{name_value}_STDdev%",
            "ATR": f"{name_value}_ATR%",
            "Volatility Category": f"{name_value}_rating"
        }, inplace=True)

        return processed_df

    except Exception as error:
        raise ValueError(f"Error cleaning data for {name_value}: {error}") from error

# -------------------------------------------------------------------------------------------------
# Load Predefined Asset (via asset_map) — Market & Volatility Scanner
# -------------------------------------------------------------------------------------------------
def load_asset_data(
    asset_category: str,
    asset_sample: str,
    timeline: str,
    desired_profit_target: float | None
) -> tuple[pd.DataFrame, str, str]:
    """
    Load and prepare the selected financial asset for statistical analysis.

    This function resolves the appropriate CSV file from the asset map and
    delegates processing to a dedicated loader that applies cleaning,
    timeline handling, and optional DPT logic.

    Parameters:
        asset_category (str): Asset group/category (e.g., "Equities - Magnificent Seven").
        asset_sample (str): Asset label (e.g., "NVIDIA").
        timeline (str): Analysis timeline ("Intraday", "Interday", etc.).
        desired_profit_target (float | None): Optional DPT (%) for DPT calculation.

    Returns:
        tuple:
            - processed_df (pd.DataFrame): Cleaned and enriched asset dataset.
            - data_title (str): Final resolved asset label (for display).
            - asset_type (str): Category type (for downstream use).
    """
    asset_file = asset_files.get(asset_category, {}).get(asset_sample)

    if asset_file is None:
        # Fallback to Tesla if the requested asset is unavailable
        asset_file = (
            "app/data_sources/financial_data/equities_mag7/Tesla Stock Price History.csv"
        )
        asset_sample = "Tesla"
        asset_category = "Equities - Magnificent Seven"

    data_title = asset_sample
    asset_type = asset_category

    # Load and process data
    processed_df = load_data_from_file(
        asset_file, timeline, desired_profit_target
    )

    return processed_df, data_title, asset_type

# -------------------------------------------------------------------------------------------------
# Returns – User Uploads
# -------------------------------------------------------------------------------------------------
def load_and_prepare_user_returns(uploaded_files):
    """
    Load and clean all user-uploaded datasets for return analysis.

    Each file is read, standardised using `clean_generic_data`, and labelled by filename
    for contextual tracking. Returns a consolidated DataFrame suitable for temporal return
    breakdowns and cross-asset return diagnostics.

    Parameters:
        uploaded_files (list): List of Streamlit `UploadedFile` objects (.csv expected).

    Returns:
        pd.DataFrame: returns_df_user — cleaned and concatenated data for returns analysis.
    """
    user_data_frames = []

    for uploaded_file in uploaded_files:
        # Load the CSV into a DataFrame
        user_df = pd.read_csv(uploaded_file)

        # Extract identifier from filename
        name_value = uploaded_file.name.split(".")[0]

        # Clean and standardise the dataset
        cleaned_user_data = clean_generic_data(user_df, "user_asset", name_value)

        # Collect into unified structure
        user_data_frames.append(cleaned_user_data)

    # Merge all into a single DataFrame for return-related analysis
    returns_df_user = pd.concat(user_data_frames, axis=0, ignore_index=True)

    return returns_df_user

# -------------------------------------------------------------------------------------------------
# Load Data from CSV (Uploaded or Local)
# -------------------------------------------------------------------------------------------------
def load_data_from_file(file, timeline, desired_profit_target):
    """
    Load and clean asset data from a CSV source, applying timeline-specific
    return logic and DPT-adjusted volatility preparation.

    This function processes raw CSV input (from user upload or predefined map),
    routes it through the full `clean_data()` workflow, and returns a structured
    `processed_df` ready for primary analytics and `filtering_df` for UI filtering.

    Parameters:
        file (str or file-like object): Path to the CSV file or Streamlit upload.
        timeline (str): Selected return timeline ('Intraday', 'Overnight', 'Interday', etc.).
        desired_profit_target (float or None): Optional DPT threshold for Interday analysis.

    Returns:
        pd.DataFrame: processed_df — fully cleaned and enriched with return and volatility features.
    """
    try:
        # Load raw data
        processed_df = pd.read_csv(file)

        # Clean, enrich, and calculate core indicators
        processed_df, _, _, _, _, _, _, _, _, _ = clean_data(
            processed_df, timeline, desired_profit_target
        )

        # Note: `_` placeholders intentionally suppress unused outputs (e.g., resampled returns)

    except Exception as error:
        raise ValueError(f"Error loading data from file: {error}") from error

    return processed_df
