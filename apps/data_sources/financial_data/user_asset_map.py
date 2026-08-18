# # -------------------------------------------------------------------------------------------------
# # Pylint Global Exceptions
# # -------------------------------------------------------------------------------------------------
# # pylint: disable=unused-argument
#
# # -------------------------------------------------------------------------------------------------
# # Docstring
# # -------------------------------------------------------------------------------------------------
# """
# User Asset Map
#
# Builds a dynamic lookup for file paths corresponding to user-managed asset categories.
#
# This module mirrors the default `asset_map.py` structure but sources from folders like
# `commodities_user/`, `currencies_user/`, etc., allowing users to maintain their own
# custom preloaded datasets.
#
# Primary Role:
# - Enables universal integration of user-defined asset files across modules
#   (e.g., correlation, returns, ATR calculators).
# - Supports category-agnostic resolution of full CSV paths.
#
# Used by:
# - Statistical mapping logic
# - Trade structuring and asset snapshot modules
# - Custom data ingestion workflows
# """
#
# # -------------------------------------------------------------------------------------------------
# # Standard library
# # -------------------------------------------------------------------------------------------------
# import os
#
# # -------------------------------------------------------------------------------------------------
# # Imports
# # -------------------------------------------------------------------------------------------------
# from .path_utils import resolve_data_file_path
#
# # Should mirror USER_CATEGORY_MAP from preloaded
# USER_CATEGORY_TO_FOLDER = {
#     "Equities - Magnificent Seven (User)": "equities_mag7_user",
#     "Equities - Sector Constituents (User)": "equities_constituents_user",
#     "Market Indices (User)": "market_indices_user",
#     "Currencies (User)": "currencies_user",
#     "Cryptocurrency (User)": "cryptocurrencies_user",
#     "Commodities (User)": "commodities_user",
#     "ETFs - Popular (User)": "etf_popular_user",
#     "ETFs - Sectors (User)": "etf_sectors_user",
#     "ETFs - Countries (User)": "etf_countries_user",
#     "Short-Term Bonds (User)": "short_term_bonds_user",
#     "Long-Term Bonds (User)": "long_term_bonds_user",
# }
#
# # -------------------------------------------------------------------------------------------------
# # Build User Maps
# # -------------------------------------------------------------------------------------------------
# def build_user_asset_map() -> dict:
#     """
#     Builds a dictionary mapping each user asset category to its associated file paths.
#
#     Scans `_user` folders for valid `.csv` files and constructs a structure that mirrors
#     the main `asset_map.py` layout, allowing seamless integration into shared logic.
#
#     Returns:
#         dict: {
#             "Commodities (User)": {
#                 "Gold Futures": "/path/to/commodities_user/Gold Futures.csv",
#                 ...
#             },
#             ...
#         }
#     """
#     asset_map = {}
#
#     for category, folder in USER_CATEGORY_TO_FOLDER.items():
#         folder_path = os.path.join(os.path.dirname(__file__), folder)
#         if not os.path.isdir(folder_path):
#             continue
#
#         asset_map[category] = {}
#
#         for file in os.listdir(folder_path):
#             if file.lower().endswith(".csv"):
#                 asset_name = os.path.splitext(file)[0]
#                 full_path = resolve_data_file_path(folder, file)
#                 asset_map[category][asset_name] = full_path
#
#     return asset_map
#
# # -------------------------------------------------------------------------------------------------
# # Retrieve full file path
# # -------------------------------------------------------------------------------------------------
# def get_user_asset_path(category: str, name: str) -> str:
#     """
#     Retrieve the absolute file path for a specific user-provided asset.
#
#     Args:
#         category (str): User asset category (e.g., "Currencies (User)").
#         name (str): Name of the asset (without `.csv` extension).
#
#     Returns:
#         str: Full file path to the asset, or None if not found.
#     """
#     asset_map = build_user_asset_map()
#     return asset_map.get(category, {}).get(name)


# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------
# pylint: disable=unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
User Asset File Mapper

Maps user-visible asset names (from dropdowns) to their full file paths,
based on user-managed folders (e.g., `commodities_user`, `currencies_user`).

This module works with the cleaned labels generated by `user_preloaded_assets.py`.
When a user selects an asset (e.g., "Alphabet A"), this module matches it to
the correct filename (e.g., "Alphabet A Stock Price History.csv") and returns the path.

This logic ensures clean user interaction without sacrificing compatibility
with the original file naming conventions.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
from .path_utils import resolve_data_file_path
from .user_preloaded_assets import get_user_preloaded_assets, USER_CATEGORY_MAP

# -------------------------------------------------------------------------------------------------
# Retrieve full file path
# -------------------------------------------------------------------------------------------------
def get_user_asset_path(category: str, cleaned_name: str) -> str:
    """
    Retrieve file path for user-uploaded asset using its cleaned display name.

    Args:
        category (str): User asset category (e.g. 'Commodities (User)')
        cleaned_name (str): Displayed cleaned name from dropdown (e.g. 'Tesla')

    Returns:
        str: File path to asset CSV or None if not found.
    """
    asset_map = get_user_preloaded_assets()
    category_map = asset_map.get(category, {})
    raw_name = category_map.get(cleaned_name)

    if raw_name:
        return resolve_data_file_path(USER_CATEGORY_MAP[category], raw_name + ".csv")

    return None
