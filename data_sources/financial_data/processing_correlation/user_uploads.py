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
# Correlation – User Uploads
# -------------------------------------------------------------------------------------------------
def load_and_clean_user_correlations(uploaded_files):
    """
    Load and clean all user-uploaded datasets for correlation analysis.

    Each file is parsed as a DataFrame, cleaned using `clean_generic_data`, and appended
    to a unified structure. Asset name is derived from the original file name for use in
    return and volatility attribution.

    Parameters:
        uploaded_files (list): List of Streamlit `UploadedFile` objects (.csv expected).

    Returns:
        pd.DataFrame: correlation_df_user — consolidated cleaned dataset for
        correlation diagnostics.
    """
    user_data_frames = []

    for uploaded_file in uploaded_files:
        # Load file
        user_df = pd.read_csv(uploaded_file)

        # Derive asset name from filename (excluding extension)
        name_value = uploaded_file.name.split(".")[0]

        # Clean using standard correlation data cleaner
        cleaned_user_data = clean_generic_data(user_df, "user_asset", name_value)

        # Accumulate cleaned frame
        user_data_frames.append(cleaned_user_data)

    # Combine all into a single user-level correlation DataFrame
    correlation_df_user = pd.concat(user_data_frames, axis=0, ignore_index=True)

    return correlation_df_user

# -------------------------------------------------------------------------------------------------
# Volatility – User Uploads
# -------------------------------------------------------------------------------------------------
def load_and_clean_user_volatility(uploaded_files):
    """
    Load and clean all user-uploaded datasets for volatility classification.

    Each file is parsed, cleaned using `clean_generic_data`, and tagged based on the original
    filename to support downstream attribution. Returns a consolidated DataFrame suitable
    for volatility diagnostics.

    Parameters:
        uploaded_files (list): List of Streamlit `UploadedFile` objects (.csv expected).

    Returns:
        pd.DataFrame: volatility_df_user — cleaned and concatenated data for volatility analysis.
    """
    user_data_frames = []

    for uploaded_file in uploaded_files:
        # Load user CSV into DataFrame
        user_df = pd.read_csv(uploaded_file)

        # Derive asset label from file name
        name_value = uploaded_file.name.split(".")[0]

        # Clean using standardised routine
        cleaned_user_data = clean_generic_data(user_df, "user_asset", name_value)

        # Accumulate for consolidation
        user_data_frames.append(cleaned_user_data)

    # Merge all into a single volatility DataFrame
    volatility_df_user = pd.concat(user_data_frames, axis=0, ignore_index=True)

    return volatility_df_user

# -------------------------------------------------------------------------------------------------
# Returns – User Uploads
# -------------------------------------------------------------------------------------------------
def load_and_prepare_user_returns(uploaded_files):
    """
    Load and clean all user-uploaded datasets for return analysis.

    Each file is read, standardised using `clean_generic_data`, and labelled by filename
    for contextual tracking. Returns a consolidated DataFrame suitable for temporal return
    breakdowns and cross-asset return diagnostics.

    Parameters:
        uploaded_files (list): List of Streamlit `UploadedFile` objects (.csv expected).

    Returns:
        pd.DataFrame: returns_df_user — cleaned and concatenated data for returns analysis.
    """
    user_data_frames = []

    for uploaded_file in uploaded_files:
        # Load the CSV into a DataFrame
        user_df = pd.read_csv(uploaded_file)

        # Extract identifier from filename
        name_value = uploaded_file.name.split(".")[0]

        # Clean and standardise the dataset
        cleaned_user_data = clean_generic_data(user_df, "user_asset", name_value)

        # Collect into unified structure
        user_data_frames.append(cleaned_user_data)

    # Merge all into a single DataFrame for return-related analysis
    returns_df_user = pd.concat(user_data_frames, axis=0, ignore_index=True)

    return returns_df_user
