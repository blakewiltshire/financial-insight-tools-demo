# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Use Case Indicators — Trade Timing & Confirmation

This module provides grouped indicator logic for use cases related to:
- General Market Overview
- Trend Strength & Direction
- Reversal Identification
- Momentum Reversal Signals
- Institutional Activity & Trend Validity
- Risk & Expected Price Swings
- Reversal & Continuation Patterns

Each section includes:
- Core signal computation functions
- Plaintext signal interpretation logic
- An indicator → function map used by dynamic app rendering

Indicator groups in this module:
- `options_trend_confirmation_map`- Trend Confirmation (Average Directional Index,
Parabolic SAR, Simple Moving Average, Exponential Moving Average, Super Trend)
- `options_momentum_strength_map` - Momentum & Strength (Relative Strength Index,
Moving Average Convergence Divergence, Chande Momentum Oscillator, Money Flow Index )
- `options_volatility_risk_map` - Volatility & Risk (Bollinger Bands, Average True Range,
Standard Deviation)
- `options_volume_confirmation_map` - Volume Confirmation (On-Balance Volume,
Accumulation/Distribution Line)
- `options_pattern_recognition_map` - Pattern Recognition (Candlestick Patterns, Head & Shoulders,
Flags & Pennants, Double Tops/Bottoms)

This file is designed to be imported by main Streamlit app modules, typically:
- `/apps/trade_portfolio_structuring/pages/03_⏳_Trade_Timing_and_Confirmation.py`
- Or any other module referencing these signal categories

File naming convention: `use_case_indicators_<domain>.py`
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd

# -------------------------------------------------------------------------------------------------
# Trend Confirmation Indicators
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Average Directional Index (ADX)
# - Parabolic SAR
# - Simple Moving Average (SMA)
# - Exponential Moving Average (EMA)
# - Super Trend
# -------------------------------------------------------------------------------------------------

# --- Support/Resistance Validation Detection ---
def check_trend_support_resistance(df):
    """Validates trend strength using support/resistance levels."""
    last_close = df["close"].iloc[-1]
    prev_high = df["high"].iloc[-5]
    prev_low = df["low"].iloc[-5]

    if last_close > prev_high:
        return "Trend Confirmation: Breakout"
    if last_close < prev_low:
        return "Trend Warning: Reversal Possible"
    if abs(last_close - prev_low) < 0.5 * (prev_high - prev_low):
        return "Trend Holding: Support Respected"
    if abs(last_close - prev_high) < 0.5 * (prev_high - prev_low):
        return "Trend Holding: Resistance Respected"

    return "No Clear Trend Signal"

# --- ADX (Average Directional Index) ---
def calculate_adx(df, period=14):
    """Computes Average Directional Index (ADX) and directional indicators (+DI, -DI)."""
    df['+DM'] = df['high'].diff()
    df['-DM'] = df['low'].diff()
    df['+DM'] = df['+DM'].where((df['+DM'] > df['-DM']) & (df['+DM'] > 0), 0)
    df['-DM'] = df['-DM'].where((df['-DM'] > df['+DM']) & (df['-DM'] > 0), 0)
    tr = pd.concat([
        (df['high'] - df['low']),
        abs(df['high'] - df['close'].shift()),
        abs(df['low'] - df['close'].shift())
    ], axis=1).max(axis=1)
    df['TR'] = tr.rolling(window=period).sum()
    df['+DI'] = (df['+DM'].rolling(window=period).sum() / df['TR']) * 100
    df['-DI'] = (df['-DM'].rolling(window=period).sum() / df['TR']) * 100
    df['ADX'] = abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']) * 100
    df['ADX'] = df['ADX'].rolling(window=period).mean()
    return df

def determine_adx_signal(df):
    """Interprets ADX value to determine trend strength category."""
    last_adx = df['ADX'].iloc[-1]
    if last_adx > 25:
        return "Strong Trend"
    if last_adx > 20:
        return "Moderate Trend"
    return "Minimal Trend"

def adx(df, adx_period):
    """Wrapper to compute and evaluate ADX trend signal."""
    df = calculate_adx(df, period=adx_period)
    return determine_adx_signal(df)

