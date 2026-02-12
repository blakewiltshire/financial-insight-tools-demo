# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
This module loads and processes financial asset datasets for correlation, volatility,
and return analysis. Supports both default and user-defined data sources.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
from pandas.errors import ParserError
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Internal Imports — Reusable Data Processing Components
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_correlation import clean_generic_data
from data_sources.financial_data.asset_map import asset_files
from data_sources.financial_data.user_asset_map import get_user_asset_path
from data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets

# -------------------------------------------------------------------------------------------------
# Commodities
# -------------------------------------------------------------------------------------------------
def load_and_clean_commodities():
    """
    Load and clean assets under 'Commodities', choosing either default or
    user-defined sources based on session selection. Consolidates all cleaned DataFrames for:
    - Correlation analysis
    - Volatility classification
    - Multi-period return calculation

    Returns:
        tuple: correlation_df, volatility_df, returns_df
    """
    cleaned_data_frames = []
    source_type = st.session_state.get("ASSET_SOURCE_TYPE", "Preloaded Asset Types (Default)")

    if source_type == "Preloaded Asset Types (User)":
        asset_category = "Commodities (User)"
        user_assets = get_user_preloaded_assets().get(asset_category, {})

        for cleaned_name, _ in user_assets.items():
            asset_path = get_user_asset_path(asset_category, cleaned_name)
            if asset_path:
                try:
                    data_frame = pd.read_csv(asset_path)
                    cleaned_data = clean_generic_data(
                    data_frame, "commodities_user", cleaned_name)
                    cleaned_data_frames.append(cleaned_data)
                except (FileNotFoundError, ParserError, OSError, ValueError) as error:
                    st.warning(f"Skipping user asset '{cleaned_name}': {error}")
    else:
        for asset_name, asset_file in asset_files.get("Commodities", {}).items():
            try:
                data_frame = pd.read_csv(asset_file)
                cleaned_data = clean_generic_data(data_frame, "commodities", asset_name)
                cleaned_data_frames.append(cleaned_data)
            except (FileNotFoundError, ParserError, OSError, ValueError) as error:
                st.warning(f"Skipping default asset '{asset_name}': {error}")

    correlation_df = pd.concat(cleaned_data_frames, axis=0, ignore_index=True)
    volatility_df = pd.concat(cleaned_data_frames, axis=0, ignore_index=True)
    returns_df = pd.concat(cleaned_data_frames, axis=0, ignore_index=True)

    return correlation_df, volatility_df, returns_df
