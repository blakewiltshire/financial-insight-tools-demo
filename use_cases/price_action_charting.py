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
- Naked Price Charts with Key Markers
- Multi-Axis Momentum & Trend Confirmations
- Volume Confirmation & Divergence Bars
- Breakout & Mean Reversion Layers
- Risk-Adjusted Return Visuals
- Period-Based Comparative Bars (e.g., Win/Loss, Volatility)

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
    Creates scatter markers for the highest and lowest close prices in a price series.
    Returns two Plotly trace objects for high and low markers.
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
    Calculates a padded Y-axis range based on the min and max close prices.
    Adds a 5% buffer above and below for visual clarity.
    """
    y_min = df["close"].min()
    y_max = df["close"].max()
    buffer = (y_max - y_min) * 0.05
    return [y_min - buffer, y_max + buffer]

# -------------------------------------------------------------------------------------------------
# Function: plot_naked_chart
# Purpose: Generates a basic line chart of closing prices with high/low markers.
# Use Case: Naked Chart (Baseline visualisation in Trade Structuring modules)
# -------------------------------------------------------------------------------------------------
def plot_naked_chart(df):
    """
    Generates a basic line chart of closing prices with high/low markers.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        mode="lines", name="Close Price", line={"color": "blue"}
    ))

    high_marker, low_marker = create_high_low_markers(df)
    fig.add_trace(high_marker)
    fig.add_trace(low_marker)

    fig.update_layout(
        title="Stock Price - Naked Chart (Closing Prices)",
        xaxis={"title": "Date"},
        yaxis={"title": "Price"},
        height=500,
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Function: create_price_action_chart
# Purpose: Plots price action and momentum indicators using dual y-axes.
# Use Case: Trend & Momentum (Trade Timing & Confirmation modules)
# -------------------------------------------------------------------------------------------------
def create_price_action_chart(df, indicators, indicator_params,
title="Price Action & Momentum Overview"):
    """
    Plots price action alongside multiple momentum indicators such as
    rate of change, acceleration, and support/resistance overlays.
    Supports dual y-axes for clarity in trend analysis.
    """
    df = df.copy()
    fig = go.Figure()

    # **Base Close Price Chart (Separate Y-Axis)**
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        mode="lines", name="Close Price", line={"color": "blue", "width": 1},
        yaxis="y1"
    ))

    # **Momentum Indicators (Secondary Axis y2)**
    if "Price Rate of Change" in indicators:
        period = indicator_params.get("Price Rate of Change", 14)
        df["ROC"] = df["close"].pct_change(periods=period) * 100
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["ROC"],
            mode="lines", name="Price Rate of Change", line={"color": "purple", "dash": "dot"},
            yaxis="y2"
        ))

    if "Price Action Momentum" in indicators:
        df["PAM"] = df["close"].diff().rolling(5).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["PAM"],
            mode="lines", name="Price Action Momentum", line={"color": "green", "dash": "dot"},
            yaxis="y2"
        ))

    if "Momentum Strength" in indicators:
        df["MS"] = df["close"].diff().rolling(10).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["MS"],
            mode="lines", name="Momentum Strength", line={"color": "orange", "dash": "dot"},
            yaxis="y2"
        ))

    if "Price Acceleration" in indicators:
        df["PA"] = df["MS"].diff().rolling(5).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["PA"],
            mode="lines", name="Price Acceleration", line={"color": "brown", "dash": "dot"},
            yaxis="y2"
        ))

    # **Trend Confirmation (Higher Highs / Lower Lows) (Scatter Plot)**
    if "Trend Confirmation (Higher Highs / Lower Lows)" in indicators:
        df["TC"] = df["close"].rolling(10).apply(lambda x: x.iloc[-1] > x.iloc[0])
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["TC"],
            mode="markers", name="Trend Confirmation", marker={"color": "red", "size": 5},
            yaxis="y2"
        ))

    if "Support/Resistance Validation" in indicators:
        df["SR"] = df["close"].rolling(10).mean()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["SR"],
            mode="lines", name="Support/Resistance", line={"color": "black", "dash": "dot"}
        ))

    # **Updated Layout for Multi-Axis Support**
    fig.update_layout(
        title=title,
        xaxis={"title": "Date"},
        yaxis={"title": "Close Price", "side": "left", "showgrid": False, "color": "blue",
         "overlaying": "y2", "anchor": "x"},
        yaxis2={"title": "Momentum Indicators", "side": "right", "showgrid": False,
         "color": "black"},
        yaxis3={"title": "Volume", "side": "right", "showgrid": False, "overlaying": "y",
         "anchor": "free", "position": 1.0},
        height=600,
        template="plotly_white"
    )

    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_volume_based_confirmation