# --- Parabolic SAR ---
def calculate_parabolic_sar(df, acceleration_factor=0.02, max_af=0.2):
    """Computes the Parabolic SAR indicator with directional logic."""
    df = df.copy()
    df["PSAR"] = float("nan")

    trend = None
    af = acceleration_factor
    ep = None

    for i in range(1, len(df)):
        prev_row = df.iloc[i - 1]
        curr_row = df.iloc[i]

        if trend is None:
            if curr_row["close"] > prev_row["close"]:
                trend = "up"
                ep = curr_row["high"]
                sar = prev_row["low"]
            else:
                trend = "down"
                ep = curr_row["low"]
                sar = prev_row["high"]
        else:
            if trend == "up":
                sar += af * (ep - sar)
                sar = min(sar, prev_row["low"], curr_row["low"])
                if curr_row["low"] < sar:
                    trend = "down"
                    sar = ep
                    ep = curr_row["low"]
                    af = acceleration_factor
                else:
                    if curr_row["high"] > ep:
                        ep = curr_row["high"]
                        af = min(af + acceleration_factor, max_af)
            elif trend == "down":
                sar += af * (ep - sar)
                sar = max(sar, prev_row["high"], curr_row["high"])
                if curr_row["high"] > sar:
                    trend = "up"
                    sar = ep
                    ep = curr_row["high"]
                    af = acceleration_factor
                else:
                    if curr_row["low"] < ep:
                        ep = curr_row["low"]
                        af = min(af + acceleration_factor, max_af)

        df.at[df.index[i], "PSAR"] = sar

    return df

def determine_parabolic_sar_signal(df):
    """Generates signal based on latest Parabolic SAR trend interpretation."""
    if "PSAR" not in df.columns:
        return "No Signal"

    close = df["close"].iloc[-1]
    psar = df["PSAR"].iloc[-1]

    if pd.isna(psar):
        return "No Signal"
    if close > psar:
        return "Bullish Trend Continuation"
    if close < psar:
        return "Bearish Trend Continuation"
    return "Neutral"

def parabolic_sar(df, acceleration_factor=0.02, max_af=0.2):
    """Wrapper for Parabolic SAR signal with parameter override support."""
    df = calculate_parabolic_sar(df, acceleration_factor, max_af)
    return determine_parabolic_sar_signal(df)

# --- Simple Moving Average (SMA) ---
def calculate_sma(df, short_period=50, long_period=200):
    """Computes SMA crossovers."""
    df['SMA Short'] = df['close'].rolling(window=short_period).mean()
    df['SMA Long'] = df['close'].rolling(window=long_period).mean()
    return df

def determine_sma_signal(df):
    """Determines SMA crossover signal based on insights mapping."""
    if df['SMA Short'].iloc[-1] > df['SMA Long'].iloc[-1]:
        return "Confirmed Trend"  # ✅ Matches insight_generator.py
    if df['SMA Short'].iloc[-1] < df['SMA Long'].iloc[-1]:
        return "Confirmed Trend"  # ✅ Still a trend, just downward
    return "Indecisive"  # ✅ Aligns with insight mapping

def sma(df, short_period=50, long_period=200):
    """Computes SMA crossover and returns a signal."""
    df = calculate_sma(df, short_period, long_period)
    return determine_sma_signal(df)

# ---  Exponential Moving Average (EMA) ---
def calculate_ema(df, short_period=12, long_period=26):
    """Computes EMA crossovers."""
    df['EMA Short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['EMA Long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    return df

def determine_ema_signal(df):
    """Determines EMA crossover signal based on insights mapping."""
    if df['EMA Short'].iloc[-1] > df['EMA Long'].iloc[-1]:
        return "Confirmed Trend"
    if df['EMA Short'].iloc[-1] < df['EMA Long'].iloc[-1]:
        return "Confirmed Trend"
    return "Indecisive"

def ema(df, short_period=12, long_period=26):
    """Computes EMA crossover and returns a signal."""
    df = calculate_ema(df, short_period, long_period)
    return determine_ema_signal(df)

# ---  Super Trend Indicator ---
def calculate_super_trend(df, atr_period=10, multiplier=3):
    """Computes Super Trend indicator."""
    df['ATR'] = df['high'].rolling(window=atr_period).std()  # Approximate ATR calculation
    df['Upper Band'] = df['high'] - (multiplier * df['ATR'])
    df['Lower Band'] = df['low'] + (multiplier * df['ATR'])
    df["Super Trend"] = df.apply(
        lambda row: row["Upper Band"]
        if row["close"] < row["Upper Band"]
        else row["Lower Band"],
        axis=1
    )

    return df

def determine_super_trend_signal(df):
    """Determines Super Trend signal."""
    if df['close'].iloc[-1] > df['Super Trend'].iloc[-1]:
        return "Trend Confirmed"
    if df['close'].iloc[-1] < df['Super Trend'].iloc[-1]:
        return "Trend Confirmed"
    return "Indecisive"

def super_trend(df, atr_period=10, multiplier=3):
    """Computes Super Trend and returns a signal."""
    df = calculate_super_trend(df, atr_period, multiplier)
    return determine_super_trend_signal(df)


# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_trend_confirmation_map = {
    "Average Directional Index": adx,
    "Parabolic SAR": parabolic_sar,
    "Simple Moving Average": sma,
    "Exponential Moving Average": ema,
    "Super Trend": super_trend
}


