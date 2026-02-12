# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name, import-error

"""
Use Case Indicators — Correlation Heatmaps & Themes

This module provides grouped indicator logic for use cases related to:
- General Correlation Overview
- Concentration Risk Clustering
- Inverse Pair Identification
- Sector Correlation Analysis
- Cross-Asset Diversification Assessment

Each section includes:
- Core computation functions
- Signal interpretation logic
- An indicator → function map used by dynamic app rendering

Indicator groups in this module:
- `options_correlation_core_map`
- `options_diversification_clustering_map`
- `options_sector_relationship_map`

File designed for Streamlit integration with Correlation Heatmaps & Themes DSS module.
"""

# -------------------------------------------------------------------------------------------------
# Standard Library Imports
# -------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

# -------------------------------------------------------------------------------------------------
# Correlation Core
# -------------------------------------------------------------------------------------------------

def correlation_coefficient(df):
    """Computes full correlation matrix."""
    corr_matrix = df.corr()
    return corr_matrix

def p_value_matrix(df):
    """Computes matrix of p-values for correlation coefficients."""
    assets = df.columns
    p_matrix = pd.DataFrame(index=assets, columns=assets)

    for a in assets:
        for b in assets:
            if a == b:
                p_matrix.loc[a, b] = 0.0
            else:
                _, p = pearsonr(df[a], df[b])
                p_matrix.loc[a, b] = p
    return p_matrix

options_correlation_core_map = {
    "Correlation Coefficient": correlation_coefficient,
    "P-Value": p_value_matrix
}

# -------------------------------------------------------------------------------------------------
# Diversification & Clustering
# -------------------------------------------------------------------------------------------------

def average_correlation(df):
    """Computes average off-diagonal correlation."""
    corr = df.corr().values
    avg_corr = (np.sum(corr) - np.trace(corr)) / (corr.shape[0]*(corr.shape[0]-1))
    return round(avg_corr, 3)

def strongest_correlation_pair(df):
    """Identifies the strongest positively correlated pair."""
    corr = df.corr()
    np.fill_diagonal(corr.values, np.nan)
    max_pair = corr.unstack().idxmax()
    max_value = corr.unstack().max()
    return {"pair": max_pair, "correlation": round(max_value, 3)}

def strongest_inverse_pair(df):
    """Identifies strongest inverse (negative) correlation pair."""
    corr = df.corr()
    np.fill_diagonal(corr.values, np.nan)
    min_pair = corr.unstack().idxmin()
    min_value = corr.unstack().min()
    return {"pair": min_pair, "correlation": round(min_value, 3)}

def diversification_assessment(df):
    """Simple DSS logic: provides rough classification of diversification strength."""
    avg_corr = average_correlation(df)
    if avg_corr >= 0.75:
        return "🚩 High Concentration Risk — Low Diversification"
    if avg_corr >= 0.5:
        return "⚠️ Moderate Concentration — Watch Portfolio Weighting"
    if avg_corr >= 0.25:
        return "🟠 Some Diversification Present"
    return "✅ Strong Diversification Present"

options_diversification_clustering_map = {
    "Average Correlation": average_correlation,
    "Strongest Correlation Pair": strongest_correlation_pair,
    "Strongest Inverse Pair": strongest_inverse_pair,
    "Diversification Assessment": diversification_assessment
}

# -------------------------------------------------------------------------------------------------
# Sector Relationship Analysis
# -------------------------------------------------------------------------------------------------

def sector_correlation_matrix(df, sector_mapping):
    """
    Aggregates sector-level correlation matrix using provided sector_mapping dictionary.
    Assumes df columns are individual assets.
    """
    sector_data = {}
    for asset, sector in sector_mapping.items():
        if sector not in sector_data:
            sector_data[sector] = []
        if asset in df.columns:
            sector_data[sector].append(df[asset])

    sector_df = pd.DataFrame({k: pd.concat(v, axis=1).mean(axis=1) for k, v in sector_data.items()})
    return sector_df.corr()

options_sector_relationship_map = {
    "Sector Correlation Matrix": sector_correlation_matrix
}

# -------------------------------------------------------------------------------------------------
# Master Indicator Mapping — Full Reference Used by Main App
# -------------------------------------------------------------------------------------------------

INDICATOR_MAPS = {
    "Correlation Core": options_correlation_core_map,
    "Diversification & Clustering": options_diversification_clustering_map,
    "Sector Relationships": options_sector_relationship_map
}
