# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name
# pylint: disable=non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
🔎 Market & Volatility Scanner

This Streamlit app provides dynamic asset-level and group-level analysis for
volatility classification, return resampling, and correlation assessment across
multiple timeframes. It supports both preloaded and user-uploaded datasets, offering
statistical insights across key financial metrics.

Core Functions:
- Load and clean financial data from preloaded asset maps or user-uploaded CSVs
- Classify volatility using ATR and standard deviation metrics
- Resample returns across Weekly, Monthly, Quarterly, and Yearly periods
- Evaluate DPT (Desired Profit Target) probabilities based on directional strategies
- Apply descriptive, risk-based, and dynamic statistical filters
- Visualise price movements, returns, and volatility relationships via multiple chart types
- Support comparative correlation analysis between base assets and grouped/uploaded datasets

Technical Architecture:
- Modular import structure with standardised cleaning via `processing_correlation.py`
- Context-aware filtering via `filtering_options_map`
- Statistical modules defined in `/use_cases/statistical_analysis/*`
- Visualisation handled via `options_data_visualisations_map`
- Fully integrated with Financial Insight Tools DSS: asset_map.py, preloaded snapshots,
  user uploads, and structured correlation overlays

Note:
This application is intended for decision support. It does not provide trading, investment,
or policy advice. To extend preloaded assets, updates must be made in
`asset_map.py`, `preloaded_assets.py`, and supporting snapshot logic.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import sys

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, UTC