# -------------------------------------------------------------------------------------------------
# Momentum & Strength
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - RSI (Relative Strength Index)
# - MACD (Moving Average Convergence Divergence)
# - Chande Momentum Oscillator (CMO)
# - Money Flow Index (MFI)
# -------------------------------------------------------------------------------------------------

# --- Relative Strength Index (RSI) ---
def calculate_rsi(df, period=14):
    """Computes Relative Strength Index (RSI) for given period."""
    delta = df["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def determine_rsi_signal(df):
    """Classifies RSI value to indicate overbought or oversold pressure."""
    last_rsi = df["RSI"].iloc[-1]
    if last_rsi > 80:
        return "Overbought"
    if last_rsi > 70:
        return "Overextended Overbought"
    if last_rsi < 20:
        return "Oversold"
    if last_rsi < 30:
        return "Deeply Oversold"
    return "Neutral"

def rsi(df, rsi_period=14):
    """Wrapper to compute RSI and return interpretation signal."""
    df = calculate_rsi(df, period=rsi_period)
    return determine_rsi_signal(df)

# --- Moving Average Convergence Divergence (MACD) ---
def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    """Computes MACD Line and Signal Line."""
    df["MACD_Line"] = (
        df["close"].ewm(span=short_period, adjust=False).mean()
        - df["close"].ewm(span=long_period, adjust=False).mean()
    )
    df["Signal_Line"] = df["MACD_Line"].ewm(span=signal_period, adjust=False).mean()
    return df

def determine_macd_signal(df):
    """Determines MACD signal based on crossover and momentum strength."""
    last_macd = df["MACD_Line"].iloc[-1]
    last_signal = df["Signal_Line"].iloc[-1]
    macd_near_zero = abs(last_macd) < 0.1

    if last_macd > last_signal and not macd_near_zero:
        return "Bullish Crossover"
    if last_macd < last_signal and not macd_near_zero:
        return "Bearish Crossover"
    return "Weak Signal"

def macd(df, period=None):  # pylint: disable=unused-argument
    """Wrapper to compute MACD crossover signal."""
    df = calculate_macd(df)
    return determine_macd_signal(df)

# --- Chande Momentum Oscillator (CMO) ---
def calculate_cmo(df, period=20):
    """Computes Chande Momentum Oscillator (CMO)."""
    delta = df["close"].diff()
    up_sum = delta.where(delta > 0, 0).rolling(window=period).sum()
    down_sum = -delta.where(delta < 0, 0).rolling(window=period).sum()
    df["CMO"] = 100 * ((up_sum - down_sum) / (up_sum + down_sum))
    return df

def determine_cmo_signal(df):
    """Determines CMO signal based on insights mapping."""
    last_cmo = df["CMO"].iloc[-1]
    if last_cmo > 50:
        return "Strong Momentum"
    if last_cmo < -50:
        return "Strong Momentum"
    return "Neutral"

def cmo(df, period=20):
    """Wrapper to compute CMO and return directional signal."""
    df = calculate_cmo(df, period=period)
    return determine_cmo_signal(df)

# ---  Money Flow Index (MFI) ---
def calculate_mfi(df, period=14):
    """Computes Money Flow Index (MFI) based on price and volume."""
    df["Typical_Price"] = (df["high"] + df["low"] + df["close"]) / 3
    df["Raw_Money_Flow"] = df["Typical_Price"] * df["volume"]
    df["Positive_Money_Flow"] = df["Raw_Money_Flow"].where(df["Typical_Price"].diff() > 0, 0)
    df["Negative_Money_Flow"] = df["Raw_Money_Flow"].where(df["Typical_Price"].diff() < 0, 0)
    money_flow_ratio = df["Positive_Money_Flow"].rolling(
        window=period).sum() / df["Negative_Money_Flow"].rolling(window=period).sum()
    df["MFI"] = 100 - (100 / (1 + money_flow_ratio))
    return df

def determine_mfi_signal(df):
    """Determines MFI signal based on insights mapping."""
    last_mfi = df["MFI"].iloc[-1]
    if last_mfi > 80 or last_mfi < 20:
        return "Strong Buying/Selling Pressure"
    return "Neutral"

def mfi(df, period=14):
    """Wrapper to compute MFI and return signal based on money flow pressure."""
    df = calculate_mfi(df, period=period)
    return determine_mfi_signal(df)

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_momentum_strength_map = {
    "Relative Strength Index": rsi,
    "Moving Average Convergence Divergence": macd,
    "Chande Momentum Oscillator": cmo,
    "Money Flow Index": mfi
}

# -------------------------------------------------------------------------------------------------
# Volatility & Risk
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Bollinger Bands (BB)
# - ATR (Average True Range)
# - Standard Deviation (SD)
# -------------------------------------------------------------------------------------------------

# ---  Bollinger Bands (BB) ---
def calculate_bollinger_bands(df, period=20, std_dev=2):
    """Computes Bollinger Bands (upper, middle, lower) using rolling mean and standard deviation."""
    df['BB Middle'] = df['close'].rolling(window=period).mean()
    df['BB Upper'] = df['BB Middle'] + (df['close'].rolling(window=period).std() * std_dev)
    df['BB Lower'] = df['BB Middle'] - (df['close'].rolling(window=period).std() * std_dev)
    return df

def determine_bollinger_signal(df):
    """Interprets Bollinger Band positioning to identify breakout, squeeze, or mean reversion."""
    last_close = df['close'].iloc[-1]
    last_upper = df['BB Upper'].iloc[-1]
    last_lower = df['BB Lower'].iloc[-1]
    if last_close > last_upper:
        return "Breakout"
    if last_close < last_lower:
        return "Breakout"
    if last_upper - last_lower < df['BB Middle'].rolling(20).std().iloc[-1]:
        return "Squeeze"
    return "Mean Reversion"

def bollinger_bands(df, period=20, std_dev=2):
    """Wrapper to compute Bollinger Bands and derive signal type."""
    df = calculate_bollinger_bands(df, period, std_dev)
    return determine_bollinger_signal(df)

# ---  ATR (Average True Range) ---
def calculate_atr(df, period=14):
    """Computes Average True Range (ATR) to measure market volatility."""
    df['TR'] = pd.concat([
        df['high'] - df['low'],
        abs(df['high'] - df['close'].shift()),
        abs(df['low'] - df['close'].shift())
    ], axis=1).max(axis=1)
    df['ATR'] = df['TR'].rolling(window=period).mean()
    return df

def determine_atr_signal(df):
    """Evaluates ATR level to classify volatility regime."""
    last_atr = df["ATR"].iloc[-1]
    if last_atr > 15:
        return "High Volatility"
    return "Low Volatility"

def atr(df, atr_period=14):
    """Wrapper to compute ATR and return volatility signal."""
    df = calculate_atr(df, period=atr_period)
    return determine_atr_signal(df)

# --- Standard Deviation (SD) ---
def calculate_standard_deviation(df, period=20):
    """Calculates rolling standard deviation of close prices."""
    df['SD'] = df['close'].rolling(window=period).std()
    return df

def determine_sd_signal(df):
    """Classifies volatility state based on standard deviation against its mean."""
    last_sd = df['SD'].iloc[-1]
    if last_sd > df['SD'].mean():
        return "High Volatility"
    return "Low Volatility"

def standard_deviation(df, period=20):
    """Wrapper to compute standard deviation and determine volatility condition."""
    df = calculate_standard_deviation(df, period=period)
    return determine_sd_signal(df)


# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_volatility_risk_map = {
    "Bollinger Bands": bollinger_bands,
    "Average True Range": atr,
    "Standard Deviation": standard_deviation
}

