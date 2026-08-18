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
Relative Macro Transmission
Positioning & Crowding

Note: Do not uncomment. asset_files is used across the Trade & Portfolio Structuring Modules.
The # commented out files are so we have the source indicator name and file paths in one place.
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
        "market_indices", "CBOE Volatility Index Historical Data.csv"),#VIX - https://www.investing.com/indices/volatility-s-p-500-historical-data - Daily (Financials) and Monthly (US - Economics)
        "Euro Stoxx 50": resolve_data_file_path(
        "market_indices", "Euro Stoxx 50 Historical Data.csv"),#STOXX50E - https://www.investing.com/indices/eu-stoxx50-historical-data - Daily (Financials) and Monthly (Euro Area - Economics)
        "FTSE 100": resolve_data_file_path(
        "market_indices", "FTSE 100 Historical Data.csv"),#uk100 - https://www.investing.com/indices/uk-100-historical-data - Daily (Financials) and Monthly (UK - Economics)
        "MSCI World": resolve_data_file_path(
        "market_indices", "MSCI World Historical Data.csv"),#MIWO00000PUS - https://www.investing.com/indices/msci-world-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Nasdaq 100": resolve_data_file_path(
        "market_indices", "Nasdaq 100 Historical Data.csv"),#ndx - https://www.investing.com/indices/nq-100-historical-data - Daily (Financials) and Monthly (US - Economics)
        "S&P 500": resolve_data_file_path(
        "market_indices", "S&P 500 Historical Data.csv"), #us500 - https://www.investing.com/indices/us-spx-500-historical-data - Daily (Financials) and Monthly (US - Economics)
        "US Small Cap 2000": resolve_data_file_path(
        "market_indices", "US Small Cap 2000 Historical Data.csv"), #US2000 - https://www.investing.com/indices/smallcap-2000-historical-data - Daily (Financials) and Monthly (US - Economics)
        "US Dollar Index": resolve_data_file_path(
        "market_indices", "US Dollar Index Historical Data.csv"), #DXY - https://www.investing.com/indices/usdollar-historical-data?cid=1224074 - Daily (Financials) and Monthly (US - Economics)
        "Dow Jones Industrial Average": resolve_data_file_path(
        "market_indices", "Dow Jones Industrial Average Historical Data.csv"), #DJI - https://www.investing.com/indices/us-30-historical-data - Daily (Financials) and Monthly (US - Economics)
    },
    "Currencies": {
        "EUR_USD": resolve_data_file_path("currencies", "EUR_USD Historical Data.csv"), #EUR/USD - https://www.investing.com/currencies/eur-usd-historical-data - Daily (Financials) and Monthly (World - Economics)
        "USD_CAD": resolve_data_file_path("currencies", "USD_CAD Historical Data.csv"), #USD/CAD - https://www.investing.com/currencies/usd-cad-historical-data - Daily (Financials) and Monthly (World - Economics)
        "USD_GBP": resolve_data_file_path("currencies", "USD_GBP Historical Data.csv"), #USD/GBP - https://www.investing.com/currencies/usd-gbp-historical-data
        "USD_JPY": resolve_data_file_path("currencies", "USD_JPY Historical Data.csv"), #USD/JPY - https://www.investing.com/currencies/usd-jpy-historical-data - Daily (Financials) and Monthly (World - Economics)
        "USD_SEK": resolve_data_file_path("currencies", "USD_SEK Historical Data.csv"), #USD/SEK - https://www.investing.com/currencies/usd-sek-historical-data
    },

    #GBP/USD -  https://www.investing.com/currencies/gbp-usd-historical-data - Monthly (World - Economics)
    #USD/CHF -  https://www.investing.com/currencies/usd-chf-historical-data - Monthly (World - Economics)
    #AUD/USD -  https://www.investing.com/currencies/aud-usd-historical-data - Monthly (World - Economics)
    #NZD/USD -  https://www.investing.com/currencies/nzd-usd-historical-data - Monthly (World - Economics)
    #USD/NOK -  https://www.investing.com/currencies/usd-nok-historical-data - Monthly (World - Economics)
    #USD/CNY -  https://www.investing.com/currencies/usd-cny-historical-data - Monthly (World - Economics)
    #USD/HKD -  https://www.investing.com/currencies/usd-hkd-historical-data - Monthly (World - Economics)
    #USD/SGD -  https://www.investing.com/currencies/usd-sgd-historical-data - Monthly (World - Economics)
    #USD/INR -  https://www.investing.com/currencies/usd-inr-historical-data - Monthly (World - Economics)
    #USD/BRL -  https://www.investing.com/currencies/usd-brl-historical-data - Monthly (World - Economics)
    #USD/MXN -  https://www.investing.com/currencies/usd-mxn-historical-data - Monthly (World - Economics)
    #USD/ZAR -  https://www.investing.com/currencies/usd-zar-historical-data - Monthly (World - Economics)
    #EUR/GBP -  https://www.investing.com/currencies/eur-gbp-historical-data - Monthly (World - Economics)
    #EUR/JPY -  https://www.investing.com/currencies/eur-jpy-historical-data - Monthly (World - Economics)
    #AUD/JPY -  https://www.investing.com/currencies/aud-jpy-historical-data - Monthly (World - Economics)


    "Cryptocurrency": {
        "Bitcoin": resolve_data_file_path("cryptocurrencies", "Bitcoin Historical Data.csv"), #BTC/USD - https://www.investing.com/indices/investing.com-btc-usd-historical-data
        "Dogecoin": resolve_data_file_path("cryptocurrencies", "Dogecoin Historical Data.csv"), #DOGE/USD - https://www.investing.com/indices/investing.com-doge-usd-historical-data
        "Ethereum": resolve_data_file_path("cryptocurrencies", "Ethereum Historical Data.csv"), #ETH/USD - https://www.investing.com/indices/investing.com-eth-usd-historical-data
        "Litecoin": resolve_data_file_path("cryptocurrencies", "Litecoin Historical Data.csv"), #LTC/USD - https://www.investing.com/crypto/litecoin/historical-data
        "XRP": resolve_data_file_path("cryptocurrencies", "XRP Historical Data.csv"), #XRP/USD - https://www.investing.com/crypto/xrp/historical-data
    },
    "Commodities": {
        "Brent Oil": resolve_data_file_path(
        "commodities", "Brent Oil Futures Historical Data.csv"),#LCO - https://www.investing.com/commodities/brent-oil-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Copper": resolve_data_file_path(
        "commodities", "Copper Futures Historical Data.csv"),#HG - https://www.investing.com/commodities/copper-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Crude Oil": resolve_data_file_path(
        "commodities", "Crude Oil WTI Futures Historical Data.csv"),#CL - https://www.investing.com/commodities/crude-oil-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Gold": resolve_data_file_path(
        "commodities", "Gold Futures Historical Data.csv"),#GC - https://www.investing.com/commodities/gold-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Natural Gas": resolve_data_file_path(
        "commodities", "Natural Gas Futures Historical Data.csv"),#NG - https://www.investing.com/commodities/natural-gas-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Platinum": resolve_data_file_path(
        "commodities", "Platinum Futures Historical Data.csv"),#PL - https://www.investing.com/commodities/platinum-historical-data - Daily (Financials) and Monthly (World - Economics)
        "Silver": resolve_data_file_path(
        "commodities", "Silver Futures Historical Data.csv"),#SI - https://www.investing.com/commodities/silver-historical-data - Daily (Financials) and Monthly (World - Economics)
        "US Coffee": resolve_data_file_path(
        "commodities", "US Coffee C Futures Historical Data.csv"),#KC - https://www.investing.com/commodities/us-coffee-c-historical-data - Daily (Financials) and Monthly (World - Economics)
        "US Wheat": resolve_data_file_path(
        "commodities", "US Wheat Futures Historical Data.csv"),#ZW - https://www.investing.com/commodities/us-wheat-historical-data - Daily (Financials) and Monthly (World - Economics)
    },
    "ETFs - Popular": {
        "S&P GSCI Commodity-Indexed Trust": resolve_data_file_path(
        "etf_popular", "GSG ETF Stock Price History.csv"),#GSG - https://www.investing.com/etfs/ishares-s-p-gsci-commod-historical-data
        "SPY S&P 500": resolve_data_file_path(
        "etf_popular", "SPY ETF Stock Price History.csv"),#SPY - https://www.investing.com/etfs/spdr-s-p-500-historical-data
        "Vanguard FTSE Developed Markets Index": resolve_data_file_path(
        "etf_popular", "VEA ETF Stock Price History.csv"),#VEA - https://www.investing.com/etfs/vanguard-europe-pacific-historical-data
        "iShares MSCI Emerging Markets ETF": resolve_data_file_path(
        "etf_popular", "EEM ETF Stock Price History.csv"),#EEM - https://www.investing.com/etfs/ishares-msci-emg-markets-historical-data
        "Invesco QQQ Trust": resolve_data_file_path(
        "etf_popular", "QQQ ETF Stock Price History.csv"),#QQQ - https://www.investing.com/etfs/powershares-qqqq-historical-data
        "MSCI USA Min Vol Factor": resolve_data_file_path(
        "etf_popular", "USMV ETF Stock Price History.csv"),#USMV - https://www.investing.com/etfs/ishares-msci-usa-min-volatility-historical-data
        "Vanguard Total Stock Market Index": resolve_data_file_path(
        "etf_popular", "VTI ETF Stock Price History.csv"),#VTI - https://www.investing.com/etfs/vanguard-total-stkmkt-historical-data
        "S&P MIDCAP 400 ETF Trust": resolve_data_file_path(
        "etf_popular", "MDY ETF Stock Price History.csv"),#MDY - https://www.investing.com/etfs/spdr-midcap-trust-series-i-historical-data
        "SPDR S&P 600 Small Cap ETF": resolve_data_file_path(
        "etf_popular", "SLY ETF Stock Price History.csv"),#SLY - https://www.investing.com/etfs/spdr-s-p-600-small-cap-historical-data
        "iShares Core U.S. Aggregate Bond ETF": resolve_data_file_path(
        "etf_popular", "AGG ETF Stock Price History.csv"),#AGG - https://www.investing.com/etfs/ishares-barclays-agg-historical-data
        "iShares TIPS Bond ETF": resolve_data_file_path(
        "etf_popular", "TIP ETF Stock Price History.csv"),#TIP - https://www.investing.com/etfs/ishares-barclays-tip-historical-data
        "State Street SPDR Bloomberg 1-3 Month T-Bill ETF": resolve_data_file_path(
        "etf_popular", "BIL ETF Stock Price History.csv"),#BIL - https://www.investing.com/etfs/spdr-lehman-1-3-month-t-bill-historical-data
        "Vanguard Real Estate Index Fund ETF Shares": resolve_data_file_path(
        "etf_popular", "VNQ ETF Stock Price History.csv"),#VNQ - https://www.investing.com/etfs/vanguard-reit-historical-data
    },
    "ETFs - Sectors": {
        "Communication Services": resolve_data_file_path(
        "etf_sectors", "XLC ETF Stock Price History.csv"),#XLC - https://www.investing.com/etfs/communication-services-select-spdr-historical-data - (Financials) and Monthly (US - Economics)
        "Consumer Discretionary": resolve_data_file_path(
        "etf_sectors", "XLY ETF Stock Price History.csv"),#XLY - https://www.investing.com/etfs/spdr-consumer-discr.-select-sector-historical-data - (Financials) and Monthly (US - Economics)
        "Consumer Staples": resolve_data_file_path(
        "etf_sectors", "XLP ETF Stock Price History.csv"),#XLP - https://www.investing.com/etfs/spdr---consumer-staples-historical-data - (Financials) and Monthly (US - Economics)
        "Energy": resolve_data_file_path("etf_sectors", "XLE ETF Stock Price History.csv"),#XLE - https://www.investing.com/etfs/spdr-energy-select-sector-fund-historical-data - (Financials) and Monthly (US - Economics)
        "Financials": resolve_data_file_path("etf_sectors", "XLF ETF Stock Price History.csv"),#XLF - https://www.investing.com/etfs/financial-select-sector-spdr-fund-historical-data - (Financials) and Monthly (US - Economics)
        "Health Care": resolve_data_file_path("etf_sectors", "XLV ETF Stock Price History.csv"),#XLV - https://www.investing.com/etfs/spdr---health-care-historical-data - (Financials) and Monthly (US - Economics)
        "Industrials": resolve_data_file_path("etf_sectors", "XLI ETF Stock Price History.csv"),#XLI - https://www.investing.com/etfs/industrial-sector-spdr-trust-historical-data - (Financials) and Monthly (US - Economics)
        "Materials": resolve_data_file_path("etf_sectors", "XLB ETF Stock Price History.csv"),#XLB - https://www.investing.com/etfs/spdr-materials-select-sector-etf-historical-data - (Financials) and Monthly (US - Economics)
        "Real Estate": resolve_data_file_path("etf_sectors", "XLRE ETF Stock Price History.csv"),#XLRE - https://www.investing.com/etfs/real-estate-select-sector-spdr-historical-data - (Financials) and Monthly (US - Economics)
        "Technology": resolve_data_file_path("etf_sectors", "XLK ETF Stock Price History.csv"),#XLK - https://www.investing.com/etfs/spdr-select-sector---technology-historical-data - (Financials) and Monthly (US - Economics)
        "Utilities": resolve_data_file_path("etf_sectors", "XLU ETF Stock Price History.csv"),#XLU - https://www.investing.com/etfs/spdr-select-sector---utilities-historical-data - (Financials) and Monthly (US - Economics)
    },
    "ETFs - Countries": {
        "United States": resolve_data_file_path("etf_countries", "EUSA ETF Stock Price History.csv"), #EUSA - https://www.investing.com/etfs/ishares-msci-usa-historical-data - Daily (Financials) and Monthly (US - Economics)
        "Australia": resolve_data_file_path("etf_countries", "EWA ETF Stock Price History.csv"),#EWA - https://www.investing.com/etfs/ishares-msci-australia-index-historical-data - Daily (Financials) and Monthly (Australia - Economics)
        "Canada": resolve_data_file_path("etf_countries", "EWC ETF Stock Price History.csv"),#EWC - https://www.investing.com/etfs/ishares-msci-canada-historical-data - Daily (Financials) and Monthly (Canada - Economics)
        "France": resolve_data_file_path("etf_countries", "EWQ ETF Stock Price History.csv"),#EWQ - https://www.investing.com/etfs/ishares-msci-france-historical-data - Daily (Financials) and Monthly (France - Economics)
        "Germany": resolve_data_file_path("etf_countries", "EWG ETF Stock Price History.csv"),#EWG - https://www.investing.com/etfs/ishare-msci-germany-historical-data - Daily (Financials) and Monthly (Germany - Economics)
        "Hong Kong": resolve_data_file_path("etf_countries", "EWH ETF Stock Price History.csv"),#EWH - https://www.investing.com/etfs/ishares-msci-hong-kong-historical-data - Daily (Financials) and Monthly (Hong Kong - Economics)
        "India": resolve_data_file_path("etf_countries", "INDY ETF Stock Price History.csv"),#INDY - https://www.investing.com/etfs/s-p-india-nifty-fifty-historical-data - Daily (Financials) and Monthly (India - Economics)
        "Israel": resolve_data_file_path("etf_countries", "EIS ETF Stock Price History.csv"),#EIS - https://www.investing.com/etfs/ishares-msci-israel-cap-inv.-mrkt-historical-data - Daily (Financials) and Monthly (India - Economics)
        "Italy": resolve_data_file_path("etf_countries", "EWI ETF Stock Price History.csv"),#EWI - https://www.investing.com/etfs/ishares-msci-italy-capped-fund-historical-data - Daily (Financials) and Monthly (Israel - Economics)
        "Japan": resolve_data_file_path("etf_countries", "EWJ ETF Stock Price History.csv"),#EWJ - https://www.investing.com/etfs/ishares-msci-japan-historical-data - Daily (Financials) and Monthly (Japan - Economics)
        "South Korea": resolve_data_file_path("etf_countries", "EWY ETF Stock Price History.csv"),#EWY - https://www.investing.com/etfs/ishares-south-korea-index-historical-data - Daily (Financials) and Monthly (South Korea - Economics)
        "Spain": resolve_data_file_path("etf_countries", "EWP ETF Stock Price History.csv"),#EWP - https://www.investing.com/etfs/ishares-msci-spain-historical-data - Daily (Financials) and Monthly (Spain - Economics)
        "Switzerland": resolve_data_file_path("etf_countries", "EWL ETF Stock Price History.csv"),#EWL - https://www.investing.com/etfs/ishares-msci-switzerland-index-historical-data - Daily (Financials) and Monthly (Switzerland - Economics)
        "United Kingdom": resolve_data_file_path("etf_countries", "EWU ETF Stock Price History.csv"),#EWU - https://www.investing.com/etfs/ishares-msci-uk-historical-data  - Daily (Financials) and Monthly (UK - Economics)
    },

        # "China": resolve_data_file_path("etf_countries", "MCHI ETF Stock Price History.csv"), #MCHI - https://www.investing.com/etfs/ishares-msci-china-historical-data - Monthly (China - Economics)
        # "Brazil": resolve_data_file_path("etf_countries", "EWZ ETF Stock Price History.csv"), #EWZ - https://www.investing.com/etfs/ishares-brazil-index-historical-data - Monthly (Brazil - Economics)



    "Short-Term Bonds": {
        "Canada": resolve_data_file_path(
        "short_term_bonds", "Canada 2-Year Bond Yield Historical Data.csv"),#CA2YT=RR - https://www.investing.com/rates-bonds/canada-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (Canada - Economics)
        "France": resolve_data_file_path(
        "short_term_bonds", "France 2-Year Bond Yield Historical Data.csv"),#FR2YT=RR - https://www.investing.com/rates-bonds/france-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (France - Economics)
        "Germany": resolve_data_file_path(
        "short_term_bonds", "Germany 2-Year Bond Yield Historical Data.csv"),#DE2YT=RR - https://www.investing.com/rates-bonds/germany-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (Germany - Economics)
        "Italy": resolve_data_file_path(
        "short_term_bonds", "Italy 2-Year Bond Yield Historical Data.csv"),#IT2YT=RR - https://www.investing.com/rates-bonds/italy-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (Italy - Economics)
        "Japan": resolve_data_file_path(
        "short_term_bonds", "Japan 2-Year Bond Yield Historical Data.csv"),#JP2YT=XX - https://www.investing.com/rates-bonds/japan-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (Japan - Economics)
        "United Kingdom": resolve_data_file_path(
        "short_term_bonds", "United Kingdom 2-Year Bond Yield Historical Data.csv"),#GB2YT=RR - https://www.investing.com/rates-bonds/uk-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (UK - Economics)
        "United States": resolve_data_file_path(
        "short_term_bonds", "United States 2-Year Bond Yield Historical Data.csv"),#US2YT=X - https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield-historical-data - Daily (Financials) and Monthly (US - Economics)
    },

        # "Australia": resolve_data_file_path("short_term_bonds", "Australia 2-Year Bond Yield Historical Data.csv"),#AU2YT=RR - https://www.investing.com/rates-bonds/australia-2-year-bond-yield-historical-data - Monthly (Australia - Economics)
        # "China": resolve_data_file_path("short_term_bonds", "China 2-Year Bond Yield Historical Data.csv"),#CN2YT=RR - https://www.investing.com/rates-bonds/china-2-year-bond-yield-historical-data - Monthly (China - Economics)
        # "Brazil": resolve_data_file_path("short_term_bonds", "Brazil 2-Year Bond Yield Historical Data.csv"),#BR2YT=XX - https://www.investing.com/rates-bonds/brazil-2-year-bond-yield-historical-data - Monthly (Brail - Economics)
        # "India": resolve_data_file_path("short_term_bonds", "India 2-Year Bond Yield Historical Data.csv"),#IN2YT=RR - https://www.investing.com/rates-bonds/india-2-year-bond-yield-historical-data - Monthly (India - Economics)
        # "South Korea": resolve_data_file_path("short_term_bonds", "South Korea 2-Year Bond Yield Historical Data.csv"),#KR2YT=RR - https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data - Monthly (South Korea - Economics)
        # "Spain": resolve_data_file_path("short_term_bonds", "Spain 2-Year Bond Yield Historical Data.csv"),#ES2YT=RR -  https://www.investing.com/rates-bonds/spain-2-year-bond-yield-historical-data - Monthly (Spain - Economics)
        # "Switzerland": resolve_data_file_path("short_term_bonds", "Switzerland 2-Year Bond Yield Historical Data.csv"),#CH2YT=RR -  https://www.investing.com/rates-bonds/switzerland-2-year-bond-yield-historical-data - Monthly (Switzerland - Economics)
        # "Israel": resolve_data_file_path("short_term_bonds", "Israel 2-Year Bond Yield Historical Data.csv"),#IL2YT=RR - https://www.investing.com/rates-bonds/israel-2-year-historical-data - Monthly (Israel - Economics)
        # "Hong Kong": resolve_data_file_path("short_term_bonds", "Hong Kong 2-Year Bond Yield Historical Data.csv"),#HK2YT=RR - https://www.investing.com/rates-bonds/hong-kong-2-year-bond-yield-historical-data - Monthly (Hong Kong - Economics)


    "Long-Term Bonds": {
        "Canada": resolve_data_file_path(
        "long_term_bonds", "Canada 10-Year Bond Yield Historical Data.csv"),#CA10YT=RR - https://www.investing.com/rates-bonds/canada-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (Canada - Economics)
        "France": resolve_data_file_path(
        "long_term_bonds", "France 10-Year Bond Yield Historical Data.csv"),#FR10YT=RR - https://www.investing.com/rates-bonds/france-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (France - Economics)
        "Germany": resolve_data_file_path(
        "long_term_bonds", "Germany 10-Year Bond Yield Historical Data.csv"),#DE10YT=RR - https://www.investing.com/rates-bonds/germany-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (Germany - Economics)
        "Italy": resolve_data_file_path(
        "long_term_bonds", "Italy 10-Year Bond Yield Historical Data.csv"),#IT10YT=RR - https://www.investing.com/rates-bonds/italy-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (Italy - Economics)
        "Japan": resolve_data_file_path(
        "long_term_bonds", "Japan 10-Year Bond Yield Historical Data.csv"),#JP10YT=XX - https://www.investing.com/rates-bonds/japan-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (Japan - Economics)
        "United Kingdom": resolve_data_file_path(
        "long_term_bonds", "United Kingdom 10-Year Bond Yield Historical Data.csv"),#GB10YT=RR - https://www.investing.com/rates-bonds/uk-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (UK - Economics)
        "United States": resolve_data_file_path(
        "long_term_bonds", "United States 10-Year Bond Yield Historical Data.csv"),#US10YT=X - https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data - Daily (Financials) and Monthly (US - Economics)
    },

        # "Australia": resolve_data_file_path("long_term_bonds", "Australia 10-Year Bond Yield Historical Data.csv"),#AU10YT=RR - https://www.investing.com/rates-bonds/australia-10-year-bond-yield-historical-data - Monthly (Australia - Economics)
        # "China": resolve_data_file_path("long_term_bonds", "China 10-Year Bond Yield Historical Data.csv"),#CN10YT=RR - https://www.investing.com/rates-bonds/china-10-year-bond-yield-historical-data - Monthly (China - Economics)
        # "Brazil": resolve_data_file_path("long_term_bonds", "Brazil 10-Year Bond Yield Historical Data.csv"),#BR10YT=XX - https://www.investing.com/rates-bonds/brazil-10-year-bond-yield-historical-data - Monthly (Brazil - Economics)
        # "India": resolve_data_file_path("long_term_bonds", "India 10-Year Bond Yield Historical Data.csv"),#IN10YT=RR - https://www.investing.com/rates-bonds/india-10-year-bond-yield-historical-data - Monthly (India - Economics)
        # "South Korea": resolve_data_file_path("long_term_bonds", "South Korea 10-Year Bond Yield Historical Data.csv"),#KR10YT=RR - https://www.investing.com/rates-bonds/south-korea-10-year-bond-yield-historical-data - Monthly (South Korea - Economics)
        # "Spain": resolve_data_file_path("long_term_bonds", "Spain 10-Year Bond Yield Historical Data.csv"),#ES10YT=RR - https://www.investing.com/rates-bonds/spain-10-year-bond-yield-historical-data - Monthly (Spain - Economics)
        # "Switzerland": resolve_data_file_path("long_term_bonds", "Switzerland 10-Year Bond Yield Historical Data.csv"),#CH10YT=RR - https://www.investing.com/rates-bonds/switzerland-10-year-bond-yield-historical-data - Monthly (Switzerland - Economics)
        # "Israel": resolve_data_file_path("long_term_bonds", "Israel 10-Year Bond Yield Historical Data.csv"),#IL10YT=RR - https://www.investing.com/rates-bonds/israel-10-year-bond-yield-historical-data - Monthly (Israel - Economics)
        # "Hong Kong": resolve_data_file_path("long_term_bonds", "Hong Kong 10-Year Bond Yield Historical Data.csv"),#HK10YT=RR - https://www.investing.com/rates-bonds/hong-kong-10-year-bond-yield-historical-data - Monthly (Hong Kong - Economics)
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

