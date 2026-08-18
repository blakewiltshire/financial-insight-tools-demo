# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Path Utilities — Financial Data Directory Resolvers

This module provides standardised functions for resolving absolute file paths
within the `/apps/data_sources/financial_data/` structure. It ensures
portability, readability, and structural consistency across all modules that
load CSV datasets (e.g., price histories, market indices, ETF series).

Used by:
- `asset_map.py`
- `processing_default.py`
- Any Streamlit module referencing financial data directly

Functions:
- `get_data_root_path()`: Returns the absolute path to the financial_data directory
- `resolve_data_file_path(...)`: Builds a full file path to a specific CSV or subdirectory
"""

# -------------------------------------------------------------------------------------------------
# Standard Library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Function: Root Directory Resolver
# -------------------------------------------------------------------------------------------------
def get_data_root_path():
    """
    Returns the absolute path to the financial data directory, relative to this script.

    Returns:
        str: Absolute path to `/apps/data_sources/financial_data`
    """
    return os.path.abspath(os.path.dirname(__file__))

# -------------------------------------------------------------------------------------------------
# Function: Full Path Builder
# -------------------------------------------------------------------------------------------------
def resolve_data_file_path(*subpaths):
    """
    Builds an absolute path to a file within the financial data folder.

    Args:
        subpaths (str): One or more path segments to append to the root path.
                        Example: "equities", "Tesla Stock Price History.csv"

    Returns:
        str: Absolute file path, ready for use in `pd.read_csv(...)` or similar
    """
    return os.path.join(get_data_root_path(), *subpaths)
