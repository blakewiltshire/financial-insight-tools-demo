# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name


# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
📈 Charting & Visualisation — Modular Plotting Utilities

This module defines reusable charting functions for visualising price action,
momentum, volume dynamics, and volatility-adjusted returns.

Charts are constructed using Plotly and designed to support layered overlays,
multi-axis plotting, and thematically relevant signal display for decision support.

Purpose
- Support core Trade & Portfolio Structuring workflows
- Provide modular, interpretable, and visually aligned financial plots
- Enable direct use in Streamlit or other compatible interfaces

Chart Categories
-
-
-


Integration
All functions are intended to be imported explicitly into Streamlit apps.
These utilities are compatible with structured `pandas` DataFrames containing
OHLCV data and pre-cleaned time series formats.

No interactive UI components are embedded in this module.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import plotly.graph_objects as go


# -------------------------------------------------------------------------------------------------
# Function: create_high_low_markers
# Purpose: Creates scatter markers for the highest and lowest closing prices in a price series.
# Use Case: Naked Chart (Baseline visualisation in Trade Structuring modules)
# -------------------------------------------------------------------------------------------------
def create_high_low_markers(df):
    """
    Creates Plotly marker objects for the highest and lowest closing prices in a time series.

    Parameters:
        df (pd.DataFrame): DataFrame containing at minimum 'date' and 'close' columns.

    Returns:
        Tuple[go.Scatter, go.Scatter]: A tuple containing:
            - High marker (red) at the highest closing price.
            - Low marker (green) at the lowest closing price.

    Notes:
        This function is typically used to visually annotate extreme points on
        interactive price charts.
    """
    max_idx = df['close'].idxmax()
    min_idx = df['close'].idxmin()

    high_marker = go.Scatter(
        x=[df.loc[max_idx, 'date']], y=[df.loc[max_idx, 'close']],
        mode="markers", marker={"color": "red", "size": 10},
        name="High Marker"
    )

    low_marker = go.Scatter(
        x=[df.loc[min_idx, 'date']], y=[df.loc[min_idx, 'close']],
        mode="markers", marker={"color": "green", "size": 10},
        name="Low Marker"
    )

    return high_marker, low_marker

# -------------------------------------------------------------------------------------------------
# Function: get_y_axis_scale
# Purpose: Calculates a buffered Y-axis range for visual clarity.
# Use Case: Shared utility across all line-based visualisations.
# -------------------------------------------------------------------------------------------------
def get_y_axis_scale(df):
    """
    Computes a padded Y-axis range based on the minimum and maximum closing prices.

    Parameters:
        df (pd.DataFrame): DataFrame containing a 'close' column with price data.

    Returns:
        list: A two-element list representing the lower and upper bounds of the Y-axis,
              expanded by 5% padding to improve chart readability.

    Notes:
        This utility supports dynamic chart rendering across instruments with varied price ranges.
    """
    y_min = df["close"].min()
    y_max = df["close"].max()
    buffer = (y_max - y_min) * 0.05  # Add 5% padding for readability
    return [y_min - buffer, y_max + buffer]

# -------------------------------------------------------------------------------------------------
# Function: plot_naked_chart
# Purpose: Generates a basic line chart of closing prices with high/low markers.
# Use Case: Naked Chart (Baseline visualisation in Trade Structuring modules)
# -------------------------------------------------------------------------------------------------
def plot_naked_chart(df):
    """
    Generates a basic line chart of closing prices with high/low markers for visual reference.

    Parameters:
        df (pd.DataFrame): DataFrame containing 'date' and 'close' columns.

    Returns:
        go.Figure: A Plotly figure object displaying:
            - Line plot of closing prices
            - Red marker at the highest close
            - Green marker at the lowest close
            - Clean layout with labelled axes and consistent styling

    Notes:
        This chart is always present as a visual baseline and is useful for
        unfiltered time series interpretation before overlays or indicators are applied.
    """
    fig = go.Figure()

    # **Base Close Price Chart**
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        mode="lines", name="Close Price", line={"color": "blue"}
    ))

    # **Add High/Low Markers**
    high_marker, low_marker = create_high_low_markers(df)
    fig.add_trace(high_marker)
    fig.add_trace(low_marker)

    # **Final Layout Styling**
    fig.update_layout(
        title="Stock Price - Naked Chart (Closing Prices)",
        xaxis={"title": "Date"},
        yaxis={"title": "Price"},
        height=500,
        template="plotly_white"
    )

    return fig

