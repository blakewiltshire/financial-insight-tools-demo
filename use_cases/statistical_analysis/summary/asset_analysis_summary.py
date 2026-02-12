# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
statistics_summary.py

This module contains functions to calculate key metrics and indicators for financial assets.
The functions include calculations for asset performance (returns, drawdown), volatility, and
the Average True Range (ATR) for different asset types such as Equities,
Cryptocurrencies, and Forex.
Additional functionalities include calculating the probability of hitting a
desired profit target (DPT) and summarizing asset metrics for analysis.

Functions:
    - calculate_asset_metrics_basic: Calculate basic asset metrics such as last price,
    peak price, and bear market start date.
    - calculate_asset_returns: Calculate returns for daily, weekly, and monthly periods.
    - calculate_asset_metrics: Calls basic metrics and returns comprehensive asset metrics.
    - calculate_volatility: Calculate asset volatility based on standard deviation
    and High-Low range.
    - overview_metrics: Calculate standard deviation and mean high-low range for an asset.
    - calculate_and_format_atr: Calculate ATR for different asset types (percentage or pips).
    - calculate_probability_of_dpt: Calculate the probability of hitting a
    desired profit target (DPT).
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
from fractions import Fraction
import pandas as pd


# -------------------------------------------------------------------------------------------------
# Function: calculate_asset_metrics_basic
# Purpose: Compute foundational metrics such as last price, peak/min levels, and bear market onset.
# Use Case: Asset Snapshot / Metric Summary (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# def calculate_asset_metrics_basic(processed_df):
#     """
#     Basic metrics for the asset: last price, max, min prices, and dates.
#     """
#     if processed_df.empty:
#         raise ValueError("The DataFrame is empty, cannot calculate asset metrics.")
#
#     last_price = processed_df['close'].iloc[-1] if processed_df.shape[0] > 0 else None
#     peak_price = processed_df['close'].max() if processed_df.shape[0] > 0 else None
#
#     # Ensure we have data for bear market threshold calculation
#     bear_market_threshold = peak_price * 0.80 if peak_price is not None else None
#
#     bear_market_start_date = processed_df[
#         processed_df['close'] <= bear_market_threshold
#     ].iloc[0]['date'] if bear_market_threshold is not None else None
#
#     # Ensure we have data for max price and date
#     max_price = processed_df['close'].max() if processed_df.shape[0] > 0 else None
#     max_price_date = processed_df.loc[
#         processed_df['close'] == max_price, 'date'
#     ].iloc[0] if max_price is not None else None
#
#     # Ensure we have data for min price and date
#     min_price = processed_df['close'].min() if processed_df.shape[0] > 0 else None
#     min_price_date = processed_df.loc[
#         processed_df['close'] == min_price, 'date'
#     ].iloc[0] if min_price is not None else None
#
#     # Ensure we have data for high price and date
#     high_price = processed_df['high'].max() if processed_df.shape[0] > 0 else None
#     high_price_date = processed_df.loc[
#         processed_df['high'] == high_price, 'date'
#     ].iloc[0] if high_price is not None else None
#
#     # Ensure we have data for low price and date
#     low_price = processed_df['low'].min() if processed_df.shape[0] > 0 else None
#     low_price_date = processed_df.loc[
#         processed_df['low'] == low_price, 'date'
#     ].iloc[0] if low_price is not None else None
#
#     return (
#         last_price, bear_market_start_date, max_price, max_price_date, min_price, min_price_date,
#         high_price, high_price_date, low_price, low_price_date
#     )

def calculate_asset_metrics_basic(processed_df):
    if processed_df.empty:
        raise ValueError("The DataFrame is empty, cannot calculate asset metrics.")

    # Always ensure ascending time
    processed_df = processed_df.sort_values("date").reset_index(drop=True)

    last_price = processed_df["close"].iloc[-1]

    # Running peak & drawdown (proper bear logic)
    running_peak = processed_df["close"].cummax()
    drawdown = processed_df["close"] / running_peak - 1.0  # negative in drawdowns
    bear_mask = drawdown <= -0.20

    # Most recent bear date (or None)
    bear_market_start_date = (
        processed_df.loc[bear_mask, "date"].iloc[-1]
        if bear_mask.any()
        else None
    )

    # Standard max/min stats (unchanged)
    max_price = processed_df["close"].max()
    max_price_date = processed_df.loc[processed_df["close"] == max_price, "date"].iloc[0]

    min_price = processed_df["close"].min()
    min_price_date = processed_df.loc[processed_df["close"] == min_price, "date"].iloc[0]

    high_price = processed_df["high"].max()
    high_price_date = processed_df.loc[processed_df["high"] == high_price, "date"].iloc[0]

    low_price = processed_df["low"].min()
    low_price_date = processed_df.loc[processed_df["low"] == low_price, "date"].iloc[0]

    return (
        last_price,
        bear_market_start_date,
        max_price,
        max_price_date,
        min_price,
        min_price_date,
        high_price,
        high_price_date,
        low_price,
        low_price_date,
    )


