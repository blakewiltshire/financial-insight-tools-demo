# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------

"""
Use Case Indicators — Price Action and Trend Confirmation

This module provides grouped indicator logic for use cases related to:
- Short-Term Performance
- Trend and Momentum Confirmation
- Breakout and Mean Reversion Signals

Each section includes:
- Core signal computation functions
- Plaintext signal interpretation logic
- An indicator → function map used by dynamic app rendering

Indicator groups in this module:
- `options_performance_map` — performance metrics (returns, risk-adjusted returns, etc.)
- `options_trend_momentum_map` — trend structure, momentum strength, volume confirmation
- `options_breakout_mean_reversion_map` — volatility compression, Bollinger bands, breakout setups

This file is designed to be imported by main Streamlit app modules, typically:
- `/apps/trade_portfolio_structuring/pages/04_📊_Price_Action_and_Trend_Confirmation.py`
- Or any other module referencing these signal categories

File naming convention: `use_case_indicators_<domain>.py`
"""

# -------------------------------------------------------------------------------------------------
# Performance Indicators
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Winning vs. Losing
# - Rolling Returns
# - Volatility-Adjusted Returns
# - Net Price Movement
# - Momentum Score
# -------------------------------------------------------------------------------------------------

# --- Winning vs. Losing ---
def calculate_winning_losing_days(df, period=14):
    """
    Calculates Winning vs. Losing without applying predisposition.
    The logic for bullish/bearish confirmation happens in
    `04_📊_Price_Action_and_Trend_Confirmation.py`.
    """
    df = df.copy()
    df["Daily Change"] = df["close"].diff()

    # Rolling sum of positive & negative days
    df["Winning Days"] = df["Daily Change"].rolling(period).apply(lambda x: (x > 0).sum())
    df["Losing Days"] = df["Daily Change"].rolling(period).apply(lambda x: (x < 0).sum())

    return df

def determine_winning_losing_signal(df):
    """
    Returns the trend based on the number of winning/losing days.
    This function **does not** check predisposition—just trend strength.
    """
    win_days = df["Winning Days"].iloc[-1]
    lose_days = df["Losing Days"].iloc[-1]

    if win_days > lose_days:
        return "Confirmed Bullish Trend"
    if lose_days > win_days:
        return "Confirmed Bearish Trend"
    return "Mixed Signals Detected"

def wld(df, period=14):
    """
    Wrapper function for 'Winning vs. Losing'.

    Delegates to:
    - calculate_winning_losing_days
    - determine_winning_losing_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_winning_losing_days(df, period=period)
    return determine_winning_losing_signal(df)

# --- Rolling Returns ---
def calculate_rolling_returns(df, period=14):
    """
    Computes Rolling Returns over a given period.
    Rolling Return = (Current Price / Price N Days Ago) - 1
    """
    df = df.copy()
    df["Rolling Returns"] = df["close"].pct_change(periods=period) * 100  # Convert to percentage
    return df

def determine_rolling_returns_signal(df):
    """
    Determines the Rolling Returns signal, correctly mapping to predisposition.
    """
    last_return = df["Rolling Returns"].iloc[-1]

    if last_return > 0:
        return "Rolling Returns Uptrend"
    if last_return < 0:
        return "Rolling Returns Downtrend"
    return "Fluctuating"

def rr(df, period=14):
    """
    Wrapper function for 'Rolling Returns'.

    Delegates to:
    - calculate_rolling_returns
    - determine_rolling_returns_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_rolling_returns(df, period=period)
    return determine_rolling_returns_signal(df)

# --- Volatility-Adjusted Returns ---
def calculate_volatility_adjusted_returns(df, period=14):
    """
    Computes risk-adjusted returns based on historical volatility.
    Risk-Adjusted Return = Rolling Returns / Volatility
    """
    df = df.copy()

    # Ensure "Rolling Returns" exists before calculating "Risk-Adjusted Return"
    if "Rolling Returns" not in df.columns:
        df = calculate_rolling_returns(df, period=period)

    df["Volatility"] = df["close"].rolling(period).std()

    # Avoid division errors if volatility is zero
    df["Risk-Adjusted Return"] = df["Rolling Returns"] / df["Volatility"].replace(0, float("nan"))

    return df