# -------------------------------------------------------------------------------------------------
# Function: create_plotly_chart
# Purpose: Generate a multi-layered Plotly chart overlaying price data with trend, momentum,
#          volatility, and institutional activity indicators for visual decision support.
# Use Case: Trend, Momentum & Volatility Indicators (Trade Timing & Confirmation modules)
# -------------------------------------------------------------------------------------------------
# pylint: disable=too-many-branches, too-many-statements
def create_plotly_chart(df, indicators, indicator_params, title="Stock Price & Indicators"):
    """
    Generates a layered Plotly chart visualising price action alongside selected
    technical indicators.

    Parameters:
        df (pd.DataFrame): DataFrame containing at minimum 'date', 'close', 'high', 'low',
        and 'volume'.
        indicators (list): List of indicator names to include. Supported indicators span:
            - Trend (e.g., ADX, SMA, EMA, Super Trend, Parabolic SAR)
            - Momentum (e.g., RSI, MACD, CMO)
            - Volatility (e.g., Bollinger Bands, ATR)
            - Institutional Activity (e.g., OBV, A/D Line)
        indicator_params (dict): Dictionary mapping indicator names to specific parameters
        (e.g., periods).
        title (str): Optional chart title.

    Returns:
        go.Figure: A Plotly chart object containing:
            - Base price chart
            - Selected overlay indicators
            - High/Low markers
            - Optional secondary Y-axis for institutional volume indicators (OBV, A/D Line)

    Notes:
        - All indicators are overlaid on the same figure for comparative interpretation.
        - Default parameters are applied when specific values are not provided
        via `indicator_params`.
        - Volume-based indicators use a secondary Y-axis to maintain visual clarity.
        - This function is used for dynamic rendering in multi-indicator financial dashboards.
    """
    df = df.copy()  # Ensure we're working with a copy to avoid SettingWithCopyWarning
    fig = go.Figure()

    # **Base Close Price Chart**
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        mode="lines", name="Close Price", line={"color": "blue"}
    ))

    # **Trend Indicators**
    if "Average Directional Index" in indicators:
        period = indicator_params.get("Average Directional Index", 14)
        df["ADX"] = df["close"].rolling(period).mean().copy()  # Ensure it's a copy
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["ADX"],
            mode="lines", name="ADX", line={"color": "red", "dash": "dot"}
        ))

    if "Simple Moving Average" in indicators:
        period = indicator_params.get("Simple Moving Average", 50)
        df["SMA"] = df["close"].rolling(period).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["SMA"],
            mode="lines", name="SMA", line={"color": "green", "dash": "dot"}
        ))

    if "Exponential Moving Average" in indicators:
        period = indicator_params.get("Exponential Moving Average", 50)
        df["EMA"] = df["close"].ewm(span=period, adjust=False).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["EMA"],
            mode="lines", name="EMA", line={"color": "orange", "dash": "dot"}
        ))

    if "Super Trend" in indicators:
        df["Super_Trend"] = df["close"].rolling(10).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["Super_Trend"],
            mode="lines", name="Super Trend", line={"color": "blue", "dash": "dot"}
        ))

    if "Parabolic SAR" in indicators:
        df["Parabolic_SAR"] = df["close"].rolling(14).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["Parabolic_SAR"],
            mode="markers", name="Parabolic SAR", marker={"color": "purple", "size": 5},
        ))

    # **Momentum Indicators**
    if "Relative Strength Index" in indicators:
        period = indicator_params.get("Relative Strength Index", 14)
        df["RSI"] = df["close"].rolling(period).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["RSI"],
            mode="lines", name="RSI", line={"color": "blue"}
        ))

    if "Moving Average Convergence Divergence" in indicators:
        period = indicator_params.get("Moving Average Convergence Divergence", 26)
        df["MACD"] = df["close"].ewm(span=period, adjust=False).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["MACD"],
            mode="lines", name="MACD", line={"color": "purple"}
        ))

    if "Chande Momentum Oscillator" in indicators:
        df["CMO"] = df["close"].rolling(20).mean().copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["CMO"],
            mode="lines", name="CMO", line={"color": "orange"}
        ))

    # **Volatility Indicators**
    if "Bollinger Bands" in indicators:
        period = indicator_params.get("Bollinger Bands", 20)
        df["BB_upper"] = df["close"].rolling(period).mean() + (
        df["close"].rolling(period).std() * 2)
        df["BB_lower"] = df["close"].rolling(period).mean() - (
        df["close"].rolling(period).std() * 2)
        df["BB_upper"] = df["BB_upper"].copy()
        df["BB_lower"] = df["BB_lower"].copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["BB_upper"],
            mode="lines", name="BB Upper", line={"color": "green"}
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["BB_lower"],
            mode="lines", name="BB Lower", line={"color": "green"}
        ))

    if "Average True Range" in indicators:
        period = indicator_params.get("Average True Range", 14)
        df["ATR"] = df["high"].rolling(period).max() - df["low"].rolling(period).min()
        df["ATR"] = df["ATR"].copy()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["ATR"],
            mode="lines", name="ATR", line={"color": "red"}
        ))

    # **Include High/Low Markers**
    high_marker, low_marker = create_high_low_markers(df)
    fig.add_trace(high_marker)
    fig.add_trace(low_marker)

    # **Final Layout Styling**
    fig.update_layout(
        title=title,
        xaxis={"title": "Date"},
        yaxis={"title": "Price"},
        height=500,
        template="plotly_white"
    )

    # **Institutional Activity Indicators (OBV & A/D Line) on Second Y-Axis**
    secondary_y = False  # Used to check if we need a secondary axis

    if "On-Balance Volume" in indicators:
        df['OBV'] = (df['volume'] * ((df['close'] > df['close'].shift()).astype(int) -
                                     (df['close'] < df['close'].shift()).astype(int))).cumsum()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["OBV"],
            mode="lines", name="On-Balance Volume (OBV)", line={"color": "brown"},
            yaxis="y2"
        ))
        secondary_y = True

    if "Accumulation/Distribution Line" in indicators:
        df['AD_Line'] = (df['volume'] * (
        df['close'] - df['low'] - (df['high'] - df['close']))).cumsum()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["AD_Line"],
            mode="lines", name="Accumulation/Distribution Line", line={"color": "darkblue"},
            yaxis="y2"
        ))
        secondary_y = True

    # **Set Up Second Y-Axis for OBV & A/D Line (If Needed)**
    if secondary_y:
        fig.update_layout(
            yaxis2={
                "title": "Volume Indicators",
                "overlaying": "y",
                "side": "right",
                "showgrid": False
            }

        )

    return fig