# -------------------------------------------------------------------------------------------------
# Function: calculate_asset_returns
# Purpose: Compute percentage-based asset returns across common short-term periods
# (daily, weekly, monthly).
# Use Case: Asset Snapshot / ATR & Returns (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def calculate_asset_returns(processed_df):
    """
    Calculate the returns in percentage: daily, weekly, and monthly returns.
    """
    daily_return = (processed_df['close'].pct_change().iloc[-1]) * 100
    weekly_return = (processed_df['close'].pct_change(periods=5).iloc[-1]) * 100
    monthly_return = (processed_df['close'].pct_change(periods=21).iloc[-1]) * 100

    return daily_return, weekly_return, monthly_return

# -------------------------------------------------------------------------------------------------
# Function: calculate_asset_metrics
# Purpose: Aggregate key performance metrics including drawdown, price extremes, and
# multi-period returns.
# Use Case: Asset Snapshot / Metric Summary (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
# pylint: disable=too-many-locals
def calculate_asset_metrics(processed_df):
    """
    Calls the basic metrics and returns the full asset metrics.
    """
    last_price, bear_market_start_date, max_price, max_price_date, \
    min_price, min_price_date, high_price, high_price_date, \
    low_price, low_price_date = calculate_asset_metrics_basic(processed_df)

    daily_return, weekly_return, monthly_return = calculate_asset_returns(processed_df)

    # Calculate days since bear market
    last_bear_market_date = pd.to_datetime(bear_market_start_date)
    current_date = pd.to_datetime(processed_df['date'].iloc[-1])
    days_since_bear_market = (current_date - last_bear_market_date).days

    # Calculate current drawdown (percentage drop from peak to current price)
    current_drawdown = ((max_price - last_price) / max_price) * 100

    return (
        last_price,
        days_since_bear_market,
        current_drawdown,
        max_price,
        max_price_date,
        min_price,
        min_price_date,
        high_price,
        high_price_date,
        low_price,
        low_price_date,
        daily_return,
        weekly_return,
        monthly_return
    )

# -------------------------------------------------------------------------------------------------
# Function: calculate_volatility
# Purpose: Classify asset volatility by comparing return-based and price range measures,
# with contextual interpretation.
# Use Case: Asset Snapshot / Volatility Summary (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def calculate_volatility(processed_df, asset_name):
    """
    Calculate the volatility score of an asset based on its price fluctuations over time.

    This function calculates volatility using two methods:
    1. Standard deviation of the 'return' column (calculated in the `clean_data` function).
    2. The High-Low range expressed as a percentage of the closing price.

    The function categorizes the asset's volatility as 'Low', 'Medium', or 'High' based
    on the maximum value between the standard deviation of volatility and the mean
    High-Low percentage.

    Args:
        processed_df (DataFrame): A pandas DataFrame containing the asset's price data.
        asset_name (str): The name of the asset being analyzed.

    Returns:
        str: The volatility category ('Low', 'Medium', or 'High').
        str: A descriptive message about the asset's volatility.
    """

    # Check if the required 'return' column exists in the DataFrame
    if 'return' not in processed_df.columns:
        raise ValueError("Required 'return' column is missing.")

    # Calculate Standard deviation of volatility using the 'return' column
    volatility_std_dev = processed_df['return'].std()

    # Calculate High-Low range as a percentage of the closing price
    processed_df['High-Low Percentage'] = (processed_df['High-Low'] / processed_df['close']) * 100

    # Calculate the mean High-Low percentage
    mean_high_to_low_range = processed_df['High-Low Percentage'].mean()

    # Determine the volatility score as the maximum of the standard deviation
    # and the mean High-Low range
    volatility_score = max(volatility_std_dev, mean_high_to_low_range)

    # Categorize volatility based on the volatility score
    if volatility_score < 1.0:
        volatility_category = 'Low'
    elif volatility_score < 3.0:
        volatility_category = 'Medium'
    else:
        volatility_category = 'High'

    # Define messages for each volatility category
    volatility_message = {
        "High": f"{asset_name} exhibits high volatility, with substantial price fluctuations. "
                "The asset's volatility is driven by market sentiment, news, and "
                "macroeconomic factors.",

        "Medium": f"{asset_name} shows moderate volatility, with noticeable price fluctuations. "
                  "Its movements are within a historical range, influenced by "
                  "typical market factors.",

        "Low": f"{asset_name} shows low volatility, with minimal price fluctuations. "
               "Its price remains relatively steady, with movements that "
               "stay within predictable bounds."
    }

    # Return the volatility category and corresponding message
    return volatility_category, volatility_message[volatility_category]