# -------------------------------------------------------------------------------------------------
# Volume Confirmation
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - On-Balance Volume (OBV)
# - Accumulation/Distribution (A/D) Line
# -------------------------------------------------------------------------------------------------

# ---  On-Balance Volume (OBV) ---
def calculate_obv(df):
    """Computes On-Balance Volume (OBV) using cumulative directional volume shifts."""
    df['OBV'] = (df['volume'] * ((df['close'] > df['close'].shift()).astype(int) -
                                 (df['close'] < df['close'].shift()).astype(int))).cumsum()
    return df

def determine_obv_signal(df):
    """Generates OBV signal by comparing latest volume trend shift."""
    last_obv = df['OBV'].iloc[-1]
    prev_obv = df['OBV'].iloc[-2]
    if last_obv > prev_obv:
        return "Volume Confirming Trend"
    if last_obv < prev_obv:
        return "Divergence"
    return "Neutral"

def obv(df, period=None):  # pylint: disable=unused-argument
    """Wrapper to compute OBV and return directional volume confirmation signal."""
    df = calculate_obv(df)
    return determine_obv_signal(df)

# ---  Accumulation/Distribution (A/D) Line ---
def calculate_ad_line(df):
    """Computes Accumulation/Distribution (A/D) Line."""
    df['Money Flow Multiplier'] = (
        ((df['close'] - df['low']) - (df['high'] - df['close']))
        / (df['high'] - df['low'])
    )
    df['Money Flow Volume'] = df['Money Flow Multiplier'] * df['volume']
    df['A/D Line'] = df['Money Flow Volume'].cumsum()
    return df