def determine_volatility_adjusted_signal(df):
    """
    Determines the Volatility-Adjusted Returns signal, correctly mapping to predisposition.
    """
    last_adjusted = df["Risk-Adjusted Return"].iloc[-1]

    if last_adjusted > 1.5:
        return "Volatility-Adjusted Uptrend"
    if last_adjusted < 0.5:
        return "Volatility-Adjusted Downtrend"
    return "Moderate Risk-Adjusted Returns"

def volatility_adjusted_returns(df, period=14):
    """
    Wrapper function for 'Volatility-Adjusted Returns'.

    Delegates to:
    - calculate_volatility_adjusted_returns
    - determine_volatility_adjusted_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_volatility_adjusted_returns(df, period=period)
    return determine_volatility_adjusted_signal(df)

# --- Net Price Movement ---
def calculate_net_price_movement(df, period=14):
    """
    Computes the net percentage price movement over the specified period.
    """
    df = df.copy()
    df["Net Price Movement"] = ((df["close"] - df["close"].shift(period)) / df["close"].shift(
    period)) * 100
    return df

def determine_net_price_movement_signal(df):
    """
    Determines the Net Price Movement signal without directly using predisposition.
    The predisposition logic is applied externally via `predisposition_map`.
    """
    last_movement = df["Net Price Movement"].iloc[-1]

    if last_movement > 0:
        return "Positive Net Price Movement"
    if last_movement < 0:
        return "Negative Net Price Movement"

    return "Mixed Signals Detected"

def net_price_movement(df, period=14):
    """
    Wrapper function for 'Net Price Movement'.

    Delegates to:
    - calculate_net_price_movement
    - determine_net_price_movement_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_net_price_movement(df, period=period)
    return determine_net_price_movement_signal(df)

# --- Momentum Score ---
def calculate_momentum_score(df, period=14):
    """
    Computes Momentum Score by normalizing cumulative momentum over X periods.
    """
    df = df.copy()

    df["Net Price Movement"] = df["close"].diff(periods=period)

    # Normalize by max movement over the period
    max_movement = df["Net Price Movement"].abs().rolling(period).max()

    df["Momentum Score"] = df["Net Price Movement"] / max_movement.replace(0, float("nan"))

    return df

def determine_momentum_signal(df):
    """
    Determines the momentum signal based on predefined thresholds.
    """
    last_momentum = df["Momentum Score"].iloc[-1]

    if last_momentum > 0.5:
        return "Strong Bullish Momentum"
    if last_momentum > 0.2:
        return "Mild Bullish Momentum"
    if last_momentum < -0.5:
        return "Strong Bearish Momentum"
    if last_momentum < -0.2:
        return "Mild Bearish Momentum"
    return "Mixed Signals"

def momentum_score(df, period=14):
    """
    Wrapper function for 'Momentum Score'.

    Delegates to:
    - calculate_momentum_score
    - determine_momentum_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_momentum_score(df, period=period)
    return determine_momentum_signal(df)

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_performance_map = {
    "Winning vs. Losing": wld,
    "Rolling Returns": rr,
    "Volatility-Adjusted Returns": volatility_adjusted_returns,
    "Momentum Score": momentum_score,
    "Net Price Movement": net_price_movement
}
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# Trend & Momentum Indicators
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Price Rate of Change (ROC)
# - Price Action Momentum
# - Trend Confirmation (Higher Highs / Lower Lows)
# - Momentum Strength
# - Price Acceleration
# - Volume-Based Confirmation
# - Support/Resistance Validation
# -------------------------------------------------------------------------------------------------

# --- Price Rate of Change (ROC) ---
def calculate_proc(df, period=14):
    """
    Computes Price Rate of Change (ROC).
    ROC = ((Current Close - Close N periods ago) / Close N periods ago) * 100
    """
    df["ROC"] = (df["close"].diff(periods=period) / df["close"].shift(periods=period)) * 100
    return df

def determine_proc_signal(df):
    """Determines Price Rate of Change signal based on thresholds."""
    last_roc = df["ROC"].iloc[-1]

    if last_roc > 5:
        return "Strong Uptrend"
    if last_roc > 1:
        return "Weak Uptrend"
    if -1 < last_roc < 1:
        return "Flat/Neutral"
    if -5 < last_roc < -1:
        return "Weak Downtrend"
    return "Strong Downtrend"

def proc(df, proc_period=14):
    """
    Wrapper function for 'Price Rate of Change (ROC)'.

    Delegates to:
    - calculate_proc
    - determine_proc_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_proc(df, period=proc_period)
    return determine_proc_signal(df)

