# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=unused-argument

"""
Insight Generator — Correlation Heatmaps & Themes

Provides structured DSS-style qualitative messaging for correlation analysis.

This module returns pre-defined narrative insights for:

- Correlation Strength
- Diversification Assessment
- Concentration Clustering
- Inverse Pair Signals
- Sector Correlation Themes

The insight structure supports modular DSS augmentation, AI persona interaction, and consistent
narrative alignment across Financial Insight Tools modules.
"""

def generate_insights(indicator, value, timeframe, predisposition):
    """
    Provides structured insights for correlation-based analysis modules.

    Parameters:
    - indicator (str): Name of the indicator or signal category.
    - value (any): Signal output from correlation processing functions.
    - timeframe (str): Retained for cross-app compatibility.
    - predisposition (str): Retained for consistency, not used in this module.

    Returns:
    - str: Structured insight message.
    """

    insights = {

        # -------------------------------------------------------------------------------------------------
        # --- Correlation Core ---
        # -------------------------------------------------------------------------------------------------

        "Correlation Coefficient": {
            "Very Strong Positive": "Correlation coefficient above 0.8 indicates very tight co-movement.",
            "Strong Positive": "Correlation between 0.6 and 0.8 suggests sustained alignment between assets.",
            "Moderate Positive": "Correlation between 0.4 and 0.6 shows moderate co-movement.",
            "Weak Positive": "Correlation between 0.2 and 0.4 indicates mild directional similarity.",
            "Negligible": "Correlation near zero indicates no significant relationship.",
            "Weak Negative": "Correlation between -0.2 and -0.4 suggests mild inverse behavior.",
            "Moderate Negative": "Correlation between -0.4 and -0.6 reflects moderate inverse tendencies.",
            "Strong Negative": "Correlation between -0.6 and -0.8 indicates strong inverse coupling.",
            "Very Strong Negative": "Correlation below -0.8 suggests assets move strongly opposite each other."
        },

        "P-Value": {
            "Significant": "P-Value below 0.05 suggests statistical significance — observed correlation likely not due to random chance.",
            "Not Significant": "P-Value above 0.05 indicates correlation may lack statistical confidence — exercise caution."
        },

        # -------------------------------------------------------------------------------------------------
        # --- Diversification & Clustering ---
        # -------------------------------------------------------------------------------------------------

        "Diversification Assessment": {
            "🚩 High Concentration Risk — Low Diversification": "Portfolio highly concentrated — strong positive correlations dominate. Risk of collective drawdown increases.",
            "⚠️ Moderate Concentration — Watch Portfolio Weighting": "Moderate concentration detected. Allocation discipline is advised to manage correlated exposure.",
            "🟠 Some Diversification Present": "Diversification present but moderate cross-asset correlation remains. Watch cluster sensitivities.",
            "✅ Strong Diversification Present": "Asset mix exhibits strong diversification — lower correlation between positions."
        },

        "Average Correlation": {
            "Insight": lambda value: (
                f"Average pairwise correlation across selected assets is {value:.2f}. "
                "Higher values suggest increasing co-movement; lower values imply stronger diversification."
            )
        },

        "Strongest Correlation Pair": {
            "Insight": lambda pair, corr: f"Highest positive correlation observed between {pair[0]} and {pair[1]} (r={corr:.2f})."
        },

        "Strongest Inverse Pair": {
            "Insight": lambda pair, corr: f"Strongest inverse correlation observed between {pair[0]} and {pair[1]} (r={corr:.2f})."
        },

        # -------------------------------------------------------------------------------------------------
        # --- Sector Relationships ---
        # -------------------------------------------------------------------------------------------------

        "Sector Correlation Matrix": {
            "Insight": "Sector-level correlation matrix computed — supports cross-sector rotation, hedging, or thematic positioning."
        }
    }

    # Logic Routing (Handles dynamic cases for pair-specific outputs)
    if indicator == "Strongest Correlation Pair" and isinstance(value, dict):
        pair = value.get("pair", ("?", "?"))
        corr = value.get("correlation", 0)
        return insights[indicator]["Insight"](pair, corr)

    if indicator == "Strongest Inverse Pair" and isinstance(value, dict):
        pair = value.get("pair", ("?", "?"))
        corr = value.get("correlation", 0)
        return insights[indicator]["Insight"](pair, corr)

    if indicator == "Average Correlation":
    return insights[indicator]["Insight"](value)    

    # Static Mapping
    category = insights.get(indicator)
    if category:
        return category.get(value, "No clear insight available for this scenario.")

    return "No insight mapping available."