# -------------------------------------------------------------------------------------------------
# Core Utilities — load shared pathing tools, markdown loaders, sidebar links etc.
# -------------------------------------------------------------------------------------------------
from core.helpers import (  # pylint: disable=import-error
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
APPS_PATH = PATHS["level_up_2"]

# -------------------------------------------------------------------------------------------------
# Shared Assets — Markdown and branding used across all apps
# -------------------------------------------------------------------------------------------------
ABOUT_APP_MD = os.path.join(ROOT_PATH, "docs", "about_market_and_volatility_scanner.md")
HELP_APP_MD = os.path.join(ROOT_PATH, "docs", "help_market_volatility_scanner.md")
ABOUT_SUPPORT_MD = os.path.join(ROOT_PATH, "docs", "about_and_support.md")
BRAND_LOGO_PATH = os.path.join(ROOT_PATH, "brand", "blake_logo.png")
DEFAULT_ASSET_SNAPSHOT_PATH = os.path.join(APPS_PATH, "data_sources", "financial_data",
"preprocessed_default", "preloaded_asset_summary.pkl")
USER_ASSET_SNAPSHOT_PATH = os.path.join(APPS_PATH, "data_sources", "financial_data",
"preprocessed_user", "preloaded_asset_summary.pkl")

# -------------------------------------------------------------------------------------------------
# Observation Engine Path — Enable observation tools (form + journal)
# -------------------------------------------------------------------------------------------------
sys.path.append(os.path.join(APPS_PATH, "observation_engine"))

# -------------------------------------------------------------------------------------------------
# Clean and format asset files
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.processing_correlation import (
    calculate_atr, resample_and_calculate_returns, clean_data, clean_generic_data,
    load_asset_data, load_data_from_file
)

from data_sources.financial_data.shared_utils import convert_date_to_us_format

from data_sources.financial_data.processing_correlation_assets.equities import (
    load_and_clean_equities_7, load_and_clean_equities_const
)

from data_sources.financial_data.processing_correlation_assets.market_indices import (
    load_and_clean_market_indices
)

from data_sources.financial_data.processing_correlation_assets.currencies import (
    load_and_clean_currency
)

from data_sources.financial_data.processing_correlation_assets.crypto import (
    load_and_clean_cryptocurrency
)

from data_sources.financial_data.processing_correlation_assets.commodities import (
    load_and_clean_commodities
)

from data_sources.financial_data.processing_correlation_assets.etfs import (
    load_and_clean_popular, load_and_clean_sectors, load_and_clean_countries
)

from data_sources.financial_data.processing_correlation_assets.bonds import (
    load_and_clean_short_term_bonds, load_and_clean_long_term_bonds
)

from data_sources.financial_data.processing_correlation_assets.user_uploads import (
    load_and_clean_user_correlations,
    load_and_clean_user_volatility,
    load_and_prepare_user_returns
)

# -------------------------------------------------------------------------------------------------
# Mapping Logic
# -------------------------------------------------------------------------------------------------
from data_sources.financial_data.preloaded_assets import get_preloaded_assets
from data_sources.financial_data.user_preloaded_assets import get_user_preloaded_assets
from data_sources.financial_data.asset_map import get_asset_path
from data_sources.financial_data.user_asset_map import get_user_asset_path

# -------------------------------------------------------------------------------------------------
# Load statistical mappings
# -------------------------------------------------------------------------------------------------
from helpers.statistical_option_mapping import get_data_mapping

correlation_mapping = get_data_mapping("correlation")
volatility_mapping = get_data_mapping("volatility")
returns_mapping = get_data_mapping("returns")

# -------------------------------------------------------------------------------------------------
# Analysis Modules
# -------------------------------------------------------------------------------------------------
from use_cases.statistical_analysis.strategy.strategy_simulation_metrics import options_maps

from use_cases.statistical_analysis.summary.asset_analysis_summary import (
    calculate_asset_metrics_basic, calculate_asset_returns, calculate_asset_metrics,
    calculate_volatility, overview_metrics, calculate_and_format_atr, calculate_probability_of_dpt
)

from use_cases.statistical_analysis.descriptive.descriptive_statistics \
    import options_descriptive_statistics_map

from use_cases.statistical_analysis.risk.monte_carlo_and_risk_metrics import (
    calculate_probability_of_dpt_advanced, options_risk_and_uncertainty_map
)

from use_cases.statistical_analysis.dynamics.market_dynamics \
    import options_market_dynamics_map

from use_cases.statistical_analysis.performance.performance_metrics_and_correlations import (
    pearsons_or_spearmans_correlation,
    pearsons_or_spearmans_correlation_user, generate_correlation_heatmap,
    volatility_assets, volatility_assets_user, options_performance_and_correlation_map
)

from use_cases.statistical_analysis.visualisations.visualisations import (
    chart_returns, scatterplot_dpt_vs_volatility, returns_visualisation,
    user_returns, cumulative_returns, rolling_returns, risk_return_scatter_plot,
    options_data_visualisations_map
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
# Streamlit Page Setup
# -------------------------------------------------------------------------------------------------
st.set_page_config(page_title="Market & Volatility Scanner", layout="wide")
st.title('🔎 Market & Volatility Scanner')
st.caption("*Assess asset-specific volatility patterns, return probabilities, and time filters.*")

# -------------------------------------------------------------------------------------------------
# Load About Markdown (auto-skips if not replaced)
# -------------------------------------------------------------------------------------------------
with st.expander("📖 About This App"):
    content = load_markdown_file(ABOUT_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/about_market_and_volatility_scanner.md")

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

# # -------------------------------------------------------------------------------------------------
# # Asset Selection Logic (Preloaded + User Upload)
# # -------------------------------------------------------------------------------------------------
st.sidebar.title('🔎 Select Asset')

# --- Uploaded Asset Defaults ---
UPLOADED_FILE = None
DATA_TITLE = ''  # Default title is empty, no predefined title
ASSET_TYPE = ""  # Default asset type is empty, needs to be selected

# --- Data source method ---
data_source = st.sidebar.selectbox(
    'Choose your data source',
    ['Preloaded Asset Types (Default)']
)

# Track which source is being used (for later correlation group logic)
st.session_state['ASSET_SOURCE_TYPE'] = data_source

# --- Preloaded Assets: Default and User ---
preloaded_assets_default = get_preloaded_assets()
preloaded_assets_user = get_user_preloaded_assets()

# --- Preloaded Assets (Default) ---
if data_source == 'Preloaded Asset Types (Default)':
    asset_category = st.sidebar.selectbox("Select Asset Category", list(preloaded_assets_default.keys()))
    asset_sample = st.sidebar.selectbox("Select Base Asset", preloaded_assets_default[asset_category])
    if asset_sample:
        DATA_TITLE = asset_sample
        ASSET_TYPE = asset_category
        asset_path = get_asset_path(asset_category, asset_sample)

# --- Fallback logic (optional if asset_path needed before conditional use) ---
if data_source.startswith("Preloaded") and asset_sample:
    if asset_path is None:
        st.error("Asset file not found. Please check the file name or structure.")

# -------------------------------------------------------------------------------------------------
# Timeline and DPT Controls
# -------------------------------------------------------------------------------------------------
st.sidebar.subheader("Select Timeline for Analysis")
timeline = st.sidebar.selectbox(
    'Select Timeline for Analysis',
    ['Intraday', 'Overnight', 'Interday', 'Daily H-L'],
    index=2,
    help="Select the timeline you want to analyse: Intraday, Overnight, Interday, or their High to Lows."
)

# Desired Profit Target (DPT) with step of 1%
st.sidebar.subheader("Desired Profit Target (%)")
desired_profit_target = st.sidebar.number_input(
    "Desired Profit Target (%)",
    min_value=1,
    max_value=100,
    value=1,
    step=1,
    help="Select the target profit percentage you aim to achieve."
)

# Desired Direction (Up or Down)
st.sidebar.subheader("Select Direction")
direction = st.sidebar.selectbox(
    "Select Direction", ['Up', 'Down'],
    help="Choose the direction of the trade (e.g., Up means you expect the price to go higher)."
)

# -------------------------------------------------------------------------------------------------
# Data Load and Cleaning Pipeline
# -------------------------------------------------------------------------------------------------
try:
    if data_source == 'Upload my own files':
        if uploaded_file is not None:
            processed_df = load_data_from_file(uploaded_file, timeline, desired_profit_target)
        else:
            st.info("Please upload a CSV file.")
            st.stop()

    elif data_source == 'Preloaded Asset Types (Default)' and asset_sample:
        processed_df, DATA_TITLE, ASSET_TYPE = load_asset_data(
            asset_category, asset_sample, timeline, desired_profit_target
        )

    elif data_source == 'Preloaded Asset Types (User)' and asset_sample:
        asset_path = get_user_asset_path(asset_category, asset_sample)

        if asset_path is None:
            st.error("User asset path not found. Please check structure.")
            st.stop()

        processed_df = load_data_from_file(asset_path, timeline, desired_profit_target)
        DATA_TITLE = asset_sample
        ASSET_TYPE = asset_category

    else:
        st.error("No valid data source or asset selected.")
        st.stop()

    processed_df, weekly_returns_df, monthly_returns_df, quarterly_returns_df, \
        six_month_returns_df, yearly_returns_df, weekly_df, monthly_df, \
        start_date, end_date = clean_data(processed_df, timeline, desired_profit_target)

    if 'return' in processed_df.columns:
        volatility_category, formatted_message = calculate_volatility(processed_df, DATA_TITLE)
    else:
        st.error("The necessary data for volatility analysis ('return') is missing.")

except KeyError as e:
    st.error(f"Missing key column: {e}")
except ValueError as e:
    st.error(f"Value error during volatility calculation: {e}")
except Exception as e:
    st.error(f"Unexpected error: {e}")

# -------------------------------------------------------------------------------------------------
# Display for the selected data
# -------------------------------------------------------------------------------------------------
st.header("Analysis Summary")

# Calculate the last price and days since the last bear market
last_price, days_since_bear_market, current_drawdown, max_price, max_price_date, min_price, \
    min_price_date, high_price, high_price_date, low_price, \
    low_price_date, daily_return, weekly_return, \
    monthly_return = calculate_asset_metrics(processed_df
)

# Check if the user uploaded their own files or is using preloaded assets
if data_source == 'Upload my own files':
    asset_type_display = ASSET_TYPE  # Display the uploaded asset type
else:
    asset_type_display = asset_category  # Display the preloaded asset category

# Display in the Overview Section
st.markdown(f"""
**Current Data Set**: {DATA_TITLE}<br>
**Asset Type**: {asset_type_display}<br>
**Analysed Period**: Historical data from dates {start_date} to {end_date}<br>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------------------------------
# Analysis Summary - Snapshots
# -------------------------------------------------------------------------------------------------
if data_source in ["Preloaded Asset Types (Default)", "Preloaded Asset Types (User)"]:
    overview_tab0, overview_tab1, overview_tab2, overview_tab3, overview_tab4 = st.tabs(
        ["🧾 Asset Group Summary", "🧾 Asset Snapshot", "📊 Key Metrics",
         "📈 ATR & Returns", "🎯 DPT Probability"]
    )
else:
    overview_tab1, overview_tab2, overview_tab3, overview_tab4 = st.tabs(
        ["🧾 Asset Snapshot", "📊 Key Metrics", "📈 ATR & Returns", "🎯 DPT Probability"]
    )

# -------------------------------------------------------------------------------------------------
# Snapshot Group Summary — Only for Preloaded Types
# -------------------------------------------------------------------------------------------------
if data_source in ["Preloaded Asset Types (Default)", "Preloaded Asset Types (User)"]:
    with overview_tab0:
        try:
            snapshot_path = (
                DEFAULT_ASSET_SNAPSHOT_PATH if data_source == "Preloaded Asset Types (Default)"
                else USER_ASSET_SNAPSHOT_PATH
            )

            if os.path.exists(snapshot_path):
                snapshot_df = pd.read_pickle(snapshot_path)
                file_timestamp = os.path.getmtime(snapshot_path)
                snapshot_date = datetime.fromtimestamp(file_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                st.info(
                    f"📦 This group summary was generated using the **Asset Snapshot Scanner**.\n\n"
                    f"🗓️ Snapshot last updated: **{snapshot_date}**\n\n"
                    f"⚠️ *Note*: This timestamp reflects when the summary file was saved — "
                    f"individual assets may still have older data unless all underlying files were updated.\n\n"
                    f"🔄 To ensure full accuracy, consider rerunning the scanner after modifying or adding asset files."
                )

                snapshot_df["Asset Name"] = snapshot_df["Asset Name"].astype(str).str.strip()
                snapshot_df["Category"] = snapshot_df["Category"].astype(str).str.strip().str.lower()
                category_name_clean = asset_category.strip().lower()

                group_df = snapshot_df[snapshot_df["Category"] == category_name_clean].copy()

                if not group_df.empty:
                    group_df = group_df.drop(columns=["Category"], errors="ignore")
                    st.subheader("🧾 Asset Group Summary")
                    st.markdown(f"Snapshot metrics for **{asset_category.strip()}**")
                    st.data_editor(
                        group_df,
                        width='stretch',
                        column_config={
                            "1M % Chg": st.column_config.NumberColumn(format="%.2f %%"),
                            "YTD % Chg": st.column_config.NumberColumn(format="%.2f %%"),
                            "Last Close": st.column_config.NumberColumn(format="%.2f"),
                            "52w Low": st.column_config.NumberColumn(format="%.2f"),
                            "52w High": st.column_config.NumberColumn(format="%.2f"),
                            "52w Range": st.column_config.NumberColumn(format="%.2f"),
                            "Last 10 Days Return": st.column_config.BarChartColumn(y_min=-10, y_max=15)
                        },
                        disabled=True,
                        hide_index=True
                    )
                else:
                    st.info("No snapshot data found for this group.")
            else:
                st.info("**Asset Group Summaries are not included in the public demo**.")
        except Exception as error:
            st.error(f"❌ Could not load snapshot data: {error}")


# --- Asset Snapshot ---
with overview_tab1:
    st.subheader("🧾 Asset Snapshot")
    st.markdown(f"""
    **Current Data Set**: {DATA_TITLE}<br>
    **Asset Type**: {asset_type_display}<br>
    **Analysed Period**: {start_date} to {end_date}<br><br>
    **Last Price**: {last_price:.2f}<br>
    :gray[*(Most recent closing price.)*]<br><br>
    **Days Since Bear Market**: {days_since_bear_market} days<br>
    :gray[*(Days since a 20%+ decline from the high.)*]<br><br>
    **Current Drawdown**: {current_drawdown:.2f}%<br>
    :gray[*(Drop from peak to current price.)*]<br><br>
    **Max Price**: {max_price:.2f} on {max_price_date.strftime('%m/%d/%Y')}<br>
    **Min Price**: {min_price:.2f} on {min_price_date.strftime('%m/%d/%Y')}<br>
    **High Price**: {high_price:.2f} on {high_price_date.strftime('%m/%d/%Y')}<br>
    **Low Price**: {low_price:.2f} on {low_price_date.strftime('%m/%d/%Y')}<br>
    """, unsafe_allow_html=True)

# --- Key Metrics ---
with overview_tab2:
    st.subheader("📊 Key Metrics")
    try:
        std_dev, mean_high_to_low_range = overview_metrics(processed_df, timeline)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Standard Deviation", f"{std_dev:.2f}%",
                      help="Price dispersion over the period (1 std dev).")
        with col2:
            st.metric("Mean High-to-Low", f"{mean_high_to_low_range:.2f}%",
                      help="Average daily range between high and low prices.")
    except Exception as e:
        st.error(f"Error in calculating overview metrics: {e}")

# --- ATR & Returns ---
with overview_tab3:
    st.subheader("📈 ATR & Returns")
    try:
        # ATR
        daily_atr_pct, weekly_atr_pct, monthly_atr_pct, \
        daily_atr_abs, weekly_atr_abs, monthly_atr_abs = calculate_and_format_atr(
            processed_df, weekly_df, monthly_df, ASSET_TYPE
        )

        atr_col1, atr_col2, atr_col3 = st.columns(3)
        with atr_col1:
            st.metric("Daily ATR (%)", daily_atr_pct)
            st.metric("Daily ATR ($)", daily_atr_abs)
        with atr_col2:
            st.metric("Weekly ATR (%)", weekly_atr_pct)
            st.metric("Weekly ATR ($)", weekly_atr_abs)
        with atr_col3:
            st.metric("Monthly ATR (%)", monthly_atr_pct)
            st.metric("Monthly ATR ($)", monthly_atr_abs)

        # Returns
        ret_col1, ret_col2, ret_col3 = st.columns(3)
        with ret_col1:
            st.metric("Daily Return", f"{daily_return:.2f}%")
        with ret_col2:
            st.metric("Weekly Return", f"{weekly_return:.2f}%")
        with ret_col3:
            st.metric("Monthly Return", f"{monthly_return:.2f}%")

    except Exception as e:
        st.error(f"An error occurred while loading ATR or returns data: {e}")

# --- DPT Probability ---
with overview_tab4:
    st.subheader("🎯 Probability of Hitting DPT")

    st.markdown(f"**Selected DPT**: {desired_profit_target:.1f}%")
    column_map = {
        'Intraday': 'Intraday',
        'Overnight': 'Overnight',
        'Interday': 'Interday',
        'Daily H-L': 'Daily H-L'
    }
    column = column_map[timeline]

    direction_message = {
        'Up': "Bullish position (Up)",
        'Down': "Bearish position (Down)"
    }

    opportunity_miss = {
        "High": "With **high volatility**, there is great opportunity, but large price swings \
can challenge the consistency of hitting targets.",
        "Medium": "With **medium volatility**, price moves are more controlled — less risky, \
but potentially fewer breakout moves.",
        "Low": "With **low volatility**, prices move within narrow bands — stable, but \
targets are harder to reach quickly."
    }

    if timeline == 'Daily H-L':
        st.info("Probability of hitting DPT is not available for the 'Daily H-L' timeline.")
    else:
        try:
            _, occurrences, count, _, _, _, _, approx = calculate_probability_of_dpt(
                processed_df, column, direction, desired_profit_target
            )

            if occurrences > 0:
                st.success(f"Hit {occurrences} out of {count} times — roughly 1 in {approx} days.")
            else:
                st.warning(f"Target not achieved during analysis period.\n\n{opportunity_miss[volatility_category]}")
        except Exception as e:
            st.error(f"Error calculating DPT probability: {e}")

# -------------------------------------------------------------------------------------------------
# Visualisations and Tends
# -------------------------------------------------------------------------------------------------
st.header("Charts")

# --- Price Movement & Trend Visualisation with collapsible expander ---
with st.expander("Price Movement & Trend Visualisation", expanded=False):  # Set expanded=False
    st.header("Price Movement & Trend Visualisation")

    # Create tabs for the different chart types
    tab1, tab2, tab3 = st.tabs(["Line Chart", "Candlestick Chart", "Area Chart"])

    # Display content for the Line Chart tab
    with tab1:
        st.write("This chart shows the overall price movement over the selected period.")
        options_data_visualisations_map["Price Movement - Line"](processed_df, timeline)

    # Display content for the Candlestick Chart tab. Filtered data for 3 months
    with tab2:
        st.write("Candlestick chart shows price movements for the last 3 months, with \
        color indicating market direction.")
        options_data_visualisations_map["Price Movement - Candlestick"](
            processed_df, timeline, use_filtered_data=True
        )

    # Display content for the Area Chart tab
    with tab3:
        st.write("Area chart displays price movements and trend over time.")
        options_data_visualisations_map["Trend Visualisation - Area"](processed_df, timeline)

# ─────────────────────────────────────────────────────────────────────────────
# Returns Section with collapsible expander
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("Returns", expanded=False):  # Set expanded=False to default
    st.subheader("Returns")
    st.write("Explore average returns across different time periods to \
    see how opportunity may vary over time.")

    # Resample the data and calculate returns
    weekly_returns_df, monthly_returns_df, quarterly_returns_df, \
    six_month_returns_df, yearly_returns_df = resample_and_calculate_returns(processed_df)

    # Tabs for different time periods
    returns_tab1, returns_tab2, returns_tab3, returns_tab4, returns_tab5 = st.tabs(
        ["Weekly", "1 Month", "3 Months", "6 Months", "12 Months"]
    )

    with returns_tab1:
        st.write(f"Average Returns from {start_date} to {end_date}")
        chart = chart_returns(weekly_returns_df, time_period='weekly', timeline=timeline)
        if chart is not None:
            st.plotly_chart(chart, theme="streamlit")

    with returns_tab2:
        st.write(f"Average Returns from {start_date} to {end_date}")
        chart = chart_returns(monthly_returns_df, time_period='monthly', timeline=timeline)
        if chart is not None:
            st.plotly_chart(chart, theme="streamlit")

    with returns_tab3:
        st.write(f"Average Returns from {start_date} to {end_date}")
        chart = chart_returns(quarterly_returns_df, time_period='quarterly', timeline=timeline)
        if chart is not None:
            st.plotly_chart(chart, theme="streamlit")

    with returns_tab4:
        st.write(f"Average Returns from {start_date} to {end_date}")
        chart = chart_returns(six_month_returns_df, time_period='halfyearly', timeline=timeline)
        if chart is not None:
            st.plotly_chart(chart, theme="streamlit")

    with returns_tab5:
        st.write(f"Average Returns from {start_date} to {end_date}")
        chart = chart_returns(yearly_returns_df, time_period='yearly', timeline=timeline)
        if chart is not None:
            st.plotly_chart(chart, theme="streamlit")
# ─────────────────────────────────────────────────────────────────────────────
# Volatility vs DPT Achievement section with collapsible option
# ─────────────────────────────────────────────────────────────────────────────

with st.expander("Volatility vs DPT Achievement", expanded=False):
    st.write("Explore how volatility aligns with the achievement of your \
    Desired Profit Target (DPT) over different time periods.")

    if timeline != 'Interday':
        st.info("For Volatility vs DPT Achievement, please choose the 'Interday' timeline.")
    else:
        COLUMN = 'Interday'  # Set this directly as we need it for Volatility calculation

        # Scatterplot for ATR (1 day, 1 week, 1 month)
        scatter_tab1, scatter_tab2, scatter_tab3 = st.tabs(
            ["1 Day ATR", "1 Week ATR", "1 Month ATR"]
        )

        with scatter_tab1:
            # Scatterplot for 1-day ATR and DPT Achievement
            fig_1d = scatterplot_dpt_vs_volatility(
                processed_df, direction, desired_profit_target, period='1d'
            )
            st.plotly_chart(fig_1d, theme="streamlit")

        with scatter_tab2:
            # Scatterplot for 1-week ATR and DPT Achievement
            fig_1w = scatterplot_dpt_vs_volatility(
                processed_df, direction, desired_profit_target, period='1w'
            )
            st.plotly_chart(fig_1w, theme="streamlit")

        with scatter_tab3:
            # Scatterplot for 3-month ATR and DPT Achievement
            fig_1m = scatterplot_dpt_vs_volatility(
                processed_df, direction, desired_profit_target, period='1m'
            )
            st.plotly_chart(fig_1m, theme="streamlit")

st.markdown("<hr>", unsafe_allow_html=True)  # Divider for better separation

# ─────────────────────────────────────────────────────────────────────────────
# Statistical Analysis Options
# ─────────────────────────────────────────────────────────────────────────────
st.header('Statistical Analysis')

with st.expander("ℹ️ Help: How to"):
    content = load_markdown_file(HELP_APP_MD)
    if content:
        st.markdown(content, unsafe_allow_html=True)
    else:
        st.error("File not found: docs/help_market_volatility_scanner.md")

# -------------------------------------------------------------------------------------------------
# Sidebar for Custom Date Range and Event-Based Analysis
# -------------------------------------------------------------------------------------------------
st.sidebar.header('Statistical Analysis')

# Sidebar for Filter Type
filter_type = st.sidebar.selectbox(
    "Choose Filter Type",
    list(filtering_options_map.keys()),  # Dynamically populate
    index=0  # Default to Range
)

# Initialize `filtered_df`
filtered_df = processed_df  # Default to full dataset

filter_applied_description = ""  # Default

# Apply Filters and Capture Filter Description
if filter_type == "Temporal Patterns":
    selected_pattern = st.sidebar.selectbox(
        "Select Temporal Pattern",
        list(filtering_options_map["Temporal Patterns"].keys())
    )

    filter_applied_description = f"Temporal Pattern: {selected_pattern}"
    filtered_df = filtering_options_map["Temporal Patterns"][selected_pattern](filtered_df)

elif filter_type == "Event-Based Analysis":
    # Show UI, filter, and extract event-specific settings
    filtered_df = filtering_options_map["Event-Based Analysis"](filtered_df)

    # Recover values using session state (Streamlit retains latest entries)
    event_date = st.session_state.get("event_date", "Not set")
    pre_days = st.session_state.get("pre_event_days", 5)
    post_days = st.session_state.get("post_event_days", 5)

    filter_applied_description = (
        f"Event-Based Analysis: Event Date = {event_date}, "
        f"Pre-event Window = {pre_days} days, Post-event Window = {post_days} days"
    )

else:
    # Default is range-based
    filtered_df = filtering_options_map[filter_type](filtered_df)
    try:
        start_date = st.session_state.get("Select Start Date", filtered_df["date"].min())
        end_date = st.session_state.get("Select End Date", filtered_df["date"].max())
        filter_applied_description = f"Date Range: {start_date} to {end_date}"
    except Exception:
        filter_applied_description = "Range filter applied (date range unknown)"

# -------------------------------------------------------------------------------------------------
# 🧮 Descriptive Statistics — Sidebar Selection and Result Capture
# -------------------------------------------------------------------------------------------------
for header, (options_map, categories) in options_maps.items():
    if header == 'Descriptive Statistics':
        all_selected_options = []
        with st.sidebar.expander(header):
            for category, options in categories.items():
                selected_options = st.multiselect(
                    f'Select options for {category}',
                    options=options,
                    key=f"select_{header}_{category}"
                )
                if selected_options:
                    all_selected_options.extend(selected_options)

        column = column_map[timeline]
        descriptive_statistics_results = {}

        for option in all_selected_options:
            try:
                result = options_descriptive_statistics_map[option](filtered_df, column)
                if result is not None:
                    descriptive_statistics_results[option] = result
            except Exception as e:
                st.warning(f"⚠️ Error computing {option}: {e}")

# -------------------------------------------------------------------------------------------------
# ☢️ Risk & Uncertainty Analysis — Sidebar Selection and Result Capture
# -------------------------------------------------------------------------------------------------
for header, (options_map, categories) in options_maps.items():
    if header == 'Risk and Uncertainty Analysis':
        all_selected_options = []
        with st.sidebar.expander(header):
            for category, options in categories.items():
                selected_options = st.multiselect(
                    f'Select options for {category}',
                    options=options,
                    key=f"select_{header}_{category}"
                )
                if selected_options:
                    all_selected_options.extend(selected_options)

        column = column_map.get(timeline, None)
        risk_uncertainty_results = {}

        for option in all_selected_options:
            try:
                if option == "Probability of Hitting DPT":
                    if timeline == 'Daily H-L':
                        st.info("Probability of hitting DPT is not available for 'Daily H-L'.")
                        continue

                    result = calculate_probability_of_dpt_advanced(
                        processed_df, column, direction, desired_profit_target, filtered_df
                    )

                    target_percentage, occurrences, count, probability, rounded_probability, \
                    probability_fraction, fraction_approx, approximate_readable = result

                    st.subheader(f"Probability of hitting DPT: {desired_profit_target}%")
                    if occurrences > 0:
                        st.markdown(f"""
                        The probability of hitting the **Desired Profit Target (DPT)** of \
                        **{desired_profit_target}%** occurred **{occurrences} out of {count} \
                        times**, or approximately **1 in {approximate_readable} trading days**, \
                        based on the selected filtering criteria.
                        """)
                    else:
                        st.markdown(f"""
                        A Desired Profit Target (DPT) of **{desired_profit_target:.0f}%** was \
                        not achieved under the current filtering conditions.
                        """)

                    # ✅ Save for snapshot
                    risk_uncertainty_results["Probability of Hitting DPT"] = {
                        "selected_dpt_pct": desired_profit_target,
                        "direction": direction,
                        "timeline": timeline,
                        "estimated_hit_ratio": f"1 in {approximate_readable}" if approximate_readable else "Unavailable",
                        "occurrences": occurrences,
                        "total_observations": count
                    }

                elif option == "Monte Carlo Simulations":
                    # Show only — skip JSON capture
                    options_risk_and_uncertainty_map[option](filtered_df, column)

                else:
                    result = options_risk_and_uncertainty_map[option](filtered_df, column)
                    if result is not None:
                        risk_uncertainty_results[option] = result

            except Exception as e:
                st.warning(f"⚠️ Error computing {option}: {e}")

# -------------------------------------------------------------------------------------------------
# 🌪️ Market Dynamics — Sidebar Selection and Result Capture
# -------------------------------------------------------------------------------------------------
for header, (options_map, categories) in options_maps.items():
    if header == 'Market Dynamics':
        all_selected_options = []
        with st.sidebar.expander(header):
            for category, options in categories.items():
                selected_options = st.multiselect(
                    f'Select options for {category}',
                    options=options,
                    key=f"select_{header}_{category}"
                )
                if selected_options:
                    all_selected_options.extend(selected_options)

        column = column_map[timeline]
        market_dynamics_results = {}

        for option in all_selected_options:
            try:
                result = options_market_dynamics_map[option](filtered_df, column)
                if result is not None:
                    market_dynamics_results[option] = result
            except Exception as e:
                st.warning(f"⚠️ Error computing {option}: {e}")

# -------------------------------------------------------------------------------------------------
#  Performance Metrics & Correlations — Sidebar Selection and Result Capture
# -------------------------------------------------------------------------------------------------
for header, (options_map, categories) in options_maps.items():
    if header == 'Performance Metrics & Correlations':  # Only process the Analysis Options
        # st.sidebar.title(header)

        all_selected_options = []
        with st.sidebar.expander(header):
            for category, options in categories.items():
                selected_options = st.multiselect(
                    f'Select options for {category}',
                    options=categories[category]
                )
                if selected_options:
                    all_selected_options.extend(selected_options)

        # Get the correct column based on timeline
        column = column_map[timeline]

        performance_analysis_results = {}  # Snapshot container for performance metrics


        # Handle each selected option
        for selected_option in all_selected_options:

            # Demo: disable correlation + volatility paths (including user uploads)
            DISABLED = {
                "Correlation with User Uploads",
                "Volatility with User Uploads",
            }

            if selected_option in correlation_mapping or selected_option in volatility_mapping or selected_option in DISABLED:
                st.info("Correlation and volatility overlays are not included in the public demo.")
                continue

            # Correlation Options
            if selected_option in correlation_mapping:
                st.subheader(f"Performing correlation for {DATA_TITLE} with {selected_option}")
                data_loader_function, correlation_df_name = correlation_mapping[selected_option]

                if timeline != 'Interday':
                    st.info("Correlation analysis can only be applied to the 'Interday' timeline.")
                else:
                    if 'return' in filtered_df.columns:
                        correlation_df, volatility_df, returns_df = data_loader_function()

                        correlation_data_df = pd.merge(
                            correlation_df,
                            filtered_df[['date', 'return']],
                            on='date',
                            how='inner'
                        )
                        correlation_data_df = correlation_data_df.rename(
                            columns={'return': f'{DATA_TITLE}'}
                        )

                        pearsons_or_spearmans_correlation(correlation_data_df,
                        filtered_df, DATA_TITLE)

                        heatmap = generate_correlation_heatmap(correlation_data_df, DATA_TITLE)
                        if heatmap:
                            st.altair_chart(heatmap)
                    else:
                        st.error("The 'return' column is missing in the filtered data.")

            # Handle User Uploads Correlation
            elif selected_option == "Correlation with User Uploads":
                st.subheader(f"Performing correlation for {DATA_TITLE} with User Uploads")

                # Handle user-uploaded data
                uploaded_files = st.sidebar.file_uploader("Upload your CSV files for correlation",
                type="csv", accept_multiple_files=True)
                if uploaded_files:
                    correlation_df_user = load_and_clean_user_correlations(uploaded_files)

                    if 'return' in filtered_df.columns:
                        correlation_df_user = pd.merge(
                            correlation_df_user,
                            filtered_df[['date', 'return']],
                            on='date',
                            how='inner'
                        )
                        correlation_df_user.rename(columns={'return': f'{DATA_TITLE}'},
                        inplace=True
                        )
                        pearsons_or_spearmans_correlation_user(correlation_df_user,
                        filtered_df, DATA_TITLE)

                        heatmap = generate_correlation_heatmap(correlation_df_user, DATA_TITLE)
                        if heatmap:
                            st.altair_chart(heatmap)
                    else:
                        st.error("The 'return' column is missing in the filtered data.")
                else:
                    st.warning("Please upload at least one file to perform correlation.")

            # Handle Volatility Options
            elif selected_option in volatility_mapping:
                st.subheader(
                f"Performing volatility analysis for {DATA_TITLE} with {selected_option}"
                )


                data_loader_function, volatility_df_name = volatility_mapping[selected_option]

                if timeline != 'Interday':
                    st.info("Volatility analysis can only be applied to the 'Interday' timeline.")
                else:
                    if 'ATR' in filtered_df.columns:
                        correlation_df, volatility_df, returns_df = data_loader_function()

                        # Merge volatility data with filtered data
                        volatility_data_df = pd.merge(
                            volatility_df,
                            filtered_df[['date', 'ATR', 'STDdev%']],
                            on='date',
                            how='inner'
                        )

                        # Prepare base asset data with proper renaming
                        base_asset = filtered_df[['date', 'ATR', 'STDdev%',
                        'Volatility Category']].copy()
                        base_asset.rename(
                            columns={
                                'ATR': f'{DATA_TITLE}_ATR%',
                                'STDdev%': f'{DATA_TITLE}_STDdev%',
                                'Volatility Category': f'{DATA_TITLE}_rating'
                            },
                            inplace=True
                        )

                        # Merge volatility data with base asset data
                        volatility_data_df = pd.merge(
                            volatility_data_df,
                            base_asset,
                            on='date',
                            how='inner'
                        )

                        # Perform volatility analysis
                        volatility_assets(volatility_data_df, filtered_df, DATA_TITLE)
                    else:
                        st.error("The 'ATR' column is missing in the filtered data.")

            # Handle User Uploads Volatility
            elif selected_option == "Volatility with User Uploads":
                st.subheader(
                f"Performing volatility analysis for {DATA_TITLE} with {selected_option}"
                )
                # Handle user-uploaded data
                uploaded_files = st.sidebar.file_uploader(
                    "Upload your CSV files for volatility analysis",
                    type="csv", accept_multiple_files=True)

                if uploaded_files:
                    volatility_user_df = load_and_clean_user_volatility(uploaded_files)

                    if 'ATR' in filtered_df.columns:

                        volatility_user_df = pd.merge(
                            volatility_user_df,
                            filtered_df[['date', 'ATR', 'STDdev%']],
                            on='date',
                            how='inner'
                        )

                        base_asset = filtered_df[[
                            'date', 'ATR', 'STDdev%', 'Volatility Category'
                        ]].copy()

                        base_asset.rename(
                            columns={
                                'ATR': f'{DATA_TITLE}_ATR%',
                                'STDdev%': f'{DATA_TITLE}_STDdev%',
                                'Volatility Category': f'{DATA_TITLE}_rating'
                            },
                            inplace=True
                        )
                        # Merge volatility data with base asset data
                        volatility_user_df = pd.merge(
                            volatility_user_df,
                            base_asset,
                            on='date',
                            how='inner'
                        )

                        # Perform volatility analysis
                        volatility_assets_user(volatility_user_df, filtered_df, DATA_TITLE)
                    else:
                        st.error("The 'ATR' column is missing in the uploaded data.")
                else:
                    st.info("Please upload at least one file to perform volatility analysis.")

            # Handle other selected options (Performance Metrics only)
            else:
                result = options_performance_and_correlation_map[selected_option](filtered_df, column)

                if selected_option == "Annualised Return" and result is not None:
                    performance_analysis_results["Annualised Return"] = {
                        "annualised_return_pct": round(result, 2)
                    }

                elif selected_option == "Maximum Drawdown" and result is not None:
                    performance_analysis_results["Maximum Drawdown"] = {
                        "max_drawdown_pct": round(result, 2)
                    }

                elif selected_option == "Volatility-Adjusted Return" and result is not None:
                    performance_analysis_results["Volatility-Adjusted Return"] = {
                        "volatility_adjusted_return_pct": round(result, 2)
                    }

                elif selected_option == "Return on Investment (ROI)" and result is not None:
                    performance_analysis_results["Return on Investment (ROI)"] = {
                        "roi_pct": round(result, 2)
                    }

                elif selected_option == "Volume vs ATR Correlation" and result is not None:
                    performance_analysis_results["Volume vs ATR Correlation"] = {
                        "correlation": round(result, 3)
                    }

# -------------------------------------------------------------------------------------------------
# Data Visualisation Filter Application
# -------------------------------------------------------------------------------------------------
for header, (options_map, categories) in options_maps.items():
    if header == 'Data Visualisation':  # Only process Data Visualisations
        all_selected_options = []
        with st.sidebar.expander(header):
            for category, options in categories.items():
                selected_options = st.multiselect(
                    f'Select options for {category}',
                    options=categories[category]
                )
                if selected_options:
                    all_selected_options.extend(selected_options)

        # Get the correct column based on timeline
        column = column_map[timeline]  # Make sure you have the column set from the column_map

        # Handle Visualisation Options for Data
        for selected_option in all_selected_options:

            # Demo: disable returns overlays & user-upload returns
            if selected_option in returns_mapping or selected_option == "Returns with User Uploads":
                st.info("Returns overlays (cross-asset and uploads) are not included in the public demo.")
                continue

            # Price Movement & Trend Visualisation (only for Range and Event-Driven)
            if selected_option in ["Price Movement - Line", "Price Movement - Candlestick",
            "Trend Visualisation - Area"]:
                if filter_type not in ["Range", "Event-Based Analysis"]:
                    st.info(f"{selected_option} is only available for Range and \
                    Event-Based Analysis.")
                    continue  # Skip for other filter types
                options_data_visualisations_map[selected_option](filtered_df, timeline)
                continue  # Proceed to next option

            # Check for Range and Events Returns or Temporal Returns
            if selected_option == "Range and Events Returns":
                # Ensure only Range or Event-Based Analysis is allowed for Range and Events Returns
                if filter_type not in ["Range", "Event-Based Analysis"]:
                    st.info("Range and Events Returns are only available for Range or \
                    Event-Based Analysis.")
                    continue  # Skip this option
                options_data_visualisations_map[selected_option](processed_df,
                timeline, filtered_df)
                continue  # Proceed to next option after handling Range and Events Returns

            if selected_option == "Temporal Returns":
                # Ensure Temporal Patterns filter is selected for Temporal Returns
                if filter_type != "Temporal Patterns":
                    st.info("Temporal Returns are only available for Temporal Patterns.")
                    continue  # Skip this option
                if 'selected_pattern' not in locals() or selected_pattern is None:
                    st.info("Please select a Temporal Pattern (Week, Month etc.) to proceed.")
                    continue  # Skip if no selected pattern
                options_data_visualisations_map[selected_option](filtered_df, timeline,
                selected_pattern)
                continue  # Proceed to next option after handling Temporal Returns

            # For other return-related options, follow the same structure
            if selected_option in returns_mapping:
                st.subheader(f"Returns analysis for {DATA_TITLE} with {selected_option}")
                data_loader_function, returns_df_name = returns_mapping[selected_option]

                # Ensure the timeline is 'Interday'
                if timeline != 'Interday':
                    st.info("Returns analysis can only be applied to the 'Interday' timeline.")
                else:
                    if 'return' in filtered_df.columns:
                        # Dynamically load the data for the selected option
                        correlation_df, volatility_df, returns_df = data_loader_function()

                        # Ensure 'date' and 'return' are in the merged data
                        if 'date' in filtered_df.columns and 'return' in filtered_df.columns:
                            # Merge the data as needed for the selected returns option
                            returns_data_df = pd.merge(returns_df, filtered_df[['date',
                            'return']], on='date', how='inner')
                            base_asset = filtered_df[['date', 'return']].copy()
                            base_asset.rename(columns={'return': f'{DATA_TITLE}_return'},
                            inplace=True)

                            # Merge the base asset data with the selected asset data
                            returns_data_df = pd.merge(returns_data_df, base_asset, on='date',
                            how='inner')

                            # Pass a clean version of the asset name to the visualisation
                            clean_asset_name = DATA_TITLE  # Clean without '_return'

                            # Show the data and visualisation
                            # st.dataframe(returns_data_df)
                            returns_visualisation(returns_data_df, f'{DATA_TITLE}_return',
                            clean_asset_name)  # Pass clean asset name here
                        else:
                            st.error("The 'date' or 'return' column is missing in the \
                            filtered data.")

                    else:
                        st.error("The 'return' column is missing in the filtered data.")
                continue  # Proceed to next option after handling user uploads

            # Handle User Uploads Return (only for Interday timeline)
            if selected_option == "Returns with User Uploads":
                if timeline != 'Interday':
                    st.info("User Uploads Return Correlation can only be applied to \
                    the 'Interday' timeline.")
                    continue  # Skip if timeline is not Interday

                uploaded_files = st.sidebar.file_uploader("Upload your CSV files for returns",
                type="csv", accept_multiple_files=True)
                if uploaded_files:
                    try:
                        # Process the uploaded files using your data processing function
                        correlation_user_returns_df = load_and_prepare_user_returns(uploaded_files)
                        base_asset = filtered_df[['date', 'return']].copy()
                        base_asset.rename(columns={'return': f'{DATA_TITLE}_return'}, inplace=True)

                        # Merge the user-uploaded returns with the filtered data
                        correlation_user_returns_df = pd.merge(correlation_user_returns_df,
                        base_asset, on='date', how='inner')

                        # Validate and visualize
                        if f'{DATA_TITLE}_return' in correlation_user_returns_df.columns:
                            user_returns(correlation_user_returns_df, f'{DATA_TITLE}_return')
                        else:
                            uploaded_file_name = uploaded_files[0].name.split(".")[0]
                            if uploaded_file_name.lower() == DATA_TITLE.lower():
                                st.warning("The 'return' column is missing in the \
                                merged data, or you are uploading a file with the \
                                same name as the base asset.")
                            else:
                                st.error("The 'return' column is missing in the merged data.")
                    except (ValueError, KeyError, TypeError) as e:
                        st.error(f"An error occurred while processing the user-uploaded data: {e}")
                else:
                    st.info("Please upload at least one CSV file to proceed with the \
                    returns analysis.")

                continue  # Proceed after handling user uploads

            # Handle Returns for Cumulative and Rolling Returns
            if selected_option == "Cumulative Returns":
                try:
                    # Ensure that the 'return' column is present
                    if 'return' in filtered_df.columns:
                        cumulative_returns(processed_df, timeline, filtered_df)
                    else:
                        st.error("The 'return' column is missing in the filtered data.")
                except (ValueError, KeyError) as e:
                    st.error(f"An error occurred while processing Cumulative Returns: {e}")
                continue

            if selected_option == "Rolling Returns":
                try:
                    # Ensure that the 'return' column is present
                    if 'return' in filtered_df.columns:
                        rolling_returns(processed_df, timeline, filtered_df)
                    else:
                        st.error("The 'return' column is missing in the filtered data.")
                except (ValueError, KeyError) as e:
                    st.error(f"An error occurred while processing Rolling Returns: {e}")
                continue

            # Handle Risk-Return Analysis
            if selected_option == "Risk-Return":
                try:
                    # Ensure that the required columns for risk-return analysis are present
                    if 'return' in filtered_df.columns:
                        risk_return_scatter_plot(processed_df, timeline, filtered_df)
                    else:
                        st.error("The 'return' or 'risk' column is missing in the filtered data.")
                except (ValueError, KeyError) as e:
                    st.error(f"An error occurred while processing Risk-Return analysis: {e}")
                continue

            # Handle DPT vs Volatility Scatter Plot for Range/Event-Based Analysis
            if selected_option == "DPT vs Volatility":
                if timeline != 'Interday':
                    st.info("Volatility vs DPT Achievement can only be applied to \
                    the 'Interday' timeline.")
                    continue  # Skip processing if timeline is not 'Interday'

                try:
                    # Call the function for scatterplot visualisation
                    scatter_fig = scatterplot_dpt_vs_volatility(filtered_df, direction,
                    desired_profit_target, period='1d', temporal_filter=None)
                    st.plotly_chart(scatter_fig, theme="streamlit",
                    key=f"{selected_option}_1d_{direction}_{desired_profit_target}")
                except (ValueError, KeyError) as e:
                    st.error(f"An error occurred while generating the DPT vs Volatility \
                    scatter plot: {e}")
                continue  # Proceed to the next selected option after processing

st.divider()

# -------------------------------------------------------------------------------------------------
# 🧠 Define Theme Metadata (for Observation Logging)
# -------------------------------------------------------------------------------------------------
# theme_code = "market_scanner"
# theme_title = "Market & Volatility Scanner"

# -------------------------------------------------------------------------------------------------
# 🎯 Asset Snapshot Insight
# -------------------------------------------------------------------------------------------------
asset_snapshot_insight = {
    "snapshot_metadata": {
        "base_asset": DATA_TITLE,
        "theme": {
            "code": "market_scanner",
            "title": "Market & Volatility Scanner"
        },
        "snapshot_timestamp": datetime.now(UTC).isoformat(),
        "asset_type": asset_type_display
    },
    "analysis_summary": {
        "analysed_period": {
            "start_date": str(start_date),
            "end_date": str(end_date)
        },
        "metrics": {
            "last_price": round(last_price, 2),
            "days_since_bear_market": days_since_bear_market,
            "current_drawdown_pct": round(current_drawdown, 2),
            "max_price": {
                "value": round(max_price, 2),
                "date": max_price_date.strftime('%Y-%m-%d')
            },
            "min_price": {
                "value": round(min_price, 2),
                "date": min_price_date.strftime('%Y-%m-%d')
            },
            "high_price": {
                "value": round(high_price, 2),
                "date": high_price_date.strftime('%Y-%m-%d')
            },
            "low_price": {
                "value": round(low_price, 2),
                "date": low_price_date.strftime('%Y-%m-%d')
            }
        },
        "volatility": {
            "standard_deviation_pct": std_dev if 'std_dev' in locals() else None,
            "mean_high_to_low_pct": mean_high_to_low_range if 'mean_high_to_low_range' in locals() else None
        },
        "atr": {
            "daily": {"pct": daily_atr_pct, "abs": daily_atr_abs},
            "weekly": {"pct": weekly_atr_pct, "abs": weekly_atr_abs},
            "monthly": {"pct": monthly_atr_pct, "abs": monthly_atr_abs}
        },
        "returns": {
            "daily_return_pct": daily_return,
            "weekly_return_pct": weekly_return,
            "monthly_return_pct": monthly_return
        },
        "dpt_probability": {
            "selected_dpt_pct": desired_profit_target,
            "direction": direction,
            "timeline": timeline,
            "estimated_hit_ratio": f"1 in {approx}" if 'approx' in locals() and approx is not None else "Unavailable",
            "occurrences": int(occurrences) if 'occurrences' in locals() and occurrences is not None else None,
            "total_observations": int(count) if 'count' in locals() and count is not None else None
        }

    },
    "statistical_analysis": {
        "context_parameters": {
            "selected_profit_target_pct": desired_profit_target,
            "direction": direction,
            "timeline": timeline,
            "filter_type": filter_type,
            "filter_description": filter_applied_description
        },
        "descriptive_statistics": descriptive_statistics_results if "descriptive_statistics_results" in locals() else None,
        "risk_and_uncertainty_analysis": risk_uncertainty_results if "risk_uncertainty_results" in locals() else None,
        "market_dynamics": market_dynamics_results if "market_dynamics_results" in locals() else None,
        "performance_metrics": performance_analysis_results if "performance_analysis_results" in locals() else None
    },
    "metadata": {
        "data_source": data_source,
        "snapshot_notes": "Generated from Market & Volatility Scanner statistical analysis."
    }
}

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

# -------------------------------------------------------------------------------------------------
# Sidebar options using multiselect
# -------------------------------------------------------------------------------------------------
st.sidebar.header("Data Inspection")
sidebar_data_options = st.sidebar.multiselect(
    'Choose data view',
    ['Processed Data', 'Filtered Data']
)

# Display Data Inspection Views
if 'Processed Data' in sidebar_data_options:
    st.write(
        "You are viewing the processed data with necessary fixes (e.g., missing values, "
        "column renaming). This is the data ready for analysis."
    )
    st.dataframe(processed_df)  # Show processed data

if 'Filtered Data' in sidebar_data_options:
    st.write(
        "This is the filtered data based on the selected date range and any temporal patterns \
        or event-based analysis filters."
    )
    st.dataframe(filtered_df)  # Show filtered data