# --- Price Action Momentum (PAM) ---
def calculate_pam(df, period=14):
    """
    Computes Price Action Momentum (PAM).
    PAM = Close Price - Close Price N periods ago
    """
    df["Momentum"] = df["close"] - df["close"].shift(periods=period)
    return df

def determine_pam_signal(df):
    """Determines Price Action Momentum signal based on thresholds."""
    last_momentum = df["Momentum"].iloc[-1]

    if last_momentum > 5:
        return "Accelerating Uptrend"
    if last_momentum > 1:
        return "Slowing Uptrend"
    if -1 < last_momentum < 1:
        return "Decelerating Move"
    if -5 < last_momentum < -1:
        return "Slowing Downtrend"
    return "Accelerating Downtrend"

def pam(df, pam_period=14):
    """
    Wrapper function for 'Price Action Momentum (PAM)'.

    Delegates to:
    - calculate_pam
    - determine_pam_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_pam(df, period=pam_period)
    return determine_pam_signal(df)

# --- Trend Confirmation (Higher Highs / Lower Lows) ---
def calculate_tc(df, period=14):
    """
    Identifies Higher Highs and Lower Lows for Trend Confirmation.
    """
    df["Higher Highs"] = df["high"] > df["high"].shift(periods=period)
    df["Lower Lows"] = df["low"] < df["low"].shift(periods=period)
    return df

def determine_tc_signal(df):
    """Determines Trend Confirmation signal."""
    last_higher_highs = df["Higher Highs"].iloc[-1]
    last_lower_lows = df["Lower Lows"].iloc[-1]

    if last_higher_highs and last_lower_lows:
        return "Range-Bound"
    if last_higher_highs:
        return "Higher Highs & Higher Lows"
    if last_lower_lows:
        return "Lower Highs & Lower Lows"
    return "No Clear Trend Signal"

def tc(df, tc_period=14):
    """
    Wrapper function for 'Trend Confirmation (Higher Highs / Lower Lows)'.

    Delegates to:
    - calculate_tc
    - determine_tc_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_tc(df, period=tc_period)
    return determine_tc_signal(df)

# --- Momentum Strength ---
def calculate_momentum_strength(df, period=14):
    """
    Computes Momentum Strength.
    Momentum Strength = Close Price - Close Price N periods ago
    """
    df["Momentum Strength"] = df["close"] - df["close"].shift(periods=period)
    return df

def determine_momentum_strength_signal(df):
    """Determines Momentum Strength signal based on thresholds."""
    last_momentum = df["Momentum Strength"].iloc[-1]

    if last_momentum > 5:
        return "Strong Momentum"
    if last_momentum > 1:
        return "Moderate Momentum"
    return "Weak Momentum"

