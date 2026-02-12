# -------------------------------------------------------------------------------------------------
# pylint global exceptions
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
mapped_data_loaders.py

This module consolidates all mappings for loading cleaned financial datasets across
correlation, returns, and volatility categories. Each entry defines a user-facing label,
a data-loading function, and the corresponding dataframe name.

This unified mapping structure supports:
- Consistent and dynamic routing in Streamlit apps
- Centralised maintenance for asset group loading logic
- Modular UI logic for performance, correlation, and risk visualisation

Example usage:
    label = "Volatility with Equities - Magnificent Seven"
    loader, df_name = volatility_data_mapping[label]
    df = loader()
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_correlation_assets import (
    load_and_clean_market_indices,
    load_and_clean_equities_7,
    load_and_clean_equities_const,
    load_and_clean_currency,
    load_and_clean_cryptocurrency,
    load_and_clean_commodities,
    load_and_clean_popular,
    load_and_clean_sectors,
    load_and_clean_countries,
    load_and_clean_short_term_bonds,
    load_and_clean_long_term_bonds,
    load_and_clean_user_correlations,
    load_and_clean_user_volatility,
    load_and_prepare_user_returns,
)

# -------------------------------------------------------------------------------------------------
# Correlation Mapping
# -------------------------------------------------------------------------------------------------
correlation_data_mapping = {
    "Correlation with Equities - Magnificent Seven":
    (load_and_clean_equities_7, "equities_correlation_df"),
    "Correlation with Equities - Sector Constituents":
    (load_and_clean_equities_const, "equities_correlation_const_df"),
    "Correlation with Market Indices":
    (load_and_clean_market_indices, "market_indices_correlation_df"),
    "Correlation with Currencies":
    (load_and_clean_currency, "currency_correlation_df"),
    "Correlation with Cryptocurrency":
    (load_and_clean_cryptocurrency, "cryptocurrency_correlation_df"),
    "Correlation with Commodities":
    (load_and_clean_commodities, "commodity_correlation_df"),
    "Correlation with ETFs - Popular":
    (load_and_clean_popular, "popular_correlation_df"),
    "Correlation with ETFs - Sectors":
    (load_and_clean_sectors, "sector_correlation_df"),
    "Correlation with ETFs - Countries":
    (load_and_clean_countries, "country_correlation_df"),
    "Correlation with Short-Term Bonds":
    (load_and_clean_short_term_bonds, "short_bonds_correlation_df"),
    "Correlation with Long-Term Bonds":
    (load_and_clean_long_term_bonds, "long_bonds_correlation_df"),
    # "Correlation with User Uploads":
    # (load_and_clean_user_correlations, "user_correlation_df"),
}

# -------------------------------------------------------------------------------------------------
# Returns Mapping
# -------------------------------------------------------------------------------------------------
returns_data_mapping = {
    "Returns with Equities - Magnificent Seven":
    (load_and_clean_equities_7, "equities_returns_df"),
    "Returns with Equities - Sector Constituents":
    (load_and_clean_equities_const, "equities_returns_const_df"),
    "Returns with Market Indices":
    (load_and_clean_market_indices, "market_indices_returns_df"),
    "Returns with Currencies":
    (load_and_clean_currency, "currency_returns_df"),
    "Returns with Cryptocurrency":
    (load_and_clean_cryptocurrency, "cryptocurrency_returns_df"),
    "Returns with Commodities":
    (load_and_clean_commodities, "commodity_returns_df"),
    "Returns with ETFs - Popular":
    (load_and_clean_popular, "popular_returns_df"),
    "Returns with ETFs - Sectors":
    (load_and_clean_sectors, "sector_returns_df"),
    "Returns with ETFs - Countries":
    (load_and_clean_countries, "country_returns_df"),
    "Returns with Short-Term Bonds":
    (load_and_clean_short_term_bonds, "short_bonds_returns_df"),
    "Returns with Long-Term Bonds":
    (load_and_clean_long_term_bonds, "long_bonds_returns_df"),
    # "Returns with User Uploads":
    # (load_and_prepare_user_returns, "user_returns_df"),
}

# -------------------------------------------------------------------------------------------------
# Volatility Mapping
# -------------------------------------------------------------------------------------------------
volatility_data_mapping = {
    "Volatility with Equities - Magnificent Seven":
    (load_and_clean_equities_7, "equities_volatility_df"),
    "Volatility with Equities - Sector Constituents":
    (load_and_clean_equities_const, "equities_volatility_const_df"),
    "Volatility with Market Indices":
    (load_and_clean_market_indices, "market_indices_volatility_df"),
    "Volatility with Currencies":
    (load_and_clean_currency, "currency_volatility_df"),
    "Volatility with Cryptocurrency":
    (load_and_clean_cryptocurrency, "cryptocurrency_volatility_df"),
    "Volatility with Commodities":
    (load_and_clean_commodities, "commodity_volatility_df"),
    "Volatility with ETFs - Popular":
    (load_and_clean_popular, "popular_volatility_df"),
    "Volatility with ETFs - Sectors":
    (load_and_clean_sectors, "sector_volatility_df"),
    "Volatility with ETFs - Countries":
    (load_and_clean_countries, "country_volatility_df"),
    "Volatility with Short-Term Bonds":
    (load_and_clean_short_term_bonds, "short_bonds_volatility_df"),
    "Volatility with Long-Term Bonds":
    (load_and_clean_long_term_bonds, "long_bonds_volatility_df"),
    # "Volatility with User Uploads":
    # (load_and_clean_user_volatility, "user_volatility_df"),
}
