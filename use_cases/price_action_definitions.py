# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
#
# Add any relevant disables (e.g., unused-import) if needed for clean linting.
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Price Action & Trend Confirmation — Predefined Use Cases

This module defines curated analytical templates to support structured exploration of:

- Performance
- Trend & Momentum
- Breakout & Mean Reversion

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
# Price Action & Trend Confirmation Module
# -------------------------------------------------------------------------------------------------
USE_CASES = {
    "Performance": {
        "Indicators": [
            "Winning vs. Losing",
            "Rolling Returns",
            "Volatility-Adjusted Returns",
            "Momentum Score",
            "Net Price Movement"
        ],
        "Categories": ["Performance"],
        "Description":
            "Evaluates directional consistency, return volatility, and net price movement."
    },
    "Trend & Momentum": {
        "Indicators": [
            "Price Rate of Change",
            "Price Action Momentum",
            "Trend Confirmation (Higher Highs / Lower Lows)",
            "Momentum Strength",
            "Price Acceleration",
            "Volume-Based Confirmation",
            "Support/Resistance Validation"
        ],
        "Categories": ["Trend & Momentum"],
        "Description":
            "Assesses directional strength, trend sustainability, and momentum quality."
    },
    "Breakout & Mean Reversion": {
        "Indicators": [
            "Bollinger Band Expansion",
            "Price Breakout vs. Mean Reversion",
            "ATR Volatility Trends",
            "Standard Deviation of Price Swings",
            "Volume vs. Price Range Compression"
        ],
        "Categories": ["Breakout & Mean Reversion"],
        "Description":
            "Detects breakout signals, compression setups, and volatility expansions."
    }
}

# -------------------------------------------------------------------------------------------------
# Function: get_use_cases
# Purpose: Exposes the USE_CASES dictionary for external modules (e.g., main app, helpers).
# -------------------------------------------------------------------------------------------------
def get_use_cases():
    """Returns the full dictionary of predefined use case templates for Price Action modules."""
    return USE_CASES
