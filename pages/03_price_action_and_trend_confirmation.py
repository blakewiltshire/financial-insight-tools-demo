# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=import-error, unused-variable
# pylint: disable=invalid-name
# pylint: disable=non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Price Action & Trend Confirmation App

Streamlit app for analysing price action using predefined use cases, visual indicators, and
contextual insights. Designed to be modular, AI-augmented, and fully interoperable with the
Financial Insight Tools DSS.

Functions:
- Loads and renders use case-specific indicators and charts
- Integrates shared helpers and insight generators
- Structures content for decision-support workflows
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st
import scipy.signal

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders, sidebar links etc.
# -------------------------------------------------------------------------------------------------
from core.helpers_1 import (  # pylint: disable=import-error
    load_markdown_file,
    build_sidebar_links,
    get_named_paths,
)

from helpers.aggrid_style import AGGRID_NUNITO_CSS


# -------------------------------------------------------------------------------------------------
# Resolve Key Paths for This Module
#
# Use `get_named_paths(__file__)` to assign contextual levels.
# These "level_up_N" values refer to how many directories above the current file
# -------------------------------------------------------------------------------------------------
PATHS = get_named_paths(__file__)
ROOT_PATH = PATHS["level_up_1"]
# APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_price_action_and_trend_confirmation.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")

# -------------------------------------------------------------------------------------------------
# Clean and format Single Asset Files
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_default import (
    load_data_from_file, load_asset_data, clean_data, resample_data
)
from data_sources.financial_data.shared_utils import convert_date_to_us_format

# -------------------------------------------------------------------------------------------------
# Mapping Logic
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.preloaded_assets import get_preloaded_assets
from data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from data_sources.financial_data.asset_map import get_asset_path
from data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# Use Cases
# -------------------------------------------------------------------------------------------------
from helpers.use_case_helpers_price_action import (
    generate_use_case_help_text,
    apply_use_case_mapping,
    resolve_canonical_use_case
)

from use_cases.price_action_definitions import USE_CASES

# --- Indicator Config ---
from use_cases.price_action_indicators import (
    options_performance_map, options_trend_momentum_map, options_breakout_mean_reversion_map
)

# --- Insights ---
from use_cases.price_action_insights import generate_insights

# --- Charting & Visualisation  ---
from use_cases.price_action_charting import (
    plot_naked_chart, create_price_action_chart, plot_volume_based_confirmation,
    plot_breakout_mean_reversion_chart, plot_volume_price_range_compression,
    plot_winning_vs_losing_periods, plot_rolling_returns, plot_volatility_adjusted_returns
)

# -------------------------------------------------------------------------------------------------
# Filtering Options (Ranges, Events and Temporal)
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.filtering_options import filtering_options_map