# -------------------------------------------------------------------------------------------------
# Function: overview_metrics
# Purpose: Compute standard deviation and average high-low range for selected timeframes to
# support volatility panels.
# Use Case: Asset Snapshot (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def overview_metrics(processed_df, timeline):
    """
    Function to calculate and return key metrics for the Overview Section of the analysis.

    This function calculates:
        1. Standard Deviation: A measure of price volatility for the selected timeline.
        2. Mean High-to-Low Range: The average percentage difference between the high
        and low prices relative to the closing price.

    Parameters:
        processed_df (DataFrame): Processed data containing asset price and other relevant columns.
        timeline (str): Selected timeline for analysis, which determines the column for calculation
                        (Intraday, Overnight, Interday, or Daily H-L).

    Returns:
        tuple: A tuple containing the standard deviation (as a percentage) and the mean high-to-low
               range (as a percentage).
    """
    # Map timeline to the corresponding column name for price data
    column_map = {
        'Intraday': 'Intraday',   # Use the 'Intraday' column for intraday price changes
        'Overnight': 'Overnight', # Use the 'Overnight' column for overnight price changes
        'Interday': 'Interday',   # Use the 'Interday' column for interday price changes
        'Daily H-L': 'Daily H-L'  # Use the 'Daily H-L' column for daily high-low range analysis
    }

    # Select the appropriate column based on the timeline
    column = column_map.get(timeline)

    # Ensure the column exists in the data, raise an error if not found
    if column not in processed_df.columns:
        raise ValueError(f"Column '{column}' not found in the dataset for the selected timeline.")

    # Calculate the Standard Deviation for the selected column (price volatility)
    std_dev = processed_df[column].std() * 100  # Standard Deviation in percentage

    # Calculate the High-to-Low percentage for each row
    processed_df['High-Low Percentage'] = (processed_df['High-Low'] / processed_df['close']) * 100

    # Calculate the mean High-to-Low percentage for the entire period
    mean_high_to_low_range = processed_df['High-Low Percentage'].mean()

    # Return the calculated metrics
    return std_dev, mean_high_to_low_range

# -------------------------------------------------------------------------------------------------
# Function: calculate_and_format_atr
# Purpose: Calculate and return Average True Range (ATR) across daily, weekly, and
# monthly horizons — in both percentage and absolute terms.
# Use Case: Asset Snapshot - ATR & Returns (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def calculate_and_format_atr(processed_df, weekly_data, monthly_data, asset_type):
    """
    Calculate and format the Average True Range (ATR) for an asset based on its type.

    This function computes the ATR in two formats for the given asset type:
    - Percentage of the closing price for Equities, Cryptocurrency, and other asset types.
    - ATR in pips for Forex (Currencies).

    Parameters:
        processed_df (DataFrame): The processed daily data for the asset.
        weekly_data (DataFrame): The processed weekly data for the asset.
        monthly_data (DataFrame): The processed monthly data for the asset.
        asset_type (str): The type of asset (e.g., 'Equities', 'Cryptocurrency',
        'Currencies', etc.).

    Returns:
        tuple: A tuple containing the daily, weekly, and monthly ATR values in both
        percentage and absolute terms.
    """

    # For Equities and Cryptocurrency, calculate ATR as percentage of the closing price
    if asset_type in ('Equities', 'Cryptocurrency'):
        daily_atr_pct = (
            f"{(processed_df['ATR'].iloc[-1] / processed_df['close'].iloc[-1]) * 100:.2f}%"
        )
        weekly_atr_pct = (
            f"{(weekly_data['ATR'].iloc[-1] / weekly_data['close'].iloc[-1]) * 100:.2f}%"
        )
        monthly_atr_pct = (
            f"{(monthly_data['ATR'].iloc[-1] / monthly_data['close'].iloc[-1]) * 100:.2f}%"
        )

        # Absolute ATR for Equities and Cryptocurrency (value in dollars)
        daily_atr_abs = f"{processed_df['ATR'].iloc[-1]:.2f}"
        weekly_atr_abs = f"{weekly_data['ATR'].iloc[-1]:.2f}"
        monthly_atr_abs = f"{monthly_data['ATR'].iloc[-1]:.2f}"

    # For Forex (Currencies), calculate ATR in pips (smallest price movement)
    elif asset_type == 'Currencies':
        daily_atr_pct = (
            f"{(processed_df['ATR'].iloc[-1] / processed_df['close'].iloc[-1]) * 100:.3f}%"
        )
        weekly_atr_pct = (
            f"{(weekly_data['ATR'].iloc[-1] / weekly_data['close'].iloc[-1]) * 100:.3f}%"
        )
        monthly_atr_pct = (
            f"{(monthly_data['ATR'].iloc[-1] / monthly_data['close'].iloc[-1]) * 100:.3f}%"
        )

        # ATR for Forex converted to pips (100th of the smallest price movement)
        daily_atr_abs = f"{processed_df['ATR'].iloc[-1] * 100:.2f}"  # ATR in pips
        weekly_atr_abs = f"{weekly_data['ATR'].iloc[-1] * 100:.2f}"
        monthly_atr_abs = f"{monthly_data['ATR'].iloc[-1] * 100:.2f}"

    # For other asset types (Commodities, Bonds, etc.), treat similarly to Equities
    else:
        daily_atr_pct = (
            f"{(processed_df['ATR'].iloc[-1] / processed_df['close'].iloc[-1]) * 100:.2f}%"
        )
        weekly_atr_pct = (
            f"{(weekly_data['ATR'].iloc[-1] / weekly_data['close'].iloc[-1]) * 100:.2f}%"
        )
        monthly_atr_pct = (
            f"{(monthly_data['ATR'].iloc[-1] / monthly_data['close'].iloc[-1]) * 100:.2f}%"
        )

        # Absolute ATR for all asset types (value in dollars)
        daily_atr_abs = f"{processed_df['ATR'].iloc[-1]:.2f}"
        weekly_atr_abs = f"{weekly_data['ATR'].iloc[-1]:.2f}"
        monthly_atr_abs = f"{monthly_data['ATR'].iloc[-1]:.2f}"

    # Return ATR values as a tuple: percentage and absolute ATR for each time period
    return (
        daily_atr_pct, weekly_atr_pct, monthly_atr_pct,
        daily_atr_abs, weekly_atr_abs, monthly_atr_abs
    )

