# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

"""
Correlation Heatmaps & Themes — Predefined Use Cases

This module defines curated analytical templates to support structured exploration of:

- General Correlation Overview
- Concentration Risk Clustering
- Inverse Pair Identification
- Sector Correlation Analysis
- Cross-Asset Diversification Assessment

Use cases are mapped to preconfigured indicator groupings and thematic categories to:

- Auto-populate indicators in the Streamlit sidebar
- Drive sidebar help text via use_case_helpers.py
- Ensure cross-app consistency in indicator logic and naming

The default state — 'Naked Charts' — renders a clean heatmap without overlays or interpretation.
"""

# -------------------------------------------------------------------------------------------------
# Structured Use Case Definitions
# -------------------------------------------------------------------------------------------------

USE_CASES = {
    "General Correlation Overview": {
        "Indicators": ["Correlation Coefficient", "P-Value"],
        "Categories": ["Correlation Core"],
        "Description": "Basic overview of pairwise correlations between selected assets."
    },
    "Concentration Risk Clustering": {
        "Indicators": ["Average Correlation", "Strongest Correlation Pair"],
        "Categories": ["Diversification & Clustering"],
        "Description": "Identifies clustering risks and concentration across asset groupings."
    },
    "Inverse Pair Identification": {
        "Indicators": ["Strongest Inverse Pair"],
        "Categories": ["Diversification & Clustering"],
        "Description": "Detects strongest negatively correlated pairs for hedging or diversification."
    },
    "Sector Correlation Analysis": {
        "Indicators": ["Sector Correlation Matrix"],
        "Categories": ["Sector Relationships"],
        "Description": "Evaluates sector-level intra-group correlation structures."
    },
    "Cross-Asset Diversification Assessment": {
        "Indicators": ["Diversification Assessment"],
        "Categories": ["Diversification & Clustering"],
        "Description": "Provides DSS-style diversification strength evaluations."
    }
}

# -------------------------------------------------------------------------------------------------
# Function: get_use_cases
# -------------------------------------------------------------------------------------------------
def get_use_cases():
    """
    Returns the full dictionary of predefined use case templates for
    Correlation Heatmaps & Themes DSS module.
    """
    return USE_CASES
