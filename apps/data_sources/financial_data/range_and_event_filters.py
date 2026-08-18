# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name
# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Range and Event Filters — Date Filtering for Financial Time Series

This module defines date and event-based filters used in Streamlit sidebar workflows.
It supports both basic date range selection and event-centric filtering across pre/post windows.

Functions:
- `apply_date_range_filter_ui`: Sidebar range selector for date boundaries
- `apply_date_range_filter_ui_custom`: Supports multiple simultaneous asset panels
(e.g., long/short)
- `apply_event_filter_ui`: Sidebar setup for single-point event filtering with pre/post windows
- `apply_event_filter`: Core logic for filtering based on proximity to a selected date
- `apply_date_range_filter`: Core logic for bounding a dataset by min/max date

These functions are UI-aware (Streamlit) and depend on a `date` column within the DataFrame.
They are compatible with both default and user-uploaded datasets.

Located at: `/apps/data_sources/financial_data/range_and_event_filters.py`
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Date Range Filter — UI and Core Logic
# -------------------------------------------------------------------------------------------------
def apply_date_range_filter_ui(df):
    """
    UI for Date Range Filter. Filters dataframe based on user-selected date range.
    """
    with st.sidebar.expander("Date Filter for Analysis"):
        start_date = st.date_input("Select Start Date", value=df["date"].min())
        end_date = st.date_input("Select End Date", value=df["date"].max())

        if start_date and end_date:
            df = apply_date_range_filter(df, start_date, end_date)
            st.write(f"Date range being reviewed: {start_date} to {end_date}")
        else:
            st.write("No date filter applied, reviewing all available data.")

    return df

def apply_date_range_filter(df, start_date, end_date):
    """
    Filters the dataframe based on a user-selected date range.
    """
    return df[
        (df["date"] >= pd.to_datetime(start_date)) &
        (df["date"] <= pd.to_datetime(end_date))
    ]

# -------------------------------------------------------------------------------------------------
# Event Filter — UI and Core Logic
# -------------------------------------------------------------------------------------------------
def apply_event_filter_ui(df):
    """
    UI for Event-Based Analysis Filter. Filters dataframe based on a selected event date.
    """
    st.sidebar.subheader("Event-Based Analysis")

    event_date = st.sidebar.date_input("Select Event Date", value=df["date"].min())

    pre_event_days = st.sidebar.slider(
        "Select Pre-event Window (days)", min_value=1, max_value=30, value=5, step=1
    )
    post_event_days = st.sidebar.slider(
        "Select Post-event Window (days)", min_value=1, max_value=30, value=5, step=1
    )

    st.write(f"Selected Event Date: {event_date}")
    st.write(f"Pre-event Window: {pre_event_days} days")
    st.write(f"Post-event Window: {post_event_days} days")

    return apply_event_filter(df, event_date, pre_event_days, post_event_days)

def apply_event_filter(df, event_date, pre_event_days, post_event_days):
    """
    Filters the dataframe based on an event window (pre/post days).
    """
    event_date = pd.to_datetime(event_date)
    pre_start = event_date - pd.Timedelta(days=pre_event_days)
    post_end = event_date + pd.Timedelta(days=post_event_days)

    df = df[(df["date"] >= pre_start) & (df["date"] <= post_end)]

    if df.empty:
        st.write("No data available for the selected event date window.")
    else:
        st.write(f"Filtering Data from {pre_start} to {post_end}")

    return df

# -------------------------------------------------------------------------------------------------
# Custom Date Range Filter — Multi-Asset Panels
# -------------------------------------------------------------------------------------------------
def apply_date_range_filter_ui_custom(df, asset_label):
    """
    Custom UI for Date Range Filter with distinct keys for long/short assets.
    """
    with st.sidebar.expander(f"Date Filter for {asset_label}"):
        start_date = st.date_input(
            f"Select Start Date for {asset_label}",
            value=df["date"].min(),
            key=f"start_date_{asset_label}"
        )
        end_date = st.date_input(
            f"Select End Date for {asset_label}",
            value=df["date"].max(),
            key=f"end_date_{asset_label}"
        )

        if start_date and end_date:
            df = apply_date_range_filter(df, start_date, end_date)
            st.write(f"Date range for {asset_label}: {start_date} to {end_date}")
        else:
            st.write(f"No date filter applied for {asset_label}, reviewing all available data.")

    return df
