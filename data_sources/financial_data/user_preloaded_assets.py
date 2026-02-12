# # -------------------------------------------------------------------------------------------------
# # Pylint Global Exceptions
# # -------------------------------------------------------------------------------------------------
#
# # -------------------------------------------------------------------------------------------------
# # Docstring
# # -------------------------------------------------------------------------------------------------
# """
# User Preloaded Asset Definitions
#
# Dynamically constructs a dictionary of available user-defined assets for each category,
# sourced from `_user` folders (e.g., `etf_sectors_user`, `currencies_user`).
#
# Primary Role:
# - Feeds 'Preloaded Asset Types (User)' selectboxes across apps.
# - Supports validation and structured dropdowns without requiring hardcoded asset lists.
#
# Key Feature:
# - Automatically reflects any file additions/removals made by the user in asset folders.
# """
# # -------------------------------------------------------------------------------------------------
# # Standard library
# # -------------------------------------------------------------------------------------------------
# import os
#
# # -------------------------------------------------------------------------------------------------
# # Base directory for user-managed asset folders (same directory as this script)
# # -------------------------------------------------------------------------------------------------
# USER_DATA_DIR = os.path.dirname(__file__)
#
# # -------------------------------------------------------------------------------------------------
# # Optional suffixes to strip from filenames when displaying in dropdowns
# # -------------------------------------------------------------------------------------------------
# ASSET_NAME_CLEANUP = [
#     " Stock Price History",
#     " Historical Data",
#     " ETF Price Data"
# ]
# # -------------------------------------------------------------------------------------------------
# # Function: Clean Asset Label
# # Purpose: Removes known suffixes or formatting strings from filenames
# # -------------------------------------------------------------------------------------------------
# def clean_asset_label(raw_name: str) -> str:
#     """
#     Removes known suffixes or formatting strings from a filename for user display.
#
#     Args:
#         raw_name (str): Filename without extension.
#
#     Returns:
#         str: Cleaned asset label for dropdowns.
#     """
#     cleaned = raw_name
#     for suffix in ASSET_NAME_CLEANUP:
#         if cleaned.endswith(suffix):
#             cleaned = cleaned.replace(suffix, "")
#     return cleaned.strip()
#
# # -------------------------------------------------------------------------------------------------
# # Category mapping to folder names
# # -------------------------------------------------------------------------------------------------
# USER_CATEGORY_MAP = {
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
# # Function: get_preloaded_assets
# # Purpose: Returns asset categories used in 'Preloaded Asset Types'
# # -------------------------------------------------------------------------------------------------
# def get_user_preloaded_assets() -> dict:
#     """
#     Constructs a dictionary of available user-defined assets for each `_user` folder category.
#
#     Returns:
#         dict: {
#             "Cryptocurrency (User)": ["Biatcoin", "Ethereum", ...],
#             ...
#         }
#     Only includes assets with `.csv` extensions. Strips extensions and known suffixes for use in dropdowns.
#     """
#     result = {}
#     for category_label, folder_name in USER_CATEGORY_MAP.items():
#         folder_path = os.path.join(USER_DATA_DIR, folder_name)
#         if not os.path.isdir(folder_path):
#             continue
#
#         asset_list = []
#         for file in os.listdir(folder_path):
#             if file.lower().endswith(".csv"):
#                 raw_name = os.path.splitext(file)[0]
#                 asset_list.append(clean_asset_label(raw_name))
#
#         if asset_list:
#             result[category_label] = sorted(asset_list)
#
#     return result



# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
User Preloaded Asset Definitions

Dynamically constructs a mapping of available user-defined assets by category,
sourced from `_user` folders (e.g., `commodities_user`, `currencies_user`).

Used to populate 'Preloaded Asset Types (User)' dropdowns and validation logic.
Ensures human-friendly names in UI while preserving underlying file structure.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os

# -------------------------------------------------------------------------------------------------
# Base directory for user-managed asset folders (e.g., commodities_user, currencies_user)
# -------------------------------------------------------------------------------------------------
USER_DATA_DIR = os.path.dirname(__file__)

# -------------------------------------------------------------------------------------------------
# Category mapping to folder names
# -------------------------------------------------------------------------------------------------
USER_CATEGORY_MAP = {
    "Equities - Magnificent Seven (User)": "equities_mag7_user",
    "Equities - Sector Constituents (User)": "equities_constituents_user",
    "Market Indices (User)": "market_indices_user",
    "Currencies (User)": "currencies_user",
    "Cryptocurrency (User)": "cryptocurrencies_user",
    "Commodities (User)": "commodities_user",
    "ETFs - Popular (User)": "etf_popular_user",
    "ETFs - Sectors (User)": "etf_sectors_user",
    "ETFs - Countries (User)": "etf_countries_user",
    "Short-Term Bonds (User)": "short_term_bonds_user",
    "Long-Term Bonds (User)": "long_term_bonds_user",
}

# -------------------------------------------------------------------------------------------------
# Cleanup suffixes for display
# -------------------------------------------------------------------------------------------------
ASSET_NAME_CLEANUP = [
    " Stock Price History",
    " Historical Data",
    " Prices",
    " Dataset"
]

# -------------------------------------------------------------------------------------------------
# Utility Function to Clean Display Labels
# -------------------------------------------------------------------------------------------------
def clean_asset_label(name: str) -> str:
    """
    Remove common suffixes from filenames to produce user-friendly labels.

    Args:
        name (str): Raw filename without extension.

    Returns:
        str: Cleaned display name.
    """
    for suffix in ASSET_NAME_CLEANUP:
        if name.endswith(suffix):
            name = name.replace(suffix, "").strip()
    return name

# -------------------------------------------------------------------------------------------------
# Function: get_user_preloaded_assets
# Purpose: Returns user asset labels for dropdowns (cleaned names), mapped to raw filenames
# -------------------------------------------------------------------------------------------------
def get_user_preloaded_assets() -> dict:
    """
    Constructs a dictionary of user-defined assets for dropdown display.

    Structure:
        {
            "Commodities (User)": {
                "Gold": "Gold Futures Historical Data",
                ...
            },
            ...
        }

    Only includes `.csv` files. Removes known suffixes in UI, but preserves full path logic.

    Returns:
        dict: Category → { cleaned name → original file name (no .csv) }
    """
    result = {}
    for category_label, folder_name in USER_CATEGORY_MAP.items():
        folder_path = os.path.join(USER_DATA_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        name_map = {}
        for file in os.listdir(folder_path):
            if file.lower().endswith(".csv"):
                raw_name = os.path.splitext(file)[0]
                cleaned_name = clean_asset_label(raw_name)
                name_map[cleaned_name] = raw_name

        if name_map:
            result[category_label] = name_map

    return result
