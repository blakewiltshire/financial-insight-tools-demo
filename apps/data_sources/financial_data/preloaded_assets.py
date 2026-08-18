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
- 02_Market_and_Volatility_Scanner.py
- 03_Trade_Timing_and_Confirmation.py
- 04_Price_Action_and_Trend_Confirmation.py

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
        "Equities - Sector Constituents": [
            "Walt Disney Company (Communication Services)", "Home Depot (Consumer Discretionary)",
            "Coca-Cola (Consumer Staples)", "Exxon Mobil (Energy)", "Visa (Financials)",
            "Pfizer (Health Care)", "Boeing Co (Industrials)", "Linde Plc (Materials)",
            "Prologis Inc (Real Estate)", "Oracle Corp (Technology)",
            "NextEra Energy Inc (Utilities)" # "SpaceX (Communication Services)"
        ],
        "Market Indices": [
            "VIX", "Euro Stoxx 50", "FTSE 100", "MSCI World", "Nasdaq 100", "S&P 500",
            "US Small Cap 2000", "US Dollar Index", "Dow Jones Industrial Average"
        ],
        "Currencies": [
            "EUR_USD", "USD_CAD", "USD_GBP", "USD_JPY", "USD_SEK"
        ],
        "Cryptocurrency": [
            "Bitcoin", "Dogecoin", "Ethereum", "Litecoin", "XRP"
        ],
        "Commodities": [
            "Brent Oil", "Copper", "Crude Oil", "Gold", "Natural Gas", "Platinum",
            "Silver", "US Coffee", "US Wheat"
        ],
        "ETFs - Popular": [
            "S&P GSCI Commodity-Indexed Trust", "SPY S&P 500",
            "Vanguard FTSE Developed Markets Index", "iShares MSCI Emerging Markets ETF", "Invesco QQQ Trust",
            "MSCI USA Min Vol Factor", "Vanguard Total Stock Market Index",
            "S&P MIDCAP 400 ETF Trust", "SPDR S&P 600 Small Cap ETF", "iShares Core U.S. Aggregate Bond ETF",
            "iShares TIPS Bond ETF", "State Street SPDR Bloomberg 1-3 Month T-Bill ETF",
            "Vanguard Real Estate Index Fund ETF Shares"
        ],
        "ETFs - Sectors": [
            "Communication Services", "Consumer Discretionary", "Consumer Staples", "Energy",
            "Financials", "Health Care", "Industrials", "Materials", "Real Estate", "Technology",
            "Utilities"
        ],
        "ETFs - Countries": [
            "United States", "Australia", "Canada", "France", "Germany", "Hong Kong", "India",
            "Israel", "Italy", "Japan", "South Korea", "Spain", "Switzerland", "United Kingdom"
        ],
        "Short-Term Bonds": [
            "Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"
        ],
        "Long-Term Bonds": [
            "Canada", "France", "Germany", "Italy", "Japan", "United Kingdom", "United States"
        ],
    }