def ms(df, period=14):
    """
    Wrapper function for 'Momentum Strength'.

    Delegates to:
    - calculate_momentum_strength
    - determine_momentum_strength_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_momentum_strength(df, period=period)
    return determine_momentum_strength_signal(df)

# --- Price Acceleration ---
def calculate_price_acceleration(df, period=5):
    """
    Computes Price Acceleration.
    Price Acceleration = Momentum Strength - Momentum Strength N periods ago
    """
    # Ensure Momentum Strength is calculated first
    if "Momentum Strength" not in df.columns:
        df = calculate_momentum_strength(df, period=14)  # Default period for Momentum Strength

    df["Price Acceleration"] = df["Momentum Strength"] - df["Momentum Strength"].shift(
    periods=period)
    return df

def determine_price_acceleration_signal(df):
    """Determines Price Acceleration signal based on thresholds."""
    last_acceleration = df["Price Acceleration"].iloc[-1]

    if last_acceleration > 5:
        return "Rapid Upside Move"
    if last_acceleration < -5:
        return "Rapid Downside Move"
    return "Decelerating Move"

def pa(df, period=5):
    """
    Wrapper function for 'Price Acceleration'.

    Delegates to:
    - calculate_price_acceleration
    - determine_price_acceleration_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_price_acceleration(df, period=period)
    return determine_price_acceleration_signal(df)

# --- Volume-Based Confirmation Calculation ---
def calculate_volume_based_confirmation(df, period=14):
    """
    Determines if price movements are supported by volume trends.

    - High Volume Breakout: Large price movement accompanied by high volume.
    - Low Volume Move: Price movement with low volume, suggesting weak conviction.
    - Divergence Detected: Price and volume trending in opposite directions.
    """
    df = df.copy()
    df["Volume_MA"] = df["volume"].rolling(period).mean()  # Moving Average of Volume
    df["Price_Change"] = df["close"].pct_change(period)  # Percentage Price Change
    df["Volume_Change"] = df["volume"].pct_change(period)  # Percentage Volume Change

    return df

def determine_volume_confirmation_signal(df):
    """
    Determines the volume-based confirmation signal.
    """
    last_price_change = df["Price_Change"].iloc[-1]
    last_volume_change = df["Volume_Change"].iloc[-1]

    if abs(last_price_change) > 0.02 and last_volume_change > 0.20:
        return "High Volume Breakout"

    if abs(last_price_change) > 0.02 and last_volume_change < 0.05:
        return "Low Volume Move"

    if (last_price_change > 0 > last_volume_change) or (
    last_price_change < 0 < last_volume_change):
        return "Divergence Detected"

    return "Stable Volume Confirmation"


def vbc(df, period=14):
    """
    Wrapper function for 'Volume-Based Confirmation'.

    Delegates to:
    - calculate_volume_based_confirmation
    - determine_volume_confirmation_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_volume_based_confirmation(df, period=period)
    return determine_volume_confirmation_signal(df)

# --- Support/Resistance Validation ---
def calculate_support_resistance(df, lookback=5):
    """
    Identifies support and resistance levels based on past highs and lows.

    - Support: The lowest price within the last `lookback` periods.
    - Resistance: The highest price within the last `lookback` periods.
    """
    df["Support Level"] = df["low"].rolling(window=lookback).min()
    df["Resistance Level"] = df["high"].rolling(window=lookback).max()
    return df

def determine_support_resistance_signal(df):
    """Determines support/resistance validation signals."""
    last_close = df["close"].iloc[-1]
    last_support = df["Support Level"].iloc[-1]
    last_resistance = df["Resistance Level"].iloc[-1]

    if last_close > last_resistance:
        return "Breakout Confirmed"
    if last_close < last_support:
        return "Failed Breakout"
    if abs(last_close - last_support) < 0.02 * last_support:
        return "Support Holding"
    if abs(last_close - last_resistance) < 0.02 * last_resistance:
        return "Resistance Holding"

    return "No Clear Support/Resistance Signal"

def srv(df, lookback=5):
    """
    Wrapper function for 'Support/Resistance Validation'.

    Delegates to:
    - calculate_support_resistance
    - determine_support_resistance_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_support_resistance(df, lookback=lookback)
    return determine_support_resistance_signal(df)

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_trend_momentum_map = {
    "Price Rate of Change": proc,
    "Price Action Momentum": pam,
    "Trend Confirmation (Higher Highs / Lower Lows)": tc,
    "Momentum Strength": ms,
    "Price Acceleration": pa,
    "Volume-Based Confirmation": vbc,
    "Support/Resistance Validation": srv
}