# Purpose: Visualises volume surges and contractions relative to baseline trends.
# Use Case: Trend & Momentum (Volume-based confirmation overlays in timing modules)
# -------------------------------------------------------------------------------------------------
def plot_volume_based_confirmation(df, period=14):
    """
    Plots Volume-Based Confirmation, detecting volume surges and divergences.
    Useful for identifying conviction behind price moves.
    """
    df = df.copy()
    df["Volume Change"] = df["volume"].pct_change(periods=period) * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"], y=df["Volume Change"],
        name="Volume-Based Confirmation", marker={"color": "purple"}
    ))

    fig.update_layout(
        title=f"Volume-Based Confirmation (Last {period} Periods)",
        xaxis_title="Date",
        yaxis_title="Volume Change (%)",
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_breakout_mean_reversion_chart
# Purpose: Generates a layered chart showing breakout, mean reversion, and volatility signals.
# Use Case: Breakout & Mean Reversion (Used in setup confirmation and volatility diagnostics)
# -------------------------------------------------------------------------------------------------
# pylint: disable=unused-argument
def plot_breakout_mean_reversion_chart(df, indicators, indicator_params=None):
    """
    Generates a layered chart for breakout, mean reversion, and volatility trends.

    Includes:
    - Bollinger Band Expansion
    - ATR-based Volatility Trends
    - Price Breakout vs Mean Reversion signals

    Args:
        df (pd.DataFrame): Price data with 'close', 'high', 'low', 'date' columns.
        indicators (list): Selected indicators to include in the chart.
        indicator_params (dict, optional): Parameters for indicators (currently unused).

    Returns:
        plotly.graph_objects.Figure: Configured line chart with selected overlays.
    """
    df = df.copy()
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        mode="lines", name="Close Price", line={"color": "blue"}
    ))

    if "Bollinger Band Expansion" in indicators:
        df["BB_Upper"] = df["close"].rolling(20).mean() + (df["close"].rolling(20).std() * 2)
        df["BB_Lower"] = df["close"].rolling(20).mean() - (df["close"].rolling(20).std() * 2)

        fig.add_trace(go.Scatter(
            x=df["date"], y=df["BB_Upper"],
            mode="lines", name="BB Upper", line={"color": "magenta", "dash": "dot"}
        ))
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["BB_Lower"],
            mode="lines", name="BB Lower", line={"color": "magenta", "dash": "dot"}
        ))

    if "ATR Volatility Trends" in indicators:
        df["ATR"] = df["high"].rolling(14).max() - df["low"].rolling(14).min()
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["ATR"],
            mode="lines", name="ATR Volatility", line={"color": "red"}
        ))

    if "Price Breakout vs. Mean Reversion" in indicators:
        df["PBMR"] = df["close"].rolling(10).apply(
            lambda x: x.iloc[-1] - x.iloc[0] if len(x) == 10 else None)
        fig.add_trace(go.Scatter(
            x=df["date"], y=df["PBMR"],
            mode="lines", name="Breakout/Mean Reversion", line={"color": "cyan", "dash": "dot"}
        ))

    fig.update_layout(
        title="Breakout & Mean Reversion Trends",
        xaxis={"title": "Date"},
        yaxis={"title": "Price"},
        height=500,
        template="plotly_white"
    )

    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_volume_price_range_compression
