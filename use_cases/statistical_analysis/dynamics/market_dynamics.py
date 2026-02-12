# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module contains functions for analysing market dynamics through various volatility and risk
metrics, such as the Volatility Ratio and Average True Range (ATR). These metrics are essential for
understanding price volatility, market patterns, and potential opportunities in financial markets.

Functions in this module include:
- `volatility_ratio`: Calculates the Volatility Ratio by comparing the price range (high - low)
  to the low price for a given timeframe. This ratio helps assess market volatility and
  price patterns.
- `average_true_range`: Calculates the Average True Range (ATR), a measure of price volatility
  that considers gaps and limit moves. It provides insights into market conditions and
  price fluctuations.

These functions enable users to evaluate market conditions and make informed decisions
based on volatility analysis.

Example usage:
    from market_dynamics import volatility_ratio, average_true_range

    volatility_ratio(df, 'column_name')
    average_true_range(df, 'column_name', 'Equities')
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Function: volatility_ratio
# Purpose: Evaluates relative price movement by comparing the daily high-low range to the low price,
# highlighting compression, expansion, and market tension signals.
# Use Case: Statistical Analysis / Market Dynamics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def volatility_ratio(processed_df, column):
    """
    Calculate and display the Volatility Ratio, which is used to measure market volatility
    by comparing the price range (high - low) to the low price for a given timeframe.

    Parameters:
    - processed_df (pd.DataFrame): The dataframe with price data.
    - column (str): Expected to be 'Interday'.

    Returns:
    - dict or None: Summary statistics in dictionary form, or None if inapplicable.
    """

    st.write('You have selected: Volatility Ratio — A measure used to identify price \
    patterns and volatility.')

    if column != 'Interday':
        st.info("Volatility Ratio can only be applied to the 'Interday' timeline.")
        return None

    # Calculate volatility ratio
    processed_df['Volatility_Ratio'] = (
        (processed_df['high'] - processed_df['low']) / processed_df['low']
    )

    # Basic stats
    max_volatility = processed_df['Volatility_Ratio'].max()
    avg_volatility = processed_df['Volatility_Ratio'].mean()

    st.write(f"Maximum Volatility Ratio: {max_volatility:.2f}")
    st.write(f"Average Volatility Ratio: {avg_volatility:.2f}")

    st.dataframe(processed_df[['date', 'high', 'low', 'Volatility_Ratio']].dropna())

    st.caption("Volatility ratio provides insights into price patterns and \
    potential market opportunities.")

    # ✅ Return JSON snapshot block
    return {
        "average_volatility_ratio": round(avg_volatility, 4),
        "maximum_volatility_ratio": round(max_volatility, 4)
    }

# -------------------------------------------------------------------------------------------------
# Function: average_true_range
# Purpose: Measures absolute and percentage price volatility over a configurable period,
# offering a dynamic view of market movement intensity across asset types.
# Use Case: Statistical Analysis / Market Dynamics (Market & Volatility module)
# -------------------------------------------------------------------------------------------------
def average_true_range(filtered_df, column, asset_type='Equities'):
    """
    Dynamically calculate and display the Average True Range (ATR) for a selected asset type
    based on the filtered data and selected period, including a volatility rating.

    Parameters:
    - filtered_df (pd.DataFrame): The filtered dataframe containing financial data.
    - column (str): The column name containing the volatility metric ('Interday').
    - asset_type (str): The type of asset (e.g., 'Equities', 'Cryptocurrency', etc.).

    Returns:
    - dict or None: ATR snapshot result for export if applicable, otherwise None.
    """

    st.write('You have selected: ATR (Average True Range) — A measure of price volatility.')

    # Slider for selecting period
    period = st.sidebar.slider('Select Period for ATR Calculation', min_value=1,
                               max_value=365, value=14, step=1)

    st.write(f"You have chosen a window of {period} days for ATR calculation.")

    if column != 'Interday':
        st.error("Please select the correct 'Interday' timeframe for Average True Range.")
        return None

    # Calculate the components of True Range
    filtered_df['High_Low'] = filtered_df['high'] - filtered_df['low']
    filtered_df['High_Close'] = abs(filtered_df['high'] - filtered_df['close'].shift(1))
    filtered_df['Low_Close'] = abs(filtered_df['low'] - filtered_df['close'].shift(1))

    filtered_df['True_Range'] = filtered_df[['High_Low', 'High_Close', 'Low_Close']].max(axis=1)

    filtered_df['ATR'] = filtered_df['True_Range'].rolling(window=period).mean()
    daily_atr = filtered_df['ATR'].iloc[-1]
    latest_close = filtered_df['close'].iloc[-1]

    # Protect against division by zero or NaNs
    if pd.isna(daily_atr) or pd.isna(latest_close) or latest_close == 0:
        st.warning("ATR or close price could not be calculated. Please check the data.")
        return None

    # Compute values
    atr_pct_value = (daily_atr / latest_close) * 100
    atr_abs_value = daily_atr

    # Display based on asset type
    if asset_type == 'Currencies':
        atr_pct_display = f"{atr_pct_value:.3f}%"
        atr_abs_display = f"{atr_abs_value * 100:.2f}"  # pips
    else:
        atr_pct_display = f"{atr_pct_value:.2f}%"
        atr_abs_display = f"{atr_abs_value:.2f}"

    # Volatility rating
    if daily_atr <= 0.02:
        atr_rating = "Low"
    elif 0.02 < daily_atr <= 0.05:
        atr_rating = "Medium"
    else:
        atr_rating = "High"

    # Display
    st.write(f"**ATR (Percentage):** {atr_pct_display}")
    st.write(f"**ATR (Absolute):** {atr_abs_display}")
    st.write(f"**ATR Volatility Rating:** {atr_rating}")

    # ✅ Return JSON snapshot block
    return {
        "atr_period_days": period,
        "atr_value": round(atr_abs_value, 6),
        "atr_percent_of_price": round(atr_pct_value, 4),
        "atr_volatility_rating": atr_rating
    }

# -------------------------------------------------------------------------------------------------
# Market Dynamics Function Mapping
# -------------------------------------------------------------------------------------------------
options_market_dynamics_map = {
    'Volatility Ratio': volatility_ratio,
    'ATR (Average True Range)': average_true_range
    # map other options to their corresponding functions here...
}
