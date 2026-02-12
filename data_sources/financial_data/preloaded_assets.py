# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Preloaded Asset Definitions

Provides a predefined dictionary of asset groupings used across multiple decision-support modules.
These asset lists are surfaced when users select "Preloaded Asset Types" from the sidebar input.

Used in:
- 02_🔎_Market_and_Volatility_Scanner.py
- 03_⏳_Trade_Timing_and_Confirmation.py
- 04_📊_Price_Action_and_Trend_Confirmation.py

Located in `/apps/data_sources/` for clear alignment with other structured data inputs.
"""

# -------------------------------------------------------------------------------------------------
# Function: get_preloaded_assets
# Purpose: Returns asset categories used in 'Preloaded Asset Types'
# -------------------------------------------------------------------------------------------------
def get_preloaded_assets():
    """
    Returns a dictionary of preloaded asset categories and their respective assets.

    This function defines the set of assets available under the 'Preloaded Asset Types'
    selection in Streamlit-based applications. It is used to populate dropdown menus
    and validation logic for category-based asset loading.

    Structure:
        Dict[str, List[str]]: Mapping of asset category to available asset names.

    Returns:
        dict: Structured mapping of asset categories to list of asset identifiers.
    """
    return {
        "Equities - Magnificent Seven": [
            "Tesla", "Alphabet A", "Amazon", "Apple", "Meta Platforms", "Microsoft", "NVIDIA"
        ],
    }