# -------------------------------------------------------------------------------------------------
# Breakout & Mean Reversion Indicators
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Bollinger Band Expansion
# - Price Breakout vs. Mean Reversion
# - ATR Volatility Trends
# - Standard Deviation of Price Swings
# - Volume vs. Price Range Compression
# -------------------------------------------------------------------------------------------------

# --- Bollinger Band Expansion ---
def calculate_bollinger_band_expansion(df, period=20):
    """
    Computes Bollinger Bands and determines expansion/contraction.

    - Expanding Bands: Increased volatility—watch for breakout.
    - Contracting Bands: Decreasing volatility—possible mean reversion or breakout setup.
    """
    df["BB_Mid"] = df["close"].rolling(window=period).mean()
    df["BB_Upper"] = df["BB_Mid"] + (df["close"].rolling(window=period).std() * 2)
    df["BB_Lower"] = df["BB_Mid"] - (df["close"].rolling(window=period).std() * 2)
    df["BB_Width"] = df["BB_Upper"] - df["BB_Lower"]

    df["BB_Width_Change"] = df["BB_Width"].pct_change()

    return df

def determine_bollinger_band_signal(df):
    """Determines whether Bollinger Bands are expanding or contracting."""
    last_change = df["BB_Width_Change"].iloc[-1]

    if last_change > 0.05:
        return "Expanding Bands"
    if last_change < -0.05:
        return "Contracting Bands"

    return "No Significant Change"

def bbe(df, period=20):
    """
    Wrapper function for 'Bollinger Band Expansion'.

    Delegates to:
    - calculate_bollinger_band_expansion
    - determine_bollinger_band_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_bollinger_band_expansion(df, period=period)
    return determine_bollinger_band_signal(df)

# --- Price Breakout vs. Mean Reversion ---
def calculate_price_breakout_mean_reversion(df, period=20):
    """
    Identifies price breakouts or mean reversion setups.

    - Breakout Above Resistance: Strong buying pressure—bullish breakout confirmed.
    - Breakout Below Support: Strong selling pressure—bearish breakout confirmed.
    - Mean Reversion Setup: Price returning to the mean—potential trading opportunity.
    """
    df["BB_Mid"] = df["close"].rolling(window=period).mean()
    df["BB_Upper"] = df["BB_Mid"] + (df["close"].rolling(window=period).std() * 2)
    df["BB_Lower"] = df["BB_Mid"] - (df["close"].rolling(window=period).std() * 2)

    return df

def determine_price_breakout_mean_reversion_signal(df):
    """Determines whether price action indicates a breakout or mean reversion."""
    last_close = df["close"].iloc[-1]
    last_upper = df["BB_Upper"].iloc[-1]
    last_lower = df["BB_Lower"].iloc[-1]
    last_mid = df["BB_Mid"].iloc[-1]

    if last_close > last_upper:
        return "Breakout Above Resistance"
    if last_close < last_lower:
        return "Breakout Below Support"
    if abs(last_close - last_mid) < 0.02 * last_mid:
        return "Mean Reversion Setup"

    return "No Clear Breakout or Reversion"

def pbmr(df, period=20):
    """
    Wrapper function for 'Price Breakout vs. Mean Reversion'.

    Delegates to:
    - calculate_price_breakout_mean_reversion
    - determine_price_breakout_mean_reversion_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_price_breakout_mean_reversion(df, period=period)
    return determine_price_breakout_mean_reversion_signal(df)