# -------------------------------------------------------------------------------------------------
# COTS Reports - Module Positioning & Crowding
# -------------------------------------------------------------------------------------------------

# financial-insight-tools-dev/apps/data_sources/positioning

# Weekly asset map for COTS - cots_assets_default.csv

#AUD positioning - AUD/USD -  https://www.investing.com/currencies/aud-usd-historical-data
#EUR positioning - EUR/USD - https://www.investing.com/currencies/eur-usd-historical-data
#GBP positioning - GBP/USD -  https://www.investing.com/currencies/gbp-usd-historical-data
#JPY positioning - USD/JPY - https://www.investing.com/currencies/usd-jpy-historical-data
#USD Index positioning - DXY - https://www.investing.com/indices/usdollar-historical-data?cid=1224074
#UST 2Y positioning - US2YT=X - https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield-historical-data
#UST 10Y positioning - US10YT=X - https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data
#Russell 2000 positioning - #US2000 - https://www.investing.com/indices/smallcap-2000-historical-data (E-Mini Russell)
#S&P 500 positioning - us500 - https://www.investing.com/indices/us-spx-500-historical-data
#VIX positioning - VIX - https://www.investing.com/indices/volatility-s-p-500-historical-data
#Gold positioning - GC - https://www.investing.com/commodities/gold-historical-data
#Silver positioning - SI - https://www.investing.com/commodities/silver-historical-data

