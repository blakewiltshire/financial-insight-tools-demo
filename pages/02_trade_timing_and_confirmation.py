# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Trade Timing & Confirmation

Streamlit app for analysing Trade Timing & Confirmation using predefined use cases,
visual indicators, and contextual insights. Designed to be modular, AI-augmented,
and fully interoperable with the
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
import altair as alt
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_trade_timing_and_confirmation.md")
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
from helpers.use_case_helpers_trade_timing import (
    generate_use_case_help_text,
    apply_use_case_mapping,
    resolve_canonical_use_case
)

from use_cases.trade_timing_definitions import USE_CASES

# --- Indicator Config ---
from use_cases.trade_timing_indicators import (
    options_trend_confirmation_map, options_momentum_strength_map, options_volatility_risk_map,
    options_volume_confirmation_map, options_pattern_recognition_map
)

# --- Insights ---
from use_cases.trade_timing_insights import generate_insights

# --- Charting & Visualisation  ---
from use_cases.trade_timing_charting import (
    plot_naked_chart, create_plotly_chart
)


# -------------------------------------------------------------------------------------------------
# Filtering Options (Ranges, Events and Temporal)
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.filtering_options import filtering_options_map
# from extensions.filtering_options import filtering_options_map

# -------------------------------------------------------------------------------------------------
# Reminder: __init__.py
# Ensure all relevant folders (e.g., /helpers, /use_cases, /data_sources etc)
# contain an empty __init__.py file.
# This marks them as Python packages and allows import resolution (especially important when
# running via Streamlit or exporting to other Python environments).
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Trade Timing & Confirmation", layout="wide")
st.title('⏳ Trade Timing & Confirmation')
st.caption("*Evaluate breakout potential, trend strength, and institutional sentiment.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📖 About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_trade_timing_and_confirmation.md")

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
st.sidebar.title('🔎 Select Asset for Trade Timing')

# --- Uploaded Asset Defaults ---
UPLOADED_FILE = None
DATA_TITLE = ''  # Default title is empty, no predefined title
ASSET_TYPE = ""  # Default asset type is empty, needs to be selected

# --- Data source method ---
data_source = st.sidebar.selectbox(
    'Choose your data source',
    ['Preloaded Asset Types (Default)']
)

# --- Preloaded Assets ---
preloaded_assets_default = get_preloaded_assets()
preloaded_assets_user = get_user_preloaded_assets()

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
indicator_categories = {
    "Trend Confirmation": options_trend_confirmation_map,
    "Momentum & Strength": options_momentum_strength_map,
    "Volatility & Risk": options_volatility_risk_map,
    "Volume Confirmation": options_volume_confirmation_map,
    "Pattern Recognition": options_pattern_recognition_map,
}

selected_indicators = {}
indicator_params = {}

# **Predefine Default Periods for All Indicators**
default_periods = {
    "Average Directional Index": 14,
    "Parabolic SAR": 14,
    "Simple Moving Average": 50,
    "Exponential Moving Average": 50,
    "Super Trend": 14,
    "Relative Strength Index": 14,
    "Moving Average Convergence Divergence": None,  # (Defaults Only)
    "Chande Momentum Oscillator": 20,
    "Money Flow Index": 14,
    "Bollinger Bands": 20,
    "Average True Range": 14,
    "Standard Deviation": 20,
    "On-Balance Volume": None,  # (Defaults Only)
    "Accumulation/Distribution Line": None,  # (Defaults Only)
    "Candlestick Patterns": None,  # No period required
    "Head & Shoulders": None,  # No period required
    "Flags & Pennants": None,  # No period required
    "Double Tops/Bottoms": None,  # No period required
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

# Sidebar: Indicator Selection
st.sidebar.title("📊 Customise Trade Execution Readiness Parameters")

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
            default=default_selection  # This behaves like a user clicking them
        )

        # Store final selected indicators per category
        selected_indicators[category] = list(set(selected))

        # Add sliders where applicable (Only for indicators that require a period)
        for indicator in selected:
            if indicator in default_periods and default_periods[indicator] is not None:
                indicator_params[indicator] = st.sidebar.slider(
                    f"{indicator} Period",
                    min_value=5, max_value=50,  # Keeps range consistent across indicators
                    value=default_periods[indicator],  # Default period is pre-defined
                    step=1
                )

