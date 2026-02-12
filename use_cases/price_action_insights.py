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
Insight Generator — Price Action and Trend Confirmation

Provides narrative signal interpretation for Price Action indicators.

This module returns pre-defined qualitative insights for each indicator signal, supporting
structured messaging across DSS modules and enabling future integration with AI personas,
trade summaries, or narrative generators.

Arguments like `timeframe` and `predisposition` are not currently used directly, but are
passed in to allow for contextual routing and expansion within the broader system.
"""

# -------------------------------------------------------------------------------------------------
# Function: generate_insights
# Purpose: Return a narrative interpretation string based on indicator signal classification
# -------------------------------------------------------------------------------------------------
def generate_insights(indicator, value, timeframe, predisposition):
    """
    Provides detailed insight statements based on the indicator value, timeframe, and trade predisposition.

    Parameters:
    - indicator (str): (e.g., 'Rolling Returns', 'Price Acceleration')
    - value (float/int): The computed value of the indicator
    - timeframe (str): The timeframe applied (e.g., 'Intraday', 'Daily', 'Weekly', 'Monthly')
    - predisposition (str): The user's chosen trade direction ('Bullish' or 'Bearish')

    Returns:
    - str: The insight statement relevant to the indicator, value, and timeframe
    """

    insights = {
# -------------------------------------------------------------------------------------------------
# Performance Insights
# -------------------------------------------------------------------------------------------------
        "Winning vs. Losing": {
            "Confirmed Bullish Trend":
            "Winning days dominate—momentum favours bullish direction.",
            "Confirmed Bearish Trend":
            "Losing days dominate—bearish pressure likely to persist.",
            "Mixed Signals Detected":
            "No dominant trend—market appears indecisive.",
        },
        "Rolling Returns": {
            "Rolling Returns Uptrend":
            "Sustained positive returns signal upward momentum.",
            "Fluctuating":
            "Returns oscillate—no clear directional bias.",
            "Rolling Returns Downtrend":
            "Consistently negative returns indicate persistent selling pressure.",
        },
        "Volatility-Adjusted Returns": {
            "Volatility-Adjusted Uptrend":
            "Returns strong relative to risk—favourable bullish environment.",
            "Moderate Risk-Adjusted Returns":
            "Neutral risk-return conditions—no signal confirmation.",
            "Volatility-Adjusted Downtrend":
            "Returns weak relative to volatility—bearish risk signal.",
        },
        "Net Price Movement": {
            "Positive Net Price Movement":
            "Cumulative price action supports a bullish thesis.",
            "Negative Net Price Movement":
            "Cumulative price action aligns with bearish conditions.",
            "Mixed Signals Detected":
            "Price direction inconclusive over selected period.",
        },
        "Momentum Score": {
            "Strong Bullish Momentum":
            "Momentum signals strong upside conviction.",
            "Mild Bullish Momentum":
            "Early signs of upward momentum—confirmation required.",
            "Mixed Signals":
            "Momentum profile lacks clarity.",
            "Mild Bearish Momentum":
            "Initial signs of downward momentum—requires confirmation.",
            "Strong Bearish Momentum":
            "Momentum indicates clear bearish direction.",
        },

# -------------------------------------------------------------------------------------------------
# Trend & Momentum Insights
# -------------------------------------------------------------------------------------------------
        "Price Rate of Change": {
            "Strong Uptrend":
            "Price rising rapidly—momentum favours bulls.",
            "Weak Uptrend":
            "Mild upward movement—trend lacks conviction.",
            "Flat/Neutral":
            "Price stable—no active directional bias.",
            "Weak Downtrend":
            "Gradual decline—potential bearish setup forming.",
            "Strong Downtrend":
            "Price falling sharply—bearish momentum dominant.",
        },
        "Price Action Momentum": {
            "Accelerating Uptrend":
            "Momentum building—bullish continuation favoured.",
            "Slowing Uptrend":
            "Momentum waning—trend exhaustion possible.",
            "Decelerating Move":
            "Momentum stabilising—neutral signal.",
            "Slowing Downtrend":
            "Bearish move losing steam—reversal risk increasing.",
            "Accelerating Downtrend":
            "Momentum intensifying to the downside—bearish signal strengthened.",
        },
        "Trend Confirmation (Higher Highs / Lower Lows)": {
            "Higher Highs & Higher Lows":
            "Classic uptrend structure confirmed.",
            "Lower Highs & Lower Lows":
            "Classic downtrend structure confirmed.",
            "Range-Bound":
            "Lateral movement—consolidation or distribution phase likely.",
        },
        "Momentum Strength": {
            "Strong Momentum":
            "Momentum supports continuation of current trend.",
            "Moderate Momentum":
            "Momentum present, but conviction is limited.",
            "Weak Momentum":
            "Weak movement—reversal or pause likely.",
        },
        "Price Acceleration": {
            "Rapid Upside Move":
            "Acceleration confirms bullish conviction.",
            "Rapid Downside Move":
            "Sharp downside move—bearish pressure intensifying.",
            "Decelerating Move":
            "Price action slowing—possible inflection point.",
        },
        "Volume-Based Confirmation": {
            "High Volume Breakout":
            "Price movement validated by strong volume—signal strengthened.",
            "Low Volume Move":
            "Weak volume undermines conviction—caution warranted.",
            "Divergence Detected":
            "Volume trend contradicts price—possible reversal brewing.",
        },
        "Support/Resistance Validation": {
            "Support Holding":
            "Support respected—bullish defence evident.",
            "Resistance Holding":
            "Resistance maintained—sellers still dominant.",
            "Breakout Confirmed":
            "Key level cleared—trend continuation likely.",
            "Failed Breakout":
            "Breakout rejected—reversal or whipsaw risk elevated.",
        },

# -------------------------------------------------------------------------------------------------
# Breakout & Mean Reversion Insights
# -------------------------------------------------------------------------------------------------
        "Bollinger Band Expansion": {
            "Expanding Bands":
            "Volatility increasing—breakout or trend acceleration likely.",
            "Contracting Bands":
            "Volatility compressing—potential breakout setup forming.",
        },
        "Price Breakout vs. Mean Reversion": {
            "Breakout Above Resistance":
            "Bullish breakout confirmed—buying pressure dominant.",
            "Breakout Below Support":
            "Bearish breakout confirmed—selling momentum accelerating.",
            "Mean Reversion Setup":
            "Price reverting to mean—watch for potential reversal or entry zone.",
        },
        "ATR Volatility Trends": {
            "Increasing ATR":
            "Heightened volatility—greater risk and opportunity.",
            "Decreasing ATR":
            "Compressed volatility—range-bound movement expected.",
        },
        "Standard Deviation of Price Swings": {
            "High Volatility":
            "Volatility elevated—potential breakout or uncertainty.",
            "Low Volatility":
            "Price action stable—trend weakening or consolidating.",
        },
        "Volume vs. Price Range Compression": {
            "Decreasing Volume & Range":
            "Tight price action—breakout likely approaching.",
            "Increasing Volume & Range":
            "Wide ranges and rising volume—strong directional move likely.",
        },
    }

    return insights.get(indicator, {}).get(value, "No clear insight available for this scenario.")