# COTS Reports - Weekly Weekend

# https://www.cftc.gov/MarketReports/CommitmentsofTraders/HistoricalCompressed/index.htm
# Traders in Financial Futures ; Futures Only Reports:.
# Disaggregated Futures Only Reports:

# Traders in Financial Futures ; Futures Only Reports:

# Remove columns and leave:
# Market_and_Exchange_Names
# Report_Date_as_MM_DD_YYYY
# Lev_Money_Positions_Long_All
# Lev_Money_Positions_Short_All
# Change_in_Lev_Money_Long_All
# Change_in_Lev_Money_Short_All
# Pct_of_OI_Lev_Money_Long_All
# Pct_of_OI_Lev_Money_Short_All

# Disaggregated Futures Only Reports:

# Market_and_Exchange_Names
# Report_Date_as_MM_DD_YYYY
# M_Money_Positions_Long_All
# M_Money_Positions_Short_All
# Change_in_M_Money_Long_All
# Change_in_M_Money_Short_All
# Pct_of_OI_M_Money_Long_All
# Pct_of_OI_M_Money_Short_All

# Excel columns - C, O, P, AF, AG, AW, AX
# C -> A, [Remove Row C], C -> M, E -> S, G -> U, I -> AP

# These are then added to each of these files.

# aud_positioning.csv
# eur_positioning.csv
# gbp_positioning.csv
# jpy_positioning.csv
# russell2000_positioning.csv
# sp500_positioning.csv
# usd_index_positioning.csv
# ust_2y_positioning.csv
# ust_10y_positioning.csv
# vix_positioning.csv
# gold_positioning.csv
# siver_positioning.csv

