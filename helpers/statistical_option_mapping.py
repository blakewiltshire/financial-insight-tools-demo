# -------------------------------------------------------------------------------------------------
# pylint global exceptions
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
statistical_option_mapping.py

This module provides a utility function to route requests to the appropriate
data mapping dictionary based on a specified mapping type (e.g., correlation, returns, volatility).

It serves as a central access point for retrieving the correct data-loading map,
supporting dynamic logic in Streamlit applications for financial analytics.

Example:
    from data_mapping_router import get_data_mapping

    mapping = get_data_mapping("returns")
    loader_fn, df_name = mapping["Returns with Equities - Magnificent Seven"]
"""

# -------------------------------------------------------------------------------------------------
# Imports: Ensure underlying mapping dictionaries are available
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.mapped_financial_data_loaders import (
    correlation_data_mapping,
    returns_data_mapping,
    volatility_data_mapping,
)


# -------------------------------------------------------------------------------------------------
# Function: get_data_mapping
# Purpose: Retrieve the appropriate data mapping dictionary based on input type
# Use Case: Dynamic routing of asset data in statistical modules and Streamlit selectboxes
# -------------------------------------------------------------------------------------------------
def get_data_mapping(mapping_type: str) -> dict:
    """
    Return the corresponding data mapping dictionary for the specified mapping type.

    Parameters:
        mapping_type (str): The category of mapping required. Acceptable values include:
                            - "correlation"
                            - "returns"
                            - "volatility"

    Returns:
        dict: The relevant data mapping dictionary if a valid type is provided.
              Returns an empty dictionary for unrecognised input.

    Example:
        mapping = get_data_mapping("correlation")
        loader_func, df_name = mapping["Correlation with Market Indices"]
    """
    return {
        "correlation": correlation_data_mapping,
        "returns": returns_data_mapping,
        "volatility": volatility_data_mapping,
    }.get(mapping_type.strip().lower(), {})