# -------------------------------------------------------------------------------------------------
# Function: calculate_probability_of_dpt
# Purpose: Estimate likelihood of achieving a defined profit threshold based on historical
# directional movement.
# Use Case: Asset Snapshot - DPT Probability (Market & Volatility module)
# -------------------------------------------------------------------------------------------------

# pylint: disable=too-many-locals
def calculate_probability_of_dpt(processed_df, column, direction,
desired_profit_target, filtered_df=None):
    """
    Calculate the probability of hitting the Desired Profit Target (DPT) based on the direction
    (Up or Down) and the selected timeline column.

    This function calculates the probability of achieving the desired profit target (DPT) by
    analyzing historical data, filtered based on the selected direction ('Up' or 'Down') and
    the chosen column representing the timeline of price changes (e.g., 'Interday').

    Parameters:
        processed_df (DataFrame): The processed data for the asset, containing price movements.
        column (str): The column to filter data based on ('Intraday', 'Interday', etc.).
        direction (str): The direction of the trade ('Up' or 'Down').
        desired_profit_target (float): The desired profit target as a percentage.
        filtered_df (DataFrame, optional): The filtered dataframe based on date
        range (default is None).

    Returns:
        tuple: A tuple containing the following values:
            - target_decimal (float): The decimal representation of the desired profit target.
            - occurrences (int): The number of times the desired profit target was achieved.
            - count (int): The total number of data points in the selected column.
            - probability (float): The probability of hitting the DPT.
            - rounded_probability (int): The rounded probability percentage.
            - probability_fraction (Fraction): The fraction representing the occurrences/count.
            - fraction_approx (Fraction): A simplified fraction with a denominator limit of 100.
            - approximate_readable (int): A more readable approximation of the probability.
    """
    # Convert DPT to decimal for filtering
    target_decimal = desired_profit_target / 100

    # Use filtered_df if provided, otherwise use the full processed_df
    data_to_use = filtered_df if filtered_df is not None else processed_df

    # Filter dataframe based on selected column and direction
    if direction == 'Up':
        dtp_filtered_data = data_to_use[data_to_use[column] >= target_decimal]
    elif direction == 'Down':
        dtp_filtered_data = data_to_use[data_to_use[column] <= -target_decimal]

    # Calculate occurrences of the DPT in the selected direction
    occurrences = len(dtp_filtered_data)
    count = data_to_use[column].count()

    # Calculate the probability of hitting the DPT
    probability = (occurrences / count) * 100
    rounded_probability = round(probability)

    # Create a Fraction for a more readable probability
    probability_fraction = Fraction(occurrences, count)

    # Approximate the fraction to make it easier to interpret, e.g., 661/2769 to 1 in 4
    approximate_fraction = occurrences / count

    # Calculate the "1 in X" representation for readability
    approximate_readable = round(1 / approximate_fraction) if approximate_fraction > 0 else 0

    # Limit the fraction to a maximum denominator of 100 for simplicity
    fraction_approx = Fraction(occurrences, count).limit_denominator(100)

    # Return all relevant values
    return (
        target_decimal, occurrences, count, probability, rounded_probability,
        probability_fraction, fraction_approx, approximate_readable
    )
