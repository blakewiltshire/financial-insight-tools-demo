# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
#
# Add any relevant disables (e.g., unused-import) if needed for clean linting.
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------

"""
Intermarket & Correlation Module (Cross Asset ↔ Asset) — Predefined Use Cases

This module defines curated analytical templates to support structured exploration of:

- Exploratory Comparison
- Correlation Consistency Check
- Regime Shift Detection
- Trend Sustainability
- Volatility Dynamics
- Volatility Divergence
- Lead-Lag Relationship
- Hedge Effectiveness
- Spread Mean Reversion

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
# Intermarket & Correlation Module (Asset ↔ Asset)
# -------------------------------------------------------------------------------------------------

USE_CASES = {
    "Exploratory Comparison": {
        "Indicators": [
            "Pearson Correlation",
            "Spearman Correlation",
            "ATR Ratio",
            "Standard Deviation"
        ],
        "Categories": ["Exploratory"],
        "Timeframes": ["Daily", "Weekly", "Monthly"],
        "Description": (
            "Raw statistical comparison — ideal for quick checks or uploaded pairs "
            "without requiring structured signal interpretation."
        )
    },
    "Correlation Consistency Check": {
        "Indicators": [
            "Rolling Pearson Correlation",
            "Correlation Z-Score"
        ],
        "Categories": ["Correlation"],
        "Timeframes": ["Daily", "Weekly"],
        "Description": (
            "Evaluate whether two assets have a stable relationship over time using "
            "rolling correlations and z-score variability."
        )
    },
    "Regime Shift Detection": {
        "Indicators": [
            "Delta of Rolling Correlation",
            "Rolling Correlation with Z-Bands"
        ],
        "Categories": ["Regime Shift"],
        "Timeframes": ["Weekly", "Monthly"],
        "Description": (
            "Detect meaningful shifts or breakdowns in asset correlation over different regimes. "
            "Highlights macro turning points or uncoupling."
        )
    },
    "Volatility Divergence": {
        "Indicators": [
            "ATR Ratio",
            "Standard Deviation Divergence"
        ],
        "Categories": ["Volatility"],
        "Timeframes": ["Daily", "Weekly"],
        "Description": (
            "Identify when two assets show diverging volatility regimes using ATR and "
            "standard deviation comparisons."
        )
    },
    "Lead-Lag Relationship": {
        "Indicators": [
            "Cross-Correlation Lag Analysis"
        ],
        "Categories": ["Timing"],
        "Timeframes": ["Daily", "Weekly"],
        "Description": (
            "Discover whether one asset tends to lead another in price movement using "
            "cross-correlation lags."
        )
    },
    "Hedge Effectiveness": {
        "Indicators": [
            "Inverse Correlation Detection",
            "Negative Pearson Tracking"
        ],
        "Categories": ["Hedge"],
        "Timeframes": ["Weekly", "Monthly"],
        "Description": (
            "Evaluate the reliability of an asset as a hedge under directional stress. "
            "Looks for inverse correlation zones."
        )
    },
    "Spread Mean Reversion": {
        "Indicators": [
            "Z-Score of Spread",
            "Spread Drift",
            "Rolling Spread Mean"
        ],
        "Categories": ["Spread"],
        "Timeframes": ["Daily", "Weekly", "Monthly"],
        "Description": (
            "Analyse whether two assets exhibit mean-reverting behaviour in their spread or ratio."
        )
    }
}

# -------------------------------------------------------------------------------------------------
# Function: get_use_cases
# Purpose: Exposes the USE_CASES dictionary for external modules (e.g., main app, helpers).
# -------------------------------------------------------------------------------------------------

def get_use_cases():
    """
    Returns the full dictionary of predefined use case templates for
    Intermarket & Correlation Module (Cross Asset ↔ Asset).
    """
    return USE_CASES