# **Indicator Timeframe Suitability**
indicator_timeframes = {
    "Average Directional Index": ["Daily", "Weekly", "Monthly"],
    "Parabolic SAR": ["Daily", "Weekly"],
    "Simple Moving Average": ["Daily", "Weekly", "Monthly"],
    "Exponential Moving Average": ["Daily", "Weekly", "Monthly"],
    "Super Trend": ["Daily", "Weekly"],
    "Relative Strength Index": ["Daily", "Weekly"],
    "Moving Average Convergence Divergence": ["Daily", "Weekly"],
    "Chande Momentum Oscillator": ["Daily", "Weekly"],
    "Money Flow Index": ["Daily", "Weekly"],
    "Bollinger Bands": ["Daily", "Weekly"],
    "Average True Range": ["Daily", "Weekly"],
    "Standard Deviation": ["Daily", "Weekly"],
    "On-Balance Volume": ["Weekly", "Monthly"],
    "Accumulation/Distribution Line": ["Weekly", "Monthly"],
    "Candlestick Patterns": ["Daily", "Weekly"],
    "Head & Shoulders": ["Weekly", "Monthly"],
    "Flags & Pennants": ["Daily", "Weekly"],
    "Double Tops/Bottoms": ["Daily", "Weekly"]
}

# **Updated Timeframes**
timeframes = ["Daily", "Weekly", "Monthly"]

insight_name_map = {
    "Average Directional Index": "Average Directional Index",
    "Parabolic SAR": "Parabolic SAR",
    "Simple Moving Average": "Simple Moving Average",
    "Exponential Moving Average": "Exponential Moving Average",
    "Super Trend": "Super Trend",
    "Relative Strength Index": "Relative Strength Index",
    "Moving Average Convergence Divergence": "Moving Average Convergence Divergence",
    "Chande Momentum Oscillator": "Chande Momentum Oscillator",
    "Money Flow Index": "Money Flow Index",
    "Bollinger Bands": "Bollinger Bands",
    "Average True Range": "Average True Range",
    "Standard Deviation": "Standard Deviation",
    "On-Balance Volume": "On-Balance Volume",
    "Accumulation/Distribution Line": "Accumulation/Distribution Line",
    "Candlestick Patterns": "Candlestick Patterns",
    "Head & Shoulders": "Head & Shoulders",
    "Flags & Pennants": "Flags & Pennants",
    "Double Tops/Bottoms": "Double Tops/Bottoms"
}

#Trend Strength Indicators
trend_strength_indicators = [
    "Average Directional Index", "Super Trend", "Simple Moving Average",
    "Exponential Moving Average", "Chande Momentum Oscillator", "Money Flow Index"
]

#Predisposition Mapping
predisposition_map = {
    "Bullish": [
        "Bullish", "Breakout", "Support Holding", "Bullish Engulfing", "Bullish Crossover",
        "Strong Buying Pressure", "Overbought", "Overextended Overbought", "Price breaking upper band",
        "Price breaking outside Keltner Channel", "Volume Confirming Trend", "Strong Uptrend",
        "High Volatility", "Accumulation—Buying Pressure"
    ],
    "Bearish": [
        "Bearish", "Failed Breakout", "Resistance Holding", "Bearish Engulfing", "Bearish Crossover",
        "Strong Selling Pressure", "Oversold", "Deeply Oversold", "Price breaking lower band",
        "Price breaking below Keltner Channel", "Divergence", "Strong Downtrend", "High Volatility",
        "Distribution—Selling Pressure"
    ],
    # Trend Strength Only Indicators (Non-Bullish/Bearish)
    "Trend Strength": [
        "Strong Trend", "Trend Confirmed", "Confirmed Trend", "Strong Momentum", "Strong Buying/Selling Pressure"
    ]
}