def determine_ad_line_signal(df):
    """Generates signal from A/D Line movement."""
    last_ad = df['A/D Line'].iloc[-1]
    prev_ad = df['A/D Line'].iloc[-2]
    if last_ad > prev_ad:
        return "Accumulation—Buying Pressure"
    if last_ad < prev_ad:
        return "Distribution—Selling Pressure"
    return "Neutral"

def ad_line(df, period=None):  # pylint: disable=unused-argument
    """Signal wrapper for Accumulation/Distribution Line."""
    df = calculate_ad_line(df)
    return determine_ad_line_signal(df)

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_volume_confirmation_map = {
    "On-Balance Volume": obv,
    "Accumulation/Distribution Line": ad_line
}

# -------------------------------------------------------------------------------------------------
# Pattern Recognition Indicators
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Candlestick Patterns
# - Head & Shoulders
# - Flags & Pennants
# - Double Tops/Bottoms
# -------------------------------------------------------------------------------------------------

# --- Support/Resistance Validation Detection ---
def validate_support_resistance(df):
    """Detects support/resistance levels and confirms breakouts or reversals."""
    last_close = df["close"].iloc[-1]
    prev_high = df["high"].iloc[-5]
    prev_low = df["low"].iloc[-5]

    if last_close > prev_high:
        return "Breakout Confirmed"
    if last_close < prev_low:
        return "Failed Breakout"
    if abs(last_close - prev_low) < 0.5 * (prev_high - prev_low):
        return "Support Holding"
    if abs(last_close - prev_high) < 0.5 * (prev_high - prev_low):
        return "Resistance Holding"

    return "No Significant Level"

# ---  Candlestick Patterns Detection ---
def detect_candlestick_patterns(df, period=None): # pylint: disable=unused-argument
    """Identifies bullish and bearish candlestick patterns."""
    last_close = df["close"].iloc[-1]
    last_open = df["open"].iloc[-1]

    if last_close > last_open:
        return "Bullish Engulfing"
    if last_close < last_open:
        return "Bearish Engulfing"
    return "Doji"

# ---  Head & Shoulders Pattern Detection ---
def detect_head_and_shoulders(df, period=None): # pylint: disable=unused-argument
    """Detects head and shoulders pattern (trend reversal)."""
    last_close = df["close"].iloc[-1]
    prev_close = df["close"].iloc[-5]

    if last_close < prev_close:
        return "Bearish"
    return "Invalidation"

# ---  Flags & Pennants Pattern Detection ---
def detect_flags_and_pennants(df, period=None): # pylint: disable=unused-argument
    """Detects trend continuation flags and pennants."""
    last_high = df["high"].iloc[-1]
    prev_high = df["high"].iloc[-5]

    if last_high > prev_high:
        return "Bullish"
    return "Bearish"

# ---  Double Tops & Bottoms Pattern Detection ---
def detect_double_tops_bottoms(df, period=None): # pylint: disable=unused-argument
    """Identifies key reversal levels (Double Tops/Bottoms)."""
    last_close = df["close"].iloc[-1]
    prev_high = df["high"].iloc[-5]

    if last_close < prev_high:
        return "Confirmed Reversal"
    return "False Breakout"

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_pattern_recognition_map = {
    "Candlestick Patterns": detect_candlestick_patterns,
    "Head & Shoulders": detect_head_and_shoulders,
    "Flags & Pennants": detect_flags_and_pennants,
    "Double Tops/Bottoms": detect_double_tops_bottoms
}