#  To show visuals in human readable format copy into predefined column labels as follows.

# Report_Date_as_MM_DD_YYYY	-> date
# Market_and_Exchange_Names	-> market_name
# Lev_Money_Positions_Long_All	-> leveraged_long
# Lev_Money_Positions_Short_All	-> leveraged_short
# Change_in_Lev_Money_Long_All	-> change_long
# Change_in_Lev_Money_Short_All	-> change_short
# Pct_of_OI_Lev_Money_Long_All	-> open_interest_long_pct
# Pct_of_OI_Lev_Money_Short_All -> open_interest_short_pct

# and change content names to:

# AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE -> Australian Dollar
# EURO FX - CHICAGO MERCANTILE EXCHANGE - Euro Dollar
# BRITISH POUND - CHICAGO MERCANTILE EXCHANGE -> British Pound
# JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE -> Japanese Yen
# USD INDEX - ICE FUTURES U.S. -> USD DXY
# UST 2Y NOTE - CHICAGO BOARD OF TRADE -> US 2Y NOTE
# UST 10Y NOTE - CHICAGO BOARD OF TRADE -> US 10Y NOTE
# RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE -> Russell 2000
# S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE -> S&P 500
# VIX FUTURES - CBOE FUTURES EXCHANGE -> VIX
# GOLD - COMMODITY EXCHANGE INC. -> Gold
# SILVER - COMMODITY EXCHANGE INC. -> Silver


# Equities - Sector Constituents (User) - Market Structure

# "equities_constituents_user", "Accenture Stock Price History.csv"),#acn - https://www.investing.com/equities/accenture-ltd-historical-data
# "equities_constituents_user", "Arm Stock Price History.csv"),#arm - https://www.investing.com/equities/arm-historical-data
# "equities_constituents_user", "Circle Internet Stock Price History.csv"),#crcl - https://www.investing.com/equities/circle-internet-group-inc-historical-data
# "equities_constituents_user", "Coinbase Global Stock Price History.csv"),#coin - https://www.investing.com/equities/coinbase-global-historical-data
# "equities_constituents_user", "Reddit Stock Price History.csv"),#rddt - https://www.investing.com/equities/reddit-historical-data
# "equities_constituents_user", "Rivian Automotive Stock Price History.csv"),#rivn - https://www.investing.com/equities/rivian-automotive-historical-data
# "equities_constituents_user", "SpaceX Stock Price History.csv"),#spcx - https://www.investing.com/equities/spacex-historical-data