# Indicator Weighting System (Updated)
indicator_weights = {
    # **Trend Strength Indicators (Weight = 3)**
    "Average Directional Index": 3,
    "Super Trend": 3,
    "Simple Moving Average": 3,
    "Exponential Moving Average": 3,
    "On-Balance Volume": 3,
    "Accumulation/Distribution Line": 3,

    # **Momentum & Volatility Indicators (Weight = 2)**
    "Relative Strength Index": 2,
    "Moving Average Convergence Divergence": 2,
    "Chande Momentum Oscillator": 2,
    "Money Flow Index": 2,
    "Bollinger Bands": 2,
    "Average True Range": 2,
    "Parabolic SAR": 2,

    # **Insights Only (Not Scored)**
    "Standard Deviation": 0,  # ❌ Insight only, used for Bollinger Band calculations
    "Candlestick Patterns": 0,
    "Head & Shoulders": 0,
    "Flags & Pennants": 0,
    "Double Tops/Bottoms": 0
}

# Execution Readiness Computation (Fixed with Adaptive Classification)
def compute_execution_readiness(df, predisposition, selected_indicators):
    summary = []
    timeframe_summary = {}

    for timeframe in timeframes:
        df_resampled = resample_data(df.copy(), timeframe)
        if df_resampled is None or df_resampled.empty:
            timeframe_summary[timeframe] = "⚠️ Insufficient Data"
            continue

        # Apply Weighting System to Generate Execution Readiness Score
        total_score = 0
        max_possible_score = 0
        confirming_indicators = 0  # ✅ Track count of confirming indicators

        for category, indicators in indicator_categories.items():
            for indicator in selected_indicators.get(category, []):
                if timeframe not in indicator_timeframes.get(indicator, []):
                    continue

                func = indicators[indicator]
                period = indicator_params.get(indicator)
                signal = func(df_resampled, period) if period else func(df_resampled)

                # Handle Trend Strength Indicators Separately (No Bullish/Bearish)
                if indicator in trend_strength_indicators:
                    predisposition_display = "N/A"
                    if signal in predisposition_map["Trend Strength"]:
                        confirmation = "✅ Trend strength detected."
                    else:
                        confirmation = "⚠️ No strong trend detected."
                else:
                    predisposition_display = predisposition
                    if signal in predisposition_map[predisposition]:
                        confirmation = f"✅ {signal} aligns with selected market conditions."
                    else:
                        confirmation = f"⚠️ {signal} differs from selected market conditions."

                # Store in summary for Key Technical Confirmation & Red Flags
                insight = generate_insights(insight_name_map.get(indicator, indicator), signal, timeframe, predisposition)
                summary.append([timeframe, indicator, signal, predisposition_display, confirmation, insight])

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
        if alignment_ratio >= 0.85:  # Strong Alignment
            timeframe_summary[timeframe] = "Indicators strongly align with detected trends."
        elif alignment_ratio >= 0.33:  # If at least one-third of the max score confirms trend
            timeframe_summary[timeframe] = "⚠️ Mixed signals detected."
        elif alignment_ratio >= -0.20:  # If trend signals contradict but not entirely
            timeframe_summary[timeframe] = "⚠️ Some indicators contradict detected trends."
        else:  # If more than 20% are contradicting trend
            timeframe_summary[timeframe] = "🚨 No alignment detected—trends are conflicting."

    return pd.DataFrame(summary, columns=["Timeframe", "Indicator", "Signal", "Predisposition", "Confirmation", "Insight"]), timeframe_summary

# **Execution Readiness Display**
if filtered_df is not None:
    summary_df, timeframe_summary = compute_execution_readiness(filtered_df, predisposition, selected_indicators)

    st.subheader("📊 Execution Readiness Summary")
    st.write(f"Evaluating **{DATA_TITLE}** for execution readiness.")

    timeframe_table = pd.DataFrame(
            [{"Timeframe": tf, "Execution Readiness": status} for tf, status in timeframe_summary.items()]
        )