# -------------------------------------------------------------------------------------------------
# Reminder: __init__.py
# Ensure all relevant folders (e.g., /helpers, /use_cases, /data_sources etc)
# contain an empty __init__.py file.
# This marks them as Python packages and allows import resolution (especially important when
# running via Streamlit or exporting to other Python environments).
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Managing Dynamic Charts with `key=`
# When rendering multiple charts using similar function calls, always pass a unique `key` to
# `st.plotly_chart(...)` to avoid duplication errors. This is particularly important in filtered,
# multi-view, or conditionally toggled layouts.
# -------------------------------------------------------------------------------------------------
keys = {
    "roc": "roc_chart_20250518060619",
    "pam": "pam_chart_20250518060619",
    "ms": "ms_chart_20250518060619",
    "pa": "pa_chart_20250518060619",
    "tc": "tc_chart_20250518060619",
    "sr": "sr_chart_20250518060619",
    "vbc": "vbc_chart_20250518060619",
    "bmr": "bmr_chart_20250518060619",
    "vprc": "vprc_chart_20250518060619",
    "win_loss": "win_loss_chart_20250518060619",
    "rolling_returns": "rolling_returns_chart_20250518060619",
    "var": "var_chart_20250518060619",
    "price_momentum": "price_momentum_chart_20250518060619",
}

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Price Action & Trend Confirmation", layout="wide")
st.title("📊 Price Action & Trend Confirmation")
st.caption("*Analyse candlestick patterns, breakout zones, and directional flow.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------

with st.expander("📌 What is this app about?"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_price_action_and_trend_confirmation.md")

# -------------------------------------------------------------------------------------------------
# Start Sidebar Operations
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Navigation Sidebar
# Allows navigation across numbered subpages in /pages/
# Uses `build_sidebar_links()` to list only structured pages (e.g., 100_....py)
# Also links back to app dashboard (e.g., app.py)
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📂 Navigation Menu")
st.sidebar.page_link('app.py', label='Financial Insight Tools Demo')
for path, label in build_sidebar_links():
    st.sidebar.page_link(path, label=label)

st.sidebar.divider()

# -------------------------------------------------------------------------------------------------
# Branding
# -------------------------------------------------------------------------------------------------
st.logo(BRAND_LOGO_PATH) # pylint: disable=no-member

# -------------------------------------------------------------------------------------------------
# Asset Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.title('🔎 Select Asset for Price Action')

# --- Uploaded Asset Defaults ---
UPLOADED_FILE = None
DATA_TITLE = ''  # Default title is empty, no predefined title
ASSET_TYPE = ""  # Default asset type is empty, needs to be selected

# --- Data source method ---
data_source = st.sidebar.selectbox(
    'Choose your data source',
    # ['Preloaded Asset Types (Default)', 'Preloaded Asset Types (User)', 'Upload my own files']
    ['Preloaded Asset Types (Default)']
)

# --- Preloaded Assets ---
preloaded_assets_default = get_preloaded_assets()
# preloaded_assets_user = get_user_preloaded_assets()

asset_path = None
uploaded_file = None

# --- Default Preloaded Assets ---
if data_source == 'Preloaded Asset Types (Default)':
    asset_category = st.sidebar.selectbox("Select Asset Category", list(preloaded_assets_default.keys()))
    asset_sample = st.sidebar.selectbox("Select Base Asset", preloaded_assets_default[asset_category])
    if asset_sample:
        DATA_TITLE = asset_sample
        ASSET_TYPE = asset_category
        asset_path = get_asset_path(asset_category, asset_sample)

# --- Predisposition (trade direction) ---
predisposition = st.sidebar.radio("Trade Bias", ["Bullish", "Bearish"])

try:
    if data_source == 'Upload my own files':
        if uploaded_file is not None:
            processed_df = load_data_from_file(uploaded_file)
        else:
            st.info("Please upload a CSV file.")
            st.stop()  # Ensures we halt until a valid file is uploaded

    elif data_source.startswith('Preloaded') and asset_path:
        processed_df = load_data_from_file(asset_path)

    else:
        processed_df = load_data_from_file(DEFAULT_FILE)
        DATA_TITLE = DEFAULT_TITLE
        ASSET_TYPE = DEFAULT_ASSET_TYPE

    processed_df, dataset_info = clean_data(processed_df)

except KeyError as e:
    st.error(f"Missing key column: {e}")

# -------------------------------------------------------------------------------------------------
# Filter Selection
# Applies to 📈 Full Data (Filtered) Chart, Confirmation and Readiness Summary
# Temporal & Event-Based Filters are not available
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📅 Select Date Range")

st.sidebar.caption(
    "⚠️ Only date range filtering is applied here. For seasonal or event-based exploration, "
    "use the 🔎 Market & Volatility Scanner."
)

filter_type = "Range" # (Remove Temporal & Event-Based Filters)
filtered_df = processed_df  # Default to full dataset
if processed_df is not None:
    filtered_df = filtering_options_map[filter_type](processed_df)  # Apply only Range Filtering

# -------------------------------------------------------------------------------------------------
# Indicator Categories.
# -------------------------------------------------------------------------------------------------
indicator_categories = {
    "Performance": options_performance_map,
    "Trend & Momentum": options_trend_momentum_map,
    "Breakout & Mean Reversion": options_breakout_mean_reversion_map,
}

selected_indicators = {}
indicator_params = {}

# **Predefine Default Periods for All Indicators**
default_periods = {
    "Winning vs. Losing": 14,
    "Rolling Returns": 14,
    "Volatility-Adjusted Returns": 14,
    "Momentum Score": 14,
    "Net Price Movement": 14,
    "Price Rate of Change": 14,
    "Price Action Momentum": 14,
    "Trend Confirmation (Higher Highs / Lower Lows)": 14,
    "Momentum Strength": 14,
    "Price Acceleration": 5,
    "Volume-Based Confirmation": 14,
    "Support/Resistance Validation": 5,
    "Bollinger Band Expansion": 20,
    "Price Breakout vs. Mean Reversion": 20,
    "ATR Volatility Trends": 14,
    "Standard Deviation of Price Swings": 20,
    "Volume vs. Price Range Compression": 20,
}

# -------------------------------------------------------------------------------------------------
# Sidebar Use Case Selection
# -------------------------------------------------------------------------------------------------
st.sidebar.title("📌 Select a Use Case")

selected_use_case = st.sidebar.selectbox(
    "Select a predefined Use Case",
    ["Naked Charts"] + list(USE_CASES.keys()),
    index=0,
    help=generate_use_case_help_text(USE_CASES, default_label="Naked Charts")
)

auto_selected_indicators = apply_use_case_mapping(
    selected_use_case,
    USE_CASES,
    indicator_categories,
    default_label="Naked Charts"
)

# ✅ Resolve for internal registry key (fixes JSON export linkage)
use_case_name = resolve_canonical_use_case(selected_use_case, USE_CASES)

# -------------------------------------------------------------------------------------------------
# **Indicator Timeframe Suitability for Price Action**
# -------------------------------------------------------------------------------------------------
indicator_timeframes = {
    "Winning vs. Losing": ["Daily", "Weekly", "Monthly"],
    "Rolling Returns": ["Daily", "Weekly", "Monthly"],
    "Volatility-Adjusted Returns": ["Daily", "Weekly", "Monthly"],
    "Net Price Movement": ["Daily", "Weekly", "Monthly"],
    "Momentum Score": ["Daily", "Weekly", "Monthly"],
    "Price Rate of Change": ["Daily", "Weekly", "Monthly"],
    "Price Action Momentum": ["Daily", "Weekly", "Monthly"],
    "Trend Confirmation (Higher Highs / Lower Lows)": ["Daily", "Weekly", "Monthly"],
    "Momentum Strength": ["Daily", "Weekly"],
    "Price Acceleration": ["Daily", "Weekly"],
    "Volume-Based Confirmation": ["Daily", "Weekly", "Monthly"],
    "Support/Resistance Validation": ["Daily", "Weekly"],
    "Bollinger Band Expansion": ["Daily", "Weekly"],
    "Price Breakout vs. Mean Reversion": ["Daily", "Weekly"],
    "ATR Volatility Trends": ["Daily", "Weekly", "Monthly"],
    "Standard Deviation of Price Swings": ["Daily", "Weekly", "Monthly"],
    "Volume vs. Price Range Compression": ["Daily", "Weekly", "Monthly"],
}

# **Updated Timeframes**
timeframes = ["Daily", "Weekly", "Monthly"]

# Sidebar: Price Action Selection
st.sidebar.title("📊 Customise Price Action Parameters")

selected_indicators = {}
indicator_params = {}

for category, indicators in indicator_categories.items():
    with st.sidebar.expander(f"📌 {category}"):

        # Auto-select indicators if a Use Case is chosen
        default_selection = auto_selected_indicators.get(category, [])

        # Ensure default selections exist in available indicators to avoid KeyError
        default_selection = [ind for ind in default_selection if ind in indicators]

        # Allow users to modify selection manually after Use Case auto-selection
        selected = st.multiselect(
            f"Select indicators for {category}",
            options=list(indicators.keys()),
            default=default_selection
        )

        # Store final selected indicators per category
        selected_indicators[category] = list(set(selected))

        # Add sliders for indicators requiring a period
        for indicator in selected:
            if indicator in default_periods and default_periods[indicator] is not None:
                indicator_params[indicator] = st.sidebar.slider(
                    f"{indicator} Period",
                    min_value=1, max_value=50,  # 🔹 Consistent parameter tuning
                    value=default_periods[indicator],
                    step=1
                )

# **Insight Mapping for App3**
insight_name_map = {
    "Winning vs. Losing": "Winning vs. Losing",
    "Rolling Returns": "Rolling Returns",
    "Volatility-Adjusted Returns": "Volatility-Adjusted Returns",
    "Net Price Movement": "Net Price Movement",
    "Momentum Score": "Momentum Score",
    "Price Rate of Change": "Price Rate of Change",
    "Price Action Momentum": "Price Action Momentum",
    "Trend Confirmation (Higher Highs / Lower Lows)": "Trend Confirmation (Higher Highs / Lower Lows)",
    "Momentum Strength": "Momentum Strength",
    "Price Acceleration": "Price Acceleration",
    "Volume-Based Confirmation": "Volume-Based Confirmation",
    "Support/Resistance Validation": "Support/Resistance Validation",
    "Bollinger Band Expansion": "Bollinger Band Expansion",
    "Price Breakout vs. Mean Reversion": "Price Breakout vs. Mean Reversion",
    "ATR Volatility Trends": "ATR Volatility Trends",
    "Standard Deviation of Price Swings": "Standard Deviation of Price Swings",
    "Volume vs. Price Range Compression": "Volume vs. Price Range Compression",
}


# Indicators that provide **absolute confirmation** (No Bullish/Bearish Bias)
trend_strength_indicators = [
    "Momentum Strength", "ATR Volatility Trends", "Standard Deviation of Price Swings",
    "Volume vs. Price Range Compression"
]

predisposition_map = {
    "Bullish": [
        "Strong Uptrend", "Accelerating Uptrend", "Higher Highs & Higher Lows",
        "Rapid Upside Move", "High Volume Breakout", "Expanding Bands",
        "Breakout Above Resistance", "Support Holding",
        "Confirmed Bullish Trend", "Breakout Confirmed",
        "Strong Bullish Momentum", "Positive Net Price Movement",
        "Rolling Returns Uptrend", "Volatility-Adjusted Uptrend"
    ],
    "Bearish": [
        "Strong Downtrend", "Accelerating Downtrend", "Lower Highs & Lower Lows",
        "Rapid Downside Move", "Failed Breakout", "Breakout Below Support",
        "Resistance Holding", "Contracting Bands",
        "Confirmed Bearish Trend",
        "Strong Bearish Momentum", "Negative Net Price Movement",
        "Rolling Returns Downtrend", "Volatility-Adjusted Downtrend"
    ],
    # **Trend Strength Only Indicators**
    "Trend Strength": [
    "Strong Momentum", "Increasing ATR", "High Volatility", "Increasing Volume & Range"
]
}


# Indicator Weighting System (Adjusted for Stability)
indicator_weights = {
    # **Performance Indicators (Weight = 3)**
    "Winning vs. Losing": 3,
    "Rolling Returns": 3,
    "Volatility-Adjusted Returns": 3,
    "Momentum Score": 3,
    "Net Price Movement": 3,

    # **Trend Confirmation (Weight = 3)**
    "Price Rate of Change": 3,
    "Price Action Momentum": 3,
    "Trend Confirmation (Higher Highs / Lower Lows)": 3,

    # **Momentum Confirmation (Weight = 2)**
    "Momentum Strength": 2,
    "Price Acceleration": 2,
    "Volume-Based Confirmation": 2,

    # **Reversal Indicators (Weight = 3)**
    "Support/Resistance Validation": 3,

    # **Breakout & Mean Reversion (Weight = 2)**
    "Bollinger Band Expansion": 2,
    "Price Breakout vs. Mean Reversion": 2,
    "ATR Volatility Trends": 2,

    # **Volatility Indicators (Weight = 2)**
    "Standard Deviation of Price Swings": 2,
    "Volume vs. Price Range Compression": 2
}

# **Execution Readiness Computation **
def compute_execution_readiness(df, predisposition, selected_indicators):
    summary = []
    timeframe_summary = {}

    for timeframe in timeframes:  # Apply to Daily, Weekly, Monthly
        df_resampled = resample_data(df.copy(), timeframe)
        if df_resampled is None or df_resampled.empty:
            timeframe_summary[timeframe] = "⚠️ Insufficient Data"
            continue

        total_score = 0
        max_possible_score = 0
        confirming_indicators = 0

        for category, indicators in indicator_categories.items():
            for indicator in selected_indicators.get(category, []):
                if timeframe not in indicator_timeframes.get(indicator, []):
                    continue

                func = indicators[indicator]
                period = indicator_params.get(indicator, 14)
                signal = func(df_resampled, period) if period else func(df_resampled)

                # Apply Trend Strength Logic (No Bullish/Bearish)
                if indicator in trend_strength_indicators:
                    predisposition_display = "N/A"
                    if signal in predisposition_map["Trend Strength"]:
                        confirmation = "✅ Trend strength detected."
                    else:
                        confirmation = "⚠️ No strong trend detected."

                # Apply Predisposition Logic
                else:
                    predisposition_display = predisposition
                    if signal in predisposition_map[predisposition]:
                        confirmation = f"✅ {signal} aligns with selected market conditions."
                    else:
                        confirmation = f"⚠️ {signal} differs from selected market conditions."

                # Store in summary for Key Technical Confirmation & Red Flags
                insight = generate_insights(insight_name_map.get(
                indicator, indicator), signal, timeframe, predisposition)
                summary.append([timeframe, indicator, signal,
                predisposition_display, confirmation, insight])

        # Apply Weighting System to Generate Execution Readiness Score
        total_score = 0
        max_possible_score = 0

        for row in summary:
            if row[0] == timeframe:  # Ensure we're applying the score for the correct timeframe
                indicator = row[1]
                confirmation = row[4]

                # Get the weighting of the indicator
                weight = indicator_weights.get(indicator, 0)  # Default to 0 if not found

                # Only count indicators that are selected
                if weight > 0:
                    max_possible_score += weight

                    # Apply weight based on confirmation status
                    if "✅" in confirmation:
                        total_score += weight
                        confirming_indicators += 1
                    elif "⚠️" in confirmation:
                        total_score -= weight

        # Compute Execution Readiness Score (Using Ratio-Based Normalization)
        alignment_ratio = total_score / max_possible_score if max_possible_score > 0 else 0

        # Special Handling for No Applicable Indicators
        if max_possible_score == 0:
            timeframe_summary[timeframe] = "ℹ️ No applicable indicators for this timeframe."
            continue

        # Generate Execution Readiness Summary based on Alignment Ratio
        if alignment_ratio >= 0.85:  # ✅ Strong Alignment
            timeframe_summary[timeframe] = "✅ Indicators strongly align with detected trends."
        elif alignment_ratio >= 0.33:  # ✅ If at least one-third of the max score confirms trend
            timeframe_summary[timeframe] = "⚠️ Mixed signals detected."
        elif alignment_ratio >= -0.20:  # ✅ If trend signals contradict but not entirely
            timeframe_summary[timeframe] = "⚠️ Some indicators contradict detected trends."
        else:  # If more than 20% are contradicting trend
            timeframe_summary[timeframe] = "🚨 No alignment detected—trends are conflicting."

    return pd.DataFrame(summary, columns=["Timeframe", "Indicator", "Signal",
    "Predisposition", "Confirmation", "Insight"]), timeframe_summary

# **Execution Readiness Display**
if filtered_df is not None:
    summary_df, timeframe_summary = compute_execution_readiness(filtered_df, predisposition,
     selected_indicators)

    st.subheader("📊 Execution Readiness Summary")
    st.write(f"Evaluating **{DATA_TITLE}** for execution readiness.")

    timeframe_table = pd.DataFrame(
            [{"Timeframe": tf, "Execution Readiness": status} for tf,
            status in timeframe_summary.items()]
        )

st.subheader("📈 Timeframe Execution Readiness")
st.dataframe(timeframe_table)

# **Detect Support & Resistance Levels & Align with Predisposition**
def detect_support_resistance(df, predisposition):
    # Always return a tuple, even if input is missing
    if df is None or df.empty:
        return [], [], "ℹ️ No data available for support/resistance detection."

    df = df.copy().reset_index(drop=True)

    # Guard: ensure expected column exists
    if "close" not in df.columns:
        return [], [], "⚠️ Missing `close` column — cannot detect support/resistance."

    peaks, _ = scipy.signal.find_peaks(df["close"], distance=5)
    troughs, _ = scipy.signal.find_peaks(-df["close"], distance=5)

    # Ensure valid index selection
    peaks = [p for p in peaks if 0 <= p < len(df)]
    troughs = [t for t in troughs if 0 <= t < len(df)]

    resistance_levels = (
        df.loc[peaks, "close"].sort_values(ascending=False).head(2).tolist()
        if peaks else []
    )
    support_levels = (
        df.loc[troughs, "close"].sort_values().head(2).tolist()
        if troughs else []
    )

    if predisposition == "Bullish":
        key_level_msg = (
            f"✅ **Bullish Bias** - Watching Support at {support_levels} "
            "for potential confirmation."
        )
    elif predisposition == "Bearish":
        key_level_msg = (
            f"⚠️ **Bearish Bias** - Watching Resistance at {resistance_levels} "
            "for potential confirmation."
        )
    else:
        key_level_msg = "ℹ️ **Neutral Bias** - Monitoring price movement relative to key levels."

    return support_levels, resistance_levels, key_level_msg


# **Tabs for Short, Medium, Full Data Views**
tab1, tab2, tab3 = st.tabs(["📉 Short-Term (50 Days)",
"📊 Medium-Term (200 Days)", "📈 Full Data (Filtered)"])

for tab, timeframe, data_slice, tab_key in [
    (tab1, "📉 Short-Term (50 Days)", filtered_df.tail(50), "short"),
    (tab2, "📊 Medium-Term (200 Days)", filtered_df.tail(200), "medium"),
    (tab3, "📈 Full Data (Filtered)", filtered_df, "full")
]:
    with tab:
        st.subheader(timeframe)

        # **Naked Charts**
        if selected_use_case == "Naked Charts":
            st.subheader("📉 Naked Chart (Price Only)")
            st.plotly_chart(
            plot_naked_chart(
            data_slice), width='stretch',
            key=f"naked_chart_{tab_key}")

        #  **Performance Charts**
        performance_indicators = selected_indicators.get("Performance", [])
        if performance_indicators:
            st.subheader("📊 Performance Breakdown")
            if "Winning vs. Losing" in performance_indicators:
                period = indicator_params.get("Winning vs. Losing", 14)
                st.plotly_chart(
                plot_winning_vs_losing_periods(
                data_slice, period), width='stretch',
                key=f"win_loss_{tab_key}_{period}")

            if "Rolling Returns" in performance_indicators:
                period = indicator_params.get("Rolling Returns", 14)
                st.plotly_chart(
                plot_rolling_returns(
                data_slice, period), width='stretch',
                key=f"rolling_returns_{tab_key}_{period}")

            if "Volatility-Adjusted Returns" in performance_indicators:
                period = indicator_params.get("Volatility-Adjusted Returns", 14)
                st.plotly_chart(
                plot_volatility_adjusted_returns(
                data_slice, period), width='stretch',
                key=f"var_{tab_key}_{period}")

        #  **Trend & Momentum Chart**
        trend_indicators = selected_indicators.get("Trend & Momentum", [])
        if trend_indicators:
            st.subheader("📊 Trend & Momentum Analysis")
            st.plotly_chart(create_price_action_chart(data_slice, trend_indicators, indicator_params), width='stretch', key=f"trend_chart_{tab_key}")

            if "Volume-Based Confirmation" in trend_indicators:
                period = indicator_params.get("Volume-Based Confirmation", 14)
                st.subheader("📊 Volume-Based Confirmation")
                st.plotly_chart(plot_volume_based_confirmation(data_slice, period), width='stretch', key=f"volume_conf_{tab_key}_{period}")

        #  **Breakout & Mean Reversion Chart**
        breakout_indicators = selected_indicators.get("Breakout & Mean Reversion", [])
        if breakout_indicators:
            st.subheader("📊 Breakout & Mean Reversion")
            st.plotly_chart(plot_breakout_mean_reversion_chart(data_slice, breakout_indicators, indicator_params), width='stretch', key=f"breakout_chart_{tab_key}")

        if "Volume vs. Price Range Compression" in breakout_indicators:
            period = indicator_params.get("Volume vs. Price Range Compression", 20)
            st.subheader("📊 Volume vs. Price Compression")
            st.plotly_chart(
                plot_volume_price_range_compression(data_slice, breakout_indicators, period),
                width='stretch',
                key=f"vprc_{tab_key}_{period}"
            )

        support, resistance, key_msg = detect_support_resistance(data_slice, predisposition)
        st.info(f"📌 **{timeframe} Support Levels:** {support} | **Resistance Levels:** {resistance}\n{key_msg}")

        #  **Tabs for Detailed Breakdown**
        tab1a, tab1b = st.tabs(["🔍 Price Action Confirmation", "⚠️ Red Flags"])

        with tab1a:
            st.subheader("🔍 Price Action Confirmation")
            gb = GridOptionsBuilder.from_dataframe(summary_df)
            gb.configure_default_column(wrapText=True, autoHeight=True)
            gb.configure_grid_options(domLayout='autoHeight')
            AgGrid(
                summary_df.copy(),
                gridOptions=gb.build(),
                height=500,
                fit_columns_on_grid_load=True,
                custom_css=AGGRID_NUNITO_CSS,
                key=f"confirmation_grid_{timeframe}",
            )


        with tab1b:
            st.subheader("⚠️ Red Flags")
            red_flags = summary_df.loc[
                summary_df["Confirmation"].str.contains("⚠️", na=False)
            ].copy()
            if not red_flags.empty:
                st.warning("🚨 Potential Issues Detected")
                gb_red_flags = GridOptionsBuilder.from_dataframe(red_flags)
                gb_red_flags.configure_default_column(wrapText=True, autoHeight=True)
                gb_red_flags.configure_grid_options(domLayout='autoHeight')
                AgGrid(
                    red_flags.copy(),
                    gridOptions=gb_red_flags.build(),
                    height=500,
                    fit_columns_on_grid_load=True,
                    custom_css=AGGRID_NUNITO_CSS,
                    key=f"red_flags_grid_{timeframe}",
                )
            else:
                st.success("✅ No major red flags detected.")

st.divider()

# -------------------------------------------------------------------------------------------------
# About & Support
# -------------------------------------------------------------------------------------------------
with st.sidebar.expander("ℹ️ About & Support"):
    support_md = load_markdown_file(ABOUT_SUPPORT_MD)
    if support_md:
        st.markdown(support_md, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------------------------------------
st.divider()

st.caption(
    "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — \
    No trading, investment, or policy advice provided."
)