# --- ATR Volatility Trends ---
def calculate_atr_volatility_trends(df, period=14):
    """
    Computes ATR (Average True Range) to assess volatility trends.

    - Increasing ATR: High volatility detected—expect larger price swings.
    - Decreasing ATR: Low volatility—potential consolidation or range-bound movement.
    """
    df["High-Low"] = df["high"] - df["low"]
    df["High-Close"] = abs(df["high"] - df["close"].shift())
    df["Low-Close"] = abs(df["low"] - df["close"].shift())

    df["TR"] = df[["High-Low", "High-Close", "Low-Close"]].max(axis=1)
    df["ATR"] = df["TR"].rolling(window=period).mean()

    df["ATR_Change"] = df["ATR"].pct_change()

    return df

def determine_atr_volatility_signal(df):
    """Determines whether ATR is increasing or decreasing."""
    last_change = df["ATR_Change"].iloc[-1]

    if last_change > 0.05:
        return "Increasing ATR"
    if last_change < -0.05:
        return "Decreasing ATR"

    return "Stable ATR"

def atrvt(df, period=14):
    """
    Wrapper function for 'ATR Volatility Trends'.

    Delegates to:
    - calculate_atr_volatility_trends
    - determine_atr_volatility_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_atr_volatility_trends(df, period=period)
    return determine_atr_volatility_signal(df)

# --- Standard Deviation of Price Swings ---
def calculate_standard_deviation_swings(df, period=20):
    """
    Computes the standard deviation of price swings.

    - High Volatility: Significant price swings detected—trend strength or uncertainty increasing.
    - Low Volatility: Price action stabilizing—trend exhaustion or consolidation ahead.
    """
    df["Price_Change_Std"] = df["close"].rolling(window=period).std()

    return df

def determine_standard_deviation_signal(df):
    """Determines volatility based on standard deviation of price swings."""
    last_std = df["Price_Change_Std"].iloc[-1]
    mean_std = df["Price_Change_Std"].mean()

    if last_std > 1.2 * mean_std:
        return "High Volatility"
    if last_std < 0.8 * mean_std:
        return "Low Volatility"

    return "Moderate Volatility"

def sdps(df, period=20):
    """
    Wrapper function for 'Standard Deviation of Price Swings'.

    Delegates to:
    - calculate_standard_deviation_swings
    - determine_standard_deviation_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_standard_deviation_swings(df, period=period)
    return determine_standard_deviation_signal(df)

# --- Volume vs. Price Range Compression ---
def calculate_volume_price_range_compression(df, period=20):  # pylint: disable=unused-argument
    """
    Analyzes volume trends and price range compression.

    - Decreasing Volume & Range: Tightening price action with low volume—watch for breakout.
    - Increasing Volume & Range: Expanding range with volume surge—high conviction price move.
    """
    df["Price_Range"] = df["high"] - df["low"]
    df["Price_Range_Change"] = df["Price_Range"].pct_change()
    df["Volume_Change"] = df["volume"].pct_change()

    return df

def determine_volume_price_range_signal(df):
    """Determines whether volume and price range are compressing or expanding."""
    last_range_change = df["Price_Range_Change"].iloc[-1]
    last_volume_change = df["Volume_Change"].iloc[-1]

    if last_range_change < -0.05 and last_volume_change < -0.05:
        return "Decreasing Volume & Range"
    if last_range_change > 0.05 and last_volume_change > 0.05:
        return "Increasing Volume & Range"

    return "Stable Volume & Price Range"

def vprc(df, period=20):
    """
    Wrapper function for 'Volume vs. Price Range Compression'.

    Delegates to:
    - calculate_volume_price_range_compression
    - determine_volume_price_range_signal

    Returns:
        str: Interpreted signal description.
    """
    df = calculate_volume_price_range_compression(df, period=period)
    return determine_volume_price_range_signal(df)

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_breakout_mean_reversion_map = {
    "Bollinger Band Expansion": bbe,
    "Price Breakout vs. Mean Reversion": pbmr,
    "ATR Volatility Trends": atrvt,
    "Standard Deviation of Price Swings": sdps,
    "Volume vs. Price Range Compression": vprc
}
# -------------------------------------------------------------------------------------------------
