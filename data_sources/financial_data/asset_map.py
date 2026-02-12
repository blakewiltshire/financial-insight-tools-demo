# -------------------------------------------------------------------------------------------------
# Pylint Global Exceptions
# -------------------------------------------------------------------------------------------------
# pylint: disable=unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Global Asset Map

Centralised dictionary that maps asset categories and names to file paths.
Used across all modules for price-action, volatility, return, and correlation analysis.
"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
from .path_utils import resolve_data_file_path

# -------------------------------------------------------------------------------------------------
# Resolve Data file to Asset
# -------------------------------------------------------------------------------------------------
asset_files = {
    "Equities - Magnificent Seven": {
        "Tesla": resolve_data_file_path("equities_mag7", "Tesla Stock Price History.csv"),#tsla - https://www.investing.com/equities/tesla-motors-historical-data
        "Alphabet A": resolve_data_file_path("equities_mag7", "Alphabet A Stock Price History.csv"),#googl - https://www.investing.com/equities/google-inc-historical-data
        "Amazon": resolve_data_file_path("equities_mag7", "Amazon.com Stock Price History.csv"),#amzn - https://www.investing.com/equities/amazon-com-inc-historical-data
        "Apple": resolve_data_file_path("equities_mag7", "Apple Stock Price History.csv"),#appl - https://www.investing.com/equities/apple-computer-inc-historical-data
        "Meta Platforms": resolve_data_file_path(
        "equities_mag7", "Meta Platforms Stock Price History.csv"),#meta - https://www.investing.com/equities/facebook-inc-historical-data
        "Microsoft": resolve_data_file_path("equities_mag7", "Microsoft Stock Price History.csv"),#msft - https://www.investing.com/equities/microsoft-corp-historical-data
        "NVIDIA": resolve_data_file_path("equities_mag7", "NVIDIA Stock Price History.csv"),#nvda - https://www.investing.com/equities/nvidia-corp-historical-data
    },
    "Equities - Sector Constituents": {
        "Boeing Co (Industrials)": resolve_data_file_path(
        "equities_constituents", "Boeing Stock Price History.csv"),#ba - https://www.investing.com/equities/boeing-co-historical-data
        "Coca-Cola (Consumer Staples)": resolve_data_file_path(
        "equities_constituents", "Coca-Cola Stock Price History.csv"),#ko - https://www.investing.com/equities/coca-cola-co-historical-data
        "Exxon Mobil (Energy)": resolve_data_file_path(
        "equities_constituents", "Exxon Mobil Stock Price History.csv"),#xom - https://www.investing.com/equities/exxon-mobil-historical-data
        "Home Depot (Consumer Discretionary)": resolve_data_file_path(
        "equities_constituents", "Home Depot Stock Price History.csv"),#hd - https://www.investing.com/equities/home-depot-historical-data
        "Linde Plc (Materials)": resolve_data_file_path(
        "equities_constituents", "Linde PLC Stock Price History.csv"),#lin - https://www.investing.com/equities/linde-plc-historical-data?cid=1208282
        "NextEra Energy Inc (Utilities)": resolve_data_file_path(
        "equities_constituents", "NextEra Energy Stock Price History.csv"),#nee - https://www.investing.com/equities/nextera-energy-inc-historical-data
        "Oracle Corp (Technology)": resolve_data_file_path(
        "equities_constituents", "Oracle Stock Price History.csv"),#orcl - https://www.investing.com/equities/oracle-corp-historical-data
        "Pfizer (Health Care)": resolve_data_file_path(
        "equities_constituents", "Pfizer Stock Price History.csv"),#pfe - https://www.investing.com/equities/pfizer-historical-data
        "Prologis Inc (Real Estate)": resolve_data_file_path(
        "equities_constituents", "Prologis Stock Price History.csv"),#pld - https://www.investing.com/equities/prologis-historical-data
        "Visa (Financials)": resolve_data_file_path(
        "equities_constituents", "Visa A Stock Price History.csv"),#v - https://www.investing.com/equities/visa-inc-historical-data
        "Walt Disney Company (Communication Services)": resolve_data_file_path(
        "equities_constituents", "Walt Disney Stock Price History.csv"),#dis - https://www.investing.com/equities/disney-historical-data
    },
    "Market Indices": {
        "VIX": resolve_data_file_path(
        "market_indices", "CBOE Volatility Index Historical Data.csv"),#VIX - https://www.investing.com/indices/volatility-s-p-500-historical-data
        "Euro Stoxx 50": resolve_data_file_path(
        "market_indices", "Euro Stoxx 50 Historical Data.csv"),# - https://www.investing.com/indices/eu-stoxx50-historical-data
        "FTSE 100": resolve_data_file_path(
        "market_indices", "FTSE 100 Historical Data.csv"),#uk100 - https://www.investing.com/indices/uk-100-historical-data
        "MSCI World": resolve_data_file_path(
        "market_indices", "MSCI World Historical Data.csv"),#MIWO00000PUS - https://www.investing.com/indices/msci-world-historical-data
        "Nasdaq 100": resolve_data_file_path(
        "market_indices", "Nasdaq 100 Historical Data.csv"),#ndx - https://www.investing.com/indices/nq-100-historical-data
        "S&P 500": resolve_data_file_path(
        "market_indices", "S&P 500 Historical Data.csv"), #us-spx-500 - https://www.investing.com/indices/us-spx-500-historical-data
        "US Small Cap 2000": resolve_data_file_path(
        "market_indices", "US Small Cap 2000 Historical Data.csv"), #US2000 - https://www.investing.com/indices/smallcap-2000-historical-data
        "US Dollar Index": resolve_data_file_path(
        "market_indices", "US Dollar Index Historical Data.csv"), #DXY - https://www.investing.com/indices/usdollar-historical-data?cid=1224074
        "Dow Jones Industrial Average": resolve_data_file_path(
        "market_indices", "Dow Jones Industrial Average Historical Data.csv"), #DJI - https://www.investing.com/indices/us-30-historical-data
    },
    "Currencies": {
        "EUR_USD": resolve_data_file_path("currencies", "EUR_USD Historical Data.csv"), #EUR/USD - https://www.investing.com/currencies/eur-usd-historical-data
        "USD_CAD": resolve_data_file_path("currencies", "USD_CAD Historical Data.csv"), #USD/CAD - https://www.investing.com/currencies/usd-cad-historical-data
        "USD_GBP": resolve_data_file_path("currencies", "USD_GBP Historical Data.csv"), #USD/GBP - https://www.investing.com/currencies/usd-gbp-historical-data
        "USD_JPY": resolve_data_file_path("currencies", "USD_JPY Historical Data.csv"), #USD/JPY - https://www.investing.com/currencies/usd-jpy-historical-data
        "USD_SEK": resolve_data_file_path("currencies", "USD_SEK Historical Data.csv"), #USD/SEK - https://www.investing.com/currencies/usd-sek-historical-data
    },
    "Cryptocurrency": {
        "Bitcoin": resolve_data_file_path("cryptocurrencies", "Bitcoin Historical Data.csv"), #BTC/USD - https://www.investing.com/indices/investing.com-btc-usd-historical-data
        "Dogecoin": resolve_data_file_path("cryptocurrencies", "Dogecoin Historical Data.csv"), #DOGE/USD - https://www.investing.com/indices/investing.com-doge-usd-historical-data
        "Ethereum": resolve_data_file_path("cryptocurrencies", "Ethereum Historical Data.csv"), #ETH/USD - https://www.investing.com/indices/investing.com-eth-usd-historical-data
        "Litecoin": resolve_data_file_path("cryptocurrencies", "Litecoin Historical Data.csv"), #LTC/USD - https://www.investing.com/crypto/litecoin/historical-data
        "XRP": resolve_data_file_path("cryptocurrencies", "XRP Historical Data.csv"), #XRP/USD - https://www.investing.com/crypto/xrp/historical-data
    },
    "Commodities": {
        "Brent Oil": resolve_data_file_path(
        "commodities", "Brent Oil Futures Historical Data.csv"),# - https://www.investing.com/commodities/brent-oil-historical-data
        "Copper": resolve_data_file_path(
        "commodities", "Copper Futures Historical Data.csv"),#HG - https://www.investing.com/commodities/copper-historical-data
        "Crude Oil": resolve_data_file_path(
        "commodities", "Crude Oil WTI Futures Historical Data.csv"),#CL - https://www.investing.com/commodities/crude-oil-historical-data
        "Gold": resolve_data_file_path(
        "commodities", "Gold Futures Historical Data.csv"),#GC - https://www.investing.com/commodities/gold-historical-data
        "Natural Gas": resolve_data_file_path(
        "commodities", "Natural Gas Futures Historical Data.csv"),#NG - https://www.investing.com/commodities/natural-gas-historical-data
        "Platinum": resolve_data_file_path(
        "commodities", "Platinum Futures Historical Data.csv"),#PL - https://www.investing.com/commodities/platinum-historical-data
        "Silver": resolve_data_file_path(
        "commodities", "Silver Futures Historical Data.csv"),#SI - https://www.investing.com/commodities/silver-historical-data
        "US Coffee": resolve_data_file_path(
        "commodities", "US Coffee C Futures Historical Data.csv"),#KC - https://www.investing.com/commodities/us-coffee-c-historical-data
        "US Wheat": resolve_data_file_path(
        "commodities", "US Wheat Futures Historical Data.csv"),#ZW - https://www.investing.com/commodities/us-wheat-historical-data
    },
    "ETFs - Popular": {
        "ARK Innovation": resolve_data_file_path(
        "etf_popular", "ARKK ETF Stock Price History.csv"),#ARKK - https://www.investing.com/etfs/ark-innovation-historical-data
        "S&P GSCI Commodity-Indexed Trust": resolve_data_file_path(
        "etf_popular", "GSG ETF Stock Price History.csv"),#GSG - https://www.investing.com/etfs/ishares-s-p-gsci-commod-historical-data
        "SPY S&P 500": resolve_data_file_path(
        "etf_popular", "SPY ETF Stock Price History.csv"),#SPY - https://www.investing.com/etfs/spdr-s-p-500-historical-data
        "Vanguard FTSE Developed Markets Index": resolve_data_file_path(
        "etf_popular", "VEA ETF Stock Price History.csv"),#VEA - https://www.investing.com/etfs/vanguard-europe-pacific-historical-data
        "MSCI Emerging Markets": resolve_data_file_path(
        "etf_popular", "EEM ETF Stock Price History.csv"),#EEM - https://www.investing.com/etfs/ishares-msci-emg-markets-historical-data
        "Invesco QQQ Trust": resolve_data_file_path(
        "etf_popular", "QQQ ETF Stock Price History.csv"),#QQQ - https://www.investing.com/etfs/powershares-qqqq-historical-data
        "MSCI USA Min Vol Factor": resolve_data_file_path(
        "etf_popular", "USMV ETF Stock Price History.csv"),#USMV - https://www.investing.com/etfs/ishares-msci-usa-min-volatility-historical-data
        "Vanguard Total Stock Market Index": resolve_data_file_path(
        "etf_popular", "VTI ETF Stock Price History.csv"),#VTI - https://www.investing.com/etfs/vanguard-total-stkmkt-historical-data
    },
    "ETFs - Sectors": {
        "Communication Services": resolve_data_file_path(
        "etf_sectors", "XLC ETF Stock Price History.csv"),#XLC - https://www.investing.com/etfs/communication-services-select-spdr-historical-data
        "Consumer Discretionary": resolve_data_file_path(
        "etf_sectors", "XLY ETF Stock Price History.csv"),#XLY - https://www.investing.com/etfs/spdr-consumer-discr.-select-sector-historical-data
        "Consumer Staples": resolve_data_file_path(
        "etf_sectors", "XLP ETF Stock Price History.csv"),#XLP - https://www.investing.com/etfs/spdr---consumer-staples-historical-data
        "Energy": resolve_data_file_path("etf_sectors", "XLE ETF Stock Price History.csv"),#XLE - https://www.investing.com/etfs/spdr-energy-select-sector-fund-historical-data
        "Financials": resolve_data_file_path("etf_sectors", "XLF ETF Stock Price History.csv"),#XLF - https://www.investing.com/etfs/financial-select-sector-spdr-fund-historical-data
        "Health Care": resolve_data_file_path("etf_sectors", "XLV ETF Stock Price History.csv"),#XLV - https://www.investing.com/etfs/spdr---health-care-historical-data
        "Industrials": resolve_data_file_path("etf_sectors", "XLI ETF Stock Price History.csv"),#XLI - https://www.investing.com/etfs/industrial-sector-spdr-trust-historical-data
        "Materials": resolve_data_file_path("etf_sectors", "XLB ETF Stock Price History.csv"),#XLB - https://www.investing.com/etfs/spdr-materials-select-sector-etf-historical-data
        "Real Estate": resolve_data_file_path("etf_sectors", "XLRE ETF Stock Price History.csv"),#XLRE - https://www.investing.com/etfs/real-estate-select-sector-spdr-historical-data
        "Technology": resolve_data_file_path("etf_sectors", "XLK ETF Stock Price History.csv"),#XLK - https://www.investing.com/etfs/spdr-select-sector---technology-historical-data
        "Utilities": resolve_data_file_path("etf_sectors", "XLU ETF Stock Price History.csv"),#XLU - https://www.investing.com/etfs/spdr-select-sector---utilities-historical-data
    },
    "ETFs - Countries": {
        "Unites States": resolve_data_file_path(
        "etf_countries", "EUSA ETF Stock Price History.csv"),#EUSA - https://www.investing.com/etfs/ishares-msci-usa-historical-data
        "Australia": resolve_data_file_path("etf_countries", "EWA ETF Stock Price History.csv"),#EWA - https://www.investing.com/etfs/ishares-msci-australia-index-historical-data
        "Canada": resolve_data_file_path("etf_countries", "EWC ETF Stock Price History.csv"),#EWC - https://www.investing.com/etfs/ishares-msci-canada-historical-data
        "France": resolve_data_file_path("etf_countries", "EWQ ETF Stock Price History.csv"),#EWQ - https://www.investing.com/etfs/ishares-msci-france-historical-data
        "Germany": resolve_data_file_path("etf_countries", "EWG ETF Stock Price History.csv"),#EWG - https://www.investing.com/etfs/ishare-msci-germany-historical-data
        "Hong Kong": resolve_data_file_path("etf_countries", "EWH ETF Stock Price History.csv"),#EWH - https://www.investing.com/etfs/ishares-msci-hong-kong-historical-data
        "India": resolve_data_file_path("etf_countries", "INDY ETF Stock Price History.csv"),#INDY - https://www.investing.com/etfs/s-p-india-nifty-fifty-historical-data
        "Israel": resolve_data_file_path("etf_countries", "EIS ETF Stock Price History.csv"),#EIS - https://www.investing.com/etfs/ishares-msci-israel-cap-inv.-mrkt-historical-data
        "Italy": resolve_data_file_path("etf_countries", "EWI ETF Stock Price History.csv"),#EWI - https://www.investing.com/etfs/ishares-msci-italy-capped-fund-historical-data
        "Japan": resolve_data_file_path("etf_countries", "EWJ ETF Stock Price History.csv"),#EWJ - https://www.investing.com/etfs/ishares-msci-japan-historical-data
        "South Korea": resolve_data_file_path("etf_countries", "EWY ETF Stock Price History.csv"),#EWY - https://www.investing.com/etfs/ishares-south-korea-index-historical-data
        "Spain": resolve_data_file_path("etf_countries", "EWP ETF Stock Price History.csv"),#EWP - https://www.investing.com/etfs/ishares-msci-spain-historical-data
        "Switzerland": resolve_data_file_path("etf_countries", "EWL ETF Stock Price History.csv"),#EWL - https://www.investing.com/etfs/ishares-msci-switzerland-index-historical-data
        "United Kingdom": resolve_data_file_path(
        "etf_countries", "EWU ETF Stock Price History.csv"),#EWU - https://www.investing.com/etfs/ishares-msci-uk-historical-data
    },
    "Short-Term Bonds": {
        "Canada": resolve_data_file_path(
        "short_term_bonds", "Canada 2-Year Bond Yield Historical Data.csv"),#CA2YT=RR - https://www.investing.com/rates-bonds/canada-2-year-bond-yield-historical-data
        "France": resolve_data_file_path(
        "short_term_bonds", "France 2-Year Bond Yield Historical Data.csv"),#FR2YT=RR - https://www.investing.com/rates-bonds/france-2-year-bond-yield-historical-data
        "Germany": resolve_data_file_path(
        "short_term_bonds", "Germany 2-Year Bond Yield Historical Data.csv"),#DE2YT=RR - https://www.investing.com/rates-bonds/germany-2-year-bond-yield-historical-data
        "Italy": resolve_data_file_path(
        "short_term_bonds", "Italy 2-Year Bond Yield Historical Data.csv"),#IT2YT=RR - https://www.investing.com/rates-bonds/italy-2-year-bond-yield-historical-data
        "Japan": resolve_data_file_path(
        "short_term_bonds", "Japan 2-Year Bond Yield Historical Data.csv"),#JP2YT=XX - https://www.investing.com/rates-bonds/japan-2-year-bond-yield-historical-data
        "United Kingdom": resolve_data_file_path(
        "short_term_bonds", "United Kingdom 2-Year Bond Yield Historical Data.csv"),#GB2YT=RR - https://www.investing.com/rates-bonds/uk-2-year-bond-yield-historical-data
        "United States": resolve_data_file_path(
        "short_term_bonds", "United States 2-Year Bond Yield Historical Data.csv"),#US2YT=X - https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield-historical-data
    },
    "Long-Term Bonds": {
        "Canada": resolve_data_file_path(
        "long_term_bonds", "Canada 10-Year Bond Yield Historical Data.csv"),#CA10YT=RR - https://www.investing.com/rates-bonds/canada-10-year-bond-yield-historical-data
        "France": resolve_data_file_path(
        "long_term_bonds", "France 10-Year Bond Yield Historical Data.csv"),#FR10YT=RR - https://www.investing.com/rates-bonds/france-10-year-bond-yield-historical-data
        "Germany": resolve_data_file_path(
        "long_term_bonds", "Germany 10-Year Bond Yield Historical Data.csv"),#DE10YT=RR - https://www.investing.com/rates-bonds/germany-10-year-bond-yield-historical-data
        "Italy": resolve_data_file_path(
        "long_term_bonds", "Italy 10-Year Bond Yield Historical Data.csv"),#IT10YT=RR - https://www.investing.com/rates-bonds/italy-10-year-bond-yield-historical-data
        "Japan": resolve_data_file_path(
        "long_term_bonds", "Japan 10-Year Bond Yield Historical Data.csv"),#JP10YT=XX - https://www.investing.com/rates-bonds/japan-10-year-bond-yield-historical-data
        "United Kingdom": resolve_data_file_path(
        "long_term_bonds", "United Kingdom 10-Year Bond Yield Historical Data.csv"),#GB10YT=RR - https://www.investing.com/rates-bonds/uk-10-year-bond-yield-historical-data
        "United States": resolve_data_file_path(
        "long_term_bonds", "United States 10-Year Bond Yield Historical Data.csv"),#US10YT=X - https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data
    },
}

# -------------------------------------------------------------------------------------------------
# Retrieve full file path
# -------------------------------------------------------------------------------------------------
def get_asset_path(category: str, name: str) -> str:
    """
    Retrieve full file path for an asset based on its category and name.

    Parameters:
    - category (str): Asset category (e.g., 'Equities - Magnificent Seven')
    - name (str): Asset name (e.g., 'Tesla')

    Returns:
    - str: File path to CSV data file
    """
    return asset_files.get(category, {}).get(name, None)