# Purpose: Plots rolling volume as a bar chart for identifying periods of low range and
# high activity.
# Use Case: Breakout & Mean Reversion (Used to assess volume anomalies during compression phases)
# -------------------------------------------------------------------------------------------------
def plot_volume_price_range_compression(df, indicators, period=10):
    """
    Generates a bar chart for volume and price range compression trends.

    Args:
        df (pd.DataFrame): Data containing 'volume' and 'date'.
        indicators (list): List of selected indicators to conditionally display charts.
        period (int, optional): Rolling period for calculating volume average. Defaults to 10.

    Returns:
        plotly.graph_objects.Figure: Bar chart figure.
    """
    df = df.copy()
    fig = go.Figure()

    if "Volume vs. Price Range Compression" in indicators:
        df["VPRC"] = df["volume"].rolling(period).mean()
        fig.add_trace(go.Bar(
            x=df["date"], y=df["VPRC"],
            name="Volume vs Price Compression",
            marker={"color": "darkgreen"}
        ))

    fig.update_layout(
        title="Volume vs. Price Range Compression",
        xaxis={"title": "Date"},
        yaxis={"title": "Volume"},
        height=500,
        template="plotly_white"
    )

    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_winning_vs_losing_periods
# Purpose: Displays the number of winning and losing days over a rolling window.
# Use Case: Performance (Used for outcome framing in portfolio/trade review modules)
# -------------------------------------------------------------------------------------------------
def plot_winning_vs_losing_periods(df, period=14):
    """
    Generates a grouped bar chart comparing the number of winning and losing days
    over a rolling window.

    Args:
        df (pd.DataFrame): Price data containing 'close' and 'date'.
        period (int): Number of periods over which to calculate win/loss counts.

    Returns:
        plotly.graph_objects.Figure: Bar chart of rolling win/loss counts.
    """
    df = df.copy()
    df["Winning Days"] = df["close"].diff().rolling(period).apply(lambda x: (x > 0).sum())
    df["Losing Days"] = df["close"].diff().rolling(period).apply(lambda x: (x < 0).sum())

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["date"], y=df["Winning Days"],
        name="Winning Periods", marker={"color": "green"}
    ))
    fig.add_trace(go.Bar(
        x=df["date"], y=df["Losing Days"],
        name="Losing Periods", marker={"color": "red"}
    ))

    fig.update_layout(
        title=f"Winning vs. Losing (Last {period} Periods)",
        xaxis_title="Date",
        yaxis_title="Count",
        barmode="group",
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_rolling_returns
# Purpose: Plots rolling percentage returns across a specified window.
# Use Case: Performance (Used in post-trade review and performance analytics)
# -------------------------------------------------------------------------------------------------
def plot_rolling_returns(df, period=14):
    """
    Plots percentage-based rolling returns over a defined period.

    Args:
        df (pd.DataFrame): Price data with 'close' and 'date'.
        period (int): Rolling period for returns calculation.

    Returns:
        plotly.graph_objects.Figure: Line chart showing rolling returns.
    """
    df = df.copy()
    df["Rolling Returns"] = df["close"].pct_change(periods=period) * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["Rolling Returns"],
        mode="lines", name="Rolling Returns", line={"color": "blue"}
    ))

    fig.update_layout(
        title=f"Rolling Returns (Last {period} Periods)",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        template="plotly_white"
    )
    return fig

# -------------------------------------------------------------------------------------------------
# Function: plot_volatility_adjusted_returns
# Purpose: Visualises risk-adjusted returns as a heatmap (return/std deviation).
# Use Case: Performance (Supports portfolio and risk benchmarking)
# -------------------------------------------------------------------------------------------------
def plot_volatility_adjusted_returns(df, period=14):
    """
    Plots a heatmap of volatility-adjusted returns calculated as return over standard deviation.

    Args:
        df (pd.DataFrame): Price data with 'close' and 'date'.
        period (int): Rolling window for volatility and return calculations.

    Returns:
        plotly.graph_objects.Figure: Heatmap of risk-adjusted return scores.
    """
    df = df.copy()

    if "Rolling Returns" not in df.columns:
        df["Rolling Returns"] = df["close"].pct_change(periods=period) * 100

    df["Volatility"] = df["close"].rolling(period).std()
    df["Risk-Adjusted Return"] = df["Rolling Returns"] / df["Volatility"].replace(0, float("nan"))

    fig = go.Figure(go.Heatmap(
        x=df["date"],
        y=["Risk-Adjusted Return"],
        z=[df["Risk-Adjusted Return"]],
        colorscale="RdYlGn"
    ))

    fig.update_layout(
        title=f"Volatility-Adjusted Returns (Last {period} Periods)",
        xaxis_title="Date",
        yaxis_title="Risk-Adjusted Return",
        template="plotly_white"
    )
    return fig
