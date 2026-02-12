"""
Helper Module: Asset Name Cleaner

Standardises asset filenames by removing known suffixes and irrelevant extensions.
Used across modules such as Asset Snapshot Scanner and User Asset Manager to ensure
clarity and consistency in UI presentation.

Suffix cleaning logic is handled via SUFFIX_REPLACEMENTS.
MARKET_DATA_PROVIDERS lists common sources used with the platform.
"""

# -------------------------------------------------------------------------------------------------
# Active Cleaning Logic — Used in filename and asset label processing
# -------------------------------------------------------------------------------------------------
SUFFIX_REPLACEMENTS = {
    " Stock Price History": "",     # Investing.com
    " Historical Data": "",         # Investing.com
    "_TV.csv": "",                  # TradingView (example)

    # File extensions and system files
    ".csv": "",
    ".txt": "",
    ".DS_Store": "",
}

def clean_asset_name(filename: str) -> str:
    """
    Cleans an asset filename by removing known suffixes and extensions.

    Args:
        filename (str): Original filename (e.g., "Tesla Stock Price History.csv")

    Returns:
        str: Cleaned asset name (e.g., "Tesla")
    """
    name = filename
    for suffix, replacement in SUFFIX_REPLACEMENTS.items():
        name = name.replace(suffix, replacement)
    return name.strip()

# -------------------------------------------------------------------------------------------------
# Reference: Market Data Providers — Used in sidebar guidance or metadata panels
# -------------------------------------------------------------------------------------------------
MARKET_DATA_PROVIDERS = {
    "Investing.com": {
        "url": "https://www.investing.com/"
    }
}
