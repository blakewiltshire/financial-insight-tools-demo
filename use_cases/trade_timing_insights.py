# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# W0613 — Unused arguments (timeframe, predisposition):
# retained for use in app-level logic or AI augmentation
# -------------------------------------------------------------------------------------------------
# pylint: disable=unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Insight Generator — Trade Timing and Confirmation

Provides narrative signal interpretation for Trade Timing and Confirmation indicators.

This module returns pre-defined qualitative insights for each indicator signal, supporting
structured messaging across DSS modules and enabling future integration with AI personas,
trade summaries, or narrative generators.

Arguments like `timeframe` and `predisposition` are not currently used directly, but are
passed in to allow for contextual routing and expansion within the broader system.
"""

def generate_insights(indicator, value, timeframe, predisposition):
    """
    Provides detailed insight statements based on the indicator value, timeframe,
    and trade predisposition.

    Parameters:
    - indicator (str): The technical indicator used (e.g., 'ADX', 'RSI', 'ATR')
    - value (float/int): The computed value of the indicator
    - timeframe (str): The timeframe applied (e.g., 'Intraday', 'Daily', 'Weekly', 'Monthly')
    - predisposition (str): The user's chosen trade direction ('Bullish' or 'Bearish')

    Returns:
    - str: The insight statement relevant to the indicator, value, and timeframe
    """

    insights = {
# -------------------------------------------------------------------------------------------------
# --- Trend Confirmation ---
# -------------------------------------------------------------------------------------------------
        "Trend Signal": {  # "Trend Signal" key must exist for code to run correctly.
            "Bullish": "Trend is strong and aligns with bullish predisposition.",
            "Bearish": "Trend suggests bearish sentiment. Confirm with other indicators.",
            "Neutral": "Trend is unclear—consider waiting for confirmation.",
        },
        "Support/Resistance Validation": {
            "Support Holding": "Price rebounding from support—buying interest confirmed.",
            "Resistance Holding": "Price rejecting resistance—selling pressure confirmed.",
            "Breakout Confirmed": "Price breaking past key level with volume—trend continuation.",
            "Failed Breakout": "False breakout—traders trapped, possible reversal.",
        },
        "Average Directional Index": {
            "Strong Trend":
            "Trend strength confirmed (ADX > 25). High conviction for trend continuation.",
            "Moderate Trend":
            "ADX is between 20-25. Trend is forming but needs further confirmation.",
            "Minimal Trend":
            "ADX below 20—trend is weak or non-existent. "
            "Confirm with price action before execution.",
        },
        "Parabolic SAR": {
            "Bullish": "Price is above the Parabolic SAR—strong uptrend continuation signal.",
            "Bearish": "Price is below the Parabolic SAR—downtrend in progress.",
            "Neutral": "Price hovering near SAR—trend confirmation required."
        },
        "Simple Moving Average": {
            "Confirmed Trend": "Moving averages show consistent directional trend.",
            "Indecisive": "MAs are close—trend confirmation required."
        },
        "Exponential Moving Average": {
            "Confirmed Trend": "EMA confirms trend strength over shorter periods.",
            "Indecisive": "EMA fluctuations indicate indecisive market conditions."
        },
        "Super Trend": {
            "Trend Confirmed": "Super Trend confirms a strong trend presence.",
            "Indecisive": "Super Trend is fluctuating—trend confirmation required."
        },

# -------------------------------------------------------------------------------------------------
# --- Momentum & Strength ---
# -------------------------------------------------------------------------------------------------
        "Relative Strength Index": {
            "Overbought":
            "RSI > 80. Extreme buying pressure detected. Risk of reversal or pullback.",
            "Overextended Overbought":
            "RSI between 70-80. Uptrend may be losing momentum. Monitor for potential "
            "pullbacks or consolidation.",
            "Oversold":
            "RSI < 20. Extreme selling pressure detected. Potential reversal zone but "
            "needs confirmation.",
            "Deeply Oversold":
            "RSI between 20-30. Downtrend exhaustion possible. Watch for recovery signals.",
            "Neutral": "RSI between 40-60. No strong momentum signal; market remains indecisive.",
        },
        "Moving Average Convergence Divergence": {
            "Bullish Crossover":
            "MACD Line crossed above Signal Line, suggesting increasing bullish momentum. "
            "Confirm with volume and trend strength.",
            "Bearish Crossover":
            "MACD Line crossed below Signal Line, indicating weakening momentum. "
            "Monitor price action and trend confirmation.",
            "Weak Signal":
            "MACD near zero—momentum remains weak. Trend confirmation is needed before "
            "drawing conclusions.",
        },
        "Chande Momentum Oscillator": {
            "Strong Momentum": "CMO confirms price movement with strong conviction.",
            "Neutral": "CMO does not indicate strong momentum—trend is unclear."
        },
        "Money Flow Index": {
            "Strong Buying/Selling Pressure": "MFI indicates significant volume-driven movement.",
            "Neutral": "MFI does not confirm strong buying or selling pressure."
        },

# -------------------------------------------------------------------------------------------------
# --- Volatility & Risk ---
# -------------------------------------------------------------------------------------------------
        "Bollinger Bands": {
            "Breakout":
            "Price breaking upper/lower band—high volatility & trend continuation likely.",
            "Squeeze": "Bands contracting—watch for breakout opportunities.",
            "Mean Reversion": "Price reverting to mid-band—trend losing strength.",
        },
        "Average True Range": {
            "High Volatility": "ATR increasing—expect larger price swings & risk.",
            "Low Volatility": "ATR decreasing—market stabilizing, reduced trading opportunity.",
        },
        "Standard Deviation": {
            "High Volatility":
            "Standard Deviation above average—market experiencing higher-than-normal volatility.",
            "Low Volatility":
            "Standard Deviation below average—market experiencing lower-than-normal volatility.",
        },

# -------------------------------------------------------------------------------------------------
# --- Volume Confirmation ---
# -------------------------------------------------------------------------------------------------
        "On-Balance Volume": {
            "Volume Confirming Trend": "OBV rising with price—strong trend confirmation.",
            "Divergence": "Price rising but OBV falling—trend may be losing strength.",
        },
        "Accumulation/Distribution Line": {
            "Accumulation—Buying Pressure":
            "A/D Line rising—volume supporting upward price movement.",
            "Distribution—Selling Pressure":
            "A/D Line falling—volume supporting downward price movement.",
            "Neutral": "No clear volume shift detected—market remains indecisive."
        },

# -------------------------------------------------------------------------------------------------
# --- Pattern Recognition ---
# -------------------------------------------------------------------------------------------------
        "Candlestick Patterns": {
            "Bullish Engulfing": "Strong buying pressure—potential reversal to the upside.",
            "Bearish Engulfing": "Selling pressure increasing—watch for downside confirmation.",
            "Doji": "Indecision in the market—wait for confirmation.",
        },
        "Head & Shoulders": {
            "Bearish": "Confirmed breakdown—trend reversal likely.",
            "Invalidation": "Pattern failed to break neckline—trend may continue.",
        },
        "Flags & Pennants": {
            "Bullish": "Price consolidating in an uptrend—watch for breakout continuation.",
            "Bearish": "Downtrend flag forming—breakout lower likely.",
        },
        "Double Tops/Bottoms": {
            "Confirmed Reversal": "Break of neckline confirms reversal—trend changing direction.",
            "False Breakout": "Failed breakdown—trend may continue in prior direction.",
        }

    }

    return insights[indicator].get(value, "No clear insight available for this scenario.")
