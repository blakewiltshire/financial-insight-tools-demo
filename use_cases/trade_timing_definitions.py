# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
#
# Add any relevant disables (e.g., unused-import) if needed for clean linting.
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------

"""
Trade, Timing and Confirmation — Predefined Use Cases

This module defines curated analytical templates to support structured exploration of:

- General Market Overview
- Trend Strength & Direction
- Reversal Identification
- Momentum Reversal Signals
- Institutional Activity & Trend Validity
- Risk & Expected Price Swings
- Reversal & Continuation Patterns

Use cases are mapped to preconfigured indicator groupings and thematic categories to:

- Auto-populate indicators in the Streamlit sidebar
- Drive sidebar help text via use_case_helpers.py
- Ensure cross-app consistency in indicator logic and naming

The default state — 'Naked Charts' — renders a clean chart without overlays or data mapping.
"""

# -------------------------------------------------------------------------------------------------
# Structured Use Case Definitions
# -------------------------------------------------------------------------------------------------
# Purpose: Maps indicators and categories to analytical templates used in the
# Trade, Timing and Confirmation Module
# -------------------------------------------------------------------------------------------------

USE_CASES = {
    "General Market Overview": {
        "overview": "Provides a high-level snapshot of market conditions using basic trend and volatility indicators.",
        "why_it_matters": "Establishes a foundational context for further analysis by identifying direction and volatility environment.",
        "indicators": [
            "Simple Moving Average", "Bollinger Bands"
        ],
        "Categories": ["Trend Confirmation", "Volatility & Risk"]
    },
    "Trend Strength & Direction": {
        "overview": "Evaluates the strength and direction of the prevailing market trend using trend-following indicators.",
        "why_it_matters": "Understanding the dominant trend helps align trades with momentum and avoid counter-trend setups.",
        "indicators": [
            "Average Directional Index", "Simple Moving Average", "Exponential Moving Average"
        ],
        "Categories": ["Trend Confirmation"],
        "Description": "Confirms trend strength and directionality using key moving averages."
    },
    "Reversal Identification": {
        "overview": "Detects when current trends may be weakening or reversing using dynamic support/resistance overlays.",
        "why_it_matters": "Helps identify profit-taking zones or potential countertrend entries.",
        "indicators": [
            "Parabolic SAR", "Super Trend", "Average Directional Index"
        ],
        "Categories": ["Trend Confirmation"],
        "Description": "Identifies trend reversals and uses momentum indicators for validation."
    },
    "Momentum Reversal Signals": {
        "overview": "Highlights shifts in momentum that may signal upcoming reversals or entry opportunities.",
        "why_it_matters": "Momentum changes often precede price reversals, allowing earlier and more precise trade setups.",
        "indicators": [
            "Moving Average Convergence Divergence", "Relative Strength Index",
            "Chande Momentum Oscillator"
        ],
        "Categories": ["Momentum & Strength"],
        "Description": "Confirms momentum reversals and trend strength."
    },
    "Institutional Activity & Trend Validity": {
        "overview": "Uses volume-based indicators to evaluate the credibility and sustainability of price moves.",
        "why_it_matters": "Volume trends often reflect institutional participation, helping to confirm or challenge price direction.",
        "indicators": [
            "On-Balance Volume", "Accumulation/Distribution Line"
        ],
        "Categories": ["Volume Confirmation", "Trend Confirmation"],
        "Description": "Confirms trend validity via volume accumulation/distribution."
    },
    "Risk & Expected Price Swings": {
        "overview": "Analyzes volatility conditions to gauge risk exposure and anticipate price fluctuations.",
        "why_it_matters": "Volatility context supports better position sizing, stop placement, and execution decisions.",
        "indicators": [
            "Average True Range", "Bollinger Bands", "Standard Deviation"
        ],
        "Categories": ["Volatility & Risk"],
        "Description": "Measures market volatility and risk for trade execution."
    },
    "Reversal & Continuation Patterns": {
        "overview": "Interprets classical price patterns to assess the likelihood of reversals or trend continuation.",
        "why_it_matters": "Pattern recognition enhances discretionary setups and scenario planning.",
        "indicators": [
            "Candlestick Patterns", "Head & Shoulders", "Flags & Pennants", "Double Tops/Bottoms"
        ],
        "Categories": ["Pattern Recognition"],
        "Description": "Confirms trend reversals and price action patterns."
    }
}

# -------------------------------------------------------------------------------------------------
# Function: get_use_cases
# Purpose: Exposes the USE_CASES dictionary for external modules (e.g., main app, helpers).
# -------------------------------------------------------------------------------------------------
def get_use_cases():
    """
    Returns the full dictionary of predefined use case templates for
    Trade Timing & Confirmation modules.
    """
    return USE_CASES