st.subheader("📈 Timeframe Execution Readiness")
st.dataframe(timeframe_table)

# **Detect Support & Resistance Levels & Align with Predisposition**
def detect_support_resistance(df, predisposition):
    df = df.copy().reset_index()  # Ensure numerical index for safe indexing

    peaks, _ = scipy.signal.find_peaks(df['close'], distance=5)
    troughs, _ = scipy.signal.find_peaks(-df['close'], distance=5)

    # Ensure valid index selection
    peaks = [p for p in peaks if p in df.index]
    troughs = [t for t in troughs if t in df.index]

    resistance_levels = df.loc[peaks, 'close'].sort_values(ascending=False).head(2).tolist() if peaks else []
    support_levels = df.loc[troughs, 'close'].sort_values().head(2).tolist() if troughs else []

    # Highlight levels based on predisposition
    if predisposition == "Bullish":
        key_level_msg = f"✅ **Bullish Bias** - Watching Support at {support_levels} for potential confirmation."
    elif predisposition == "Bearish":
        key_level_msg = f"⚠️ **Bearish Bias** - Watching Resistance at {resistance_levels} for potential confirmation."
    else:
        key_level_msg = "ℹ️ **Neutral Bias** - Monitoring price movement relative to key levels."

    return support_levels, resistance_levels, key_level_msg

# **Tabs for Short, Medium, Full Data Views**
tab1, tab2, tab3 = st.tabs([
    "📉 Short-Term (50 Days)",
    "📊 Medium-Term (200 Days)",
    "📈 Full Data (Filtered)"
])

# **Loop Through All Timeframes**
for tab, timeframe, data_slice in [
    (tab1, "📉 Short-Term (50 Days)", processed_df.tail(50)),
    (tab2, "📊 Medium-Term (200 Days)", processed_df.tail(200)),
    (tab3, "📈 Full Data (Filtered)", filtered_df)
]:
    with tab:
        st.subheader(timeframe)

        # **Generate Plotly Chart for Price & Indicators (Including OBV & A/D)**
        indicators_to_plot = (
            selected_indicators.get("Trend Confirmation", []) +
            selected_indicators.get("Momentum & Strength", []) +
            selected_indicators.get("Volatility & Risk", []) +
            selected_indicators.get("Volume Confirmation", [])  # Now included in main chart!
        )

        price_chart = create_plotly_chart(data_slice, indicators_to_plot, indicator_params)
        st.plotly_chart(price_chart, width='stretch')

        # **Detect Support & Resistance Levels**
        support, resistance, key_msg = detect_support_resistance(data_slice, predisposition)

        # **Display Support & Resistance Levels**
        st.info(f"📌 **{timeframe} Support Levels:** {support} | **Resistance Levels:** {resistance}\n{key_msg}")

        # **Tabs for Detailed Breakdown**
        tab1a, tab1b = st.tabs(["🔍 Key Technical Confirmation", "⚠️ Red Flags"])

        with tab1a:
            st.subheader("🔍 Key Technical Confirmation")
            gb = GridOptionsBuilder.from_dataframe(summary_df)
            gb.configure_default_column(wrapText=True, autoHeight=True)
            gb.configure_grid_options(domLayout='autoHeight')
            AgGrid(summary_df, gridOptions=gb.build(), height=500, fit_columns_on_grid_load=True, key=f'confirmation_grid_{timeframe}')



        with tab1b:
            st.subheader("⚠️ Red Flags")
            red_flags = summary_df[summary_df["Confirmation"].str.contains("⚠️", na=False)]
            if not red_flags.empty:
                st.warning("🚨 Potential Issues Detected")
                gb_red_flags = GridOptionsBuilder.from_dataframe(red_flags)
                gb_red_flags.configure_default_column(wrapText=True, autoHeight=True)
                gb_red_flags.configure_grid_options(domLayout='autoHeight')
                AgGrid(red_flags, gridOptions=gb_red_flags.build(), height=500, fit_columns_on_grid_load=True, key=f'red_flags_grid_{timeframe}')
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
