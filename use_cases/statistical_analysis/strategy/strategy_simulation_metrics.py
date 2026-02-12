# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module provides a structured mapping between user-facing analytical categories and their
underlying functional logic across statistical, risk, market dynamics, and performance analysis.

It facilitates the selection logic used in statistical and visualisation panels, enabling
dynamic Streamlit interfaces to present relevant options grouped by analytical purpose.

Each entry maps a display label (e.g., 'Descriptive Statistics') to:
1. A corresponding function dictionary (e.g., options_descriptive_statistics_map), and
2. A category-to-function-label structure for sidebar groupings and UI presentation.

This ensures consistent application routing, modular expandability, and clarity
when presenting complex market metrics, risk diagnostics, or performance views.
"""

# -------------------------------------------------------------------------------------------------
# Import Mapped Functional Modules by Category
# -------------------------------------------------------------------------------------------------
from use_cases.statistical_analysis.descriptive.descriptive_statistics \
    import options_descriptive_statistics_map

from use_cases.statistical_analysis.risk.monte_carlo_and_risk_metrics \
    import options_risk_and_uncertainty_map

from use_cases.statistical_analysis.dynamics.market_dynamics \
    import options_market_dynamics_map

from use_cases.statistical_analysis.performance.performance_metrics_and_correlations \
    import options_performance_and_correlation_map

from use_cases.statistical_analysis.visualisations.visualisations \
    import options_data_visualisations_map

# -------------------------------------------------------------------------------------------------
# Master Option Map for Statistical and Visual Analysis Tools
# -------------------------------------------------------------------------------------------------
options_maps = {
    'Descriptive Statistics': (
        options_descriptive_statistics_map,
        {
            "Descriptive Statistics": [
                "Measure of Central Tendency", "Measures of Dispersion",
                "Measures of Shape", "Basic Statistics", "Frequency Distribution"
            ],
        }
    ),

    'Risk and Uncertainty Analysis': (
        options_risk_and_uncertainty_map,
        {
            "Risk and Uncertainty Analysis": [
                "Monte Carlo Simulations", "Risk-Adjusted Returns (Sharpe Ratio)",
                "Downside Risk Measure (Sortino Ratio)", "Probability of Hitting DPT"
            ],
        }
    ),

    'Market Dynamics': (
        options_market_dynamics_map,
        {
            "Market Dynamics": [
                "Volatility Ratio", "ATR (Average True Range)"
            ],
        }
    ),

    'Performance Metrics & Correlations': (
        options_performance_and_correlation_map,
        {
            "Performance Analysis": [
                "Annualised Return", "Maximum Drawdown",
                "Volatility-Adjusted Return", "Return on Investment (ROI)"
            ],
            "Correlation & Causation Analysis": [
                "Volume vs ATR Correlation",
                "Correlation with Equities - Magnificent Seven",
                "Correlation with Equities - Sector Constituents",
                "Correlation with Market Indices", "Correlation with Currencies",
                "Correlation with Cryptocurrency", "Correlation with Commodities",
                "Correlation with ETFs - Popular", "Correlation with ETFs - Sectors",
                "Correlation with ETFs - Countries", "Correlation with Short-Term Bonds",
                "Correlation with Long-Term Bonds", "Correlation with User Uploads"
            ],
            "Volatility & Opportunity": [
                "Volatility with Equities - Magnificent Seven",
                "Volatility with Equities - Sector Constituents",
                "Volatility with Market Indices", "Volatility with Currencies",
                "Volatility with Cryptocurrency", "Volatility with Commodities",
                "Volatility with ETFs - Popular", "Volatility with ETFs - Sectors",
                "Volatility with ETFs - Countries", "Volatility with Short-Term Bonds",
                "Volatility with Long-Term Bonds", "Volatility with User Uploads"
            ],
        }
    ),

    'Data Visualisation': (
        options_data_visualisations_map,
        {
            "Price Movement & Trend Visualisation": [
                "Price Movement - Line", "Price Movement - Candlestick",
                "Trend Visualisation - Area"
            ],
            "Returns": [
                "Range and Events Returns", "Temporal Returns",
                "Returns with Equities - Magnificent Seven",
                "Returns with Equities - Sector Constituents",
                "Returns with Market Indices", "Returns with Currencies",
                "Returns with Cryptocurrency", "Returns with Commodities",
                "Returns with ETFs - Popular", "Returns with ETFs - Sectors",
                "Returns with ETFs - Countries", "Returns with Short-Term Bonds",
                "Returns with Long-Term Bonds", "Returns with User Uploads"
            ],
            "Additional Return Metrics": [
                "Cumulative Returns", "Rolling Returns"
            ],
            "Risk-Return Analysis": [
                "Risk-Return"
            ],
            "Volatility vs DPT Achievement": [
                "DPT vs Volatility"
            ]
        }
    ),
}
