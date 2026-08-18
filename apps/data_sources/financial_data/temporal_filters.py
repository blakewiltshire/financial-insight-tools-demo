# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Temporal Filters — Streamlit UI + Logic for Time-Based Data Narrowing

This module provides functions for applying temporal filters to a DataFrame
via the Streamlit sidebar. It supports:

- Weekday filtering (Monday to Friday)
- Month filtering (Jan to Dec)
- Seasonal filtering (Winter to Autumn)
- Business Quarter filtering (Q1 to Q4)
- ISO Week filtering (1 to 52)

Each filter is presented through an interactive Streamlit UI and applies logic
based on a required `date` column in the DataFrame.

Usage Context:
- Used by: `filtering_options.py`
- Supports apps using `resample_data` or any time series decomposition

All filters return a filtered DataFrame suitable for plotting or metric extraction.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Mapping Dictionaries
# -------------------------------------------------------------------------------------------------
WEEKDAY_MAP = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2,
    "Thursday": 3, "Friday": 4
}

MONTHS_MAP = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12
}

SEASON_MAP = {
    "Winter": [12, 1, 2], "Spring": [3, 4, 5], "Summer": [6, 7, 8], "Autumn": [9, 10, 11]
}

# -------------------------------------------------------------------------------------------------
# Weekday Filter
# -------------------------------------------------------------------------------------------------
def apply_weekday_filter_ui(df):
    """
    UI for Weekday Filter. Filters dataframe based on selected weekdays.
    """
    weekdays_choices = st.sidebar.multiselect("Select Weekdays", list(WEEKDAY_MAP.keys()))
    if not weekdays_choices:
        st.sidebar.warning("Please select at least one weekday.")
        weekdays_choices = ["Monday"]
    return apply_weekday_filter(df, weekdays_choices)

def apply_weekday_filter(df, weekdays_choices):
    """Filters the dataframe by selected weekdays."""
    selected_weekdays = [WEEKDAY_MAP[day] for day in weekdays_choices]
    df["Weekday"] = df["date"].dt.weekday
    return df[df["Weekday"].isin(selected_weekdays)]

# -------------------------------------------------------------------------------------------------
# Month Filter
# -------------------------------------------------------------------------------------------------
def apply_month_filter_ui(df):
    """
    UI for Month Filter. Filters dataframe based on selected months.
    """
    months_choices = st.sidebar.multiselect("Select Months", list(MONTHS_MAP.keys()))
    if not months_choices:
        st.sidebar.warning("Please select at least one month.")
        months_choices = ["January"]
    return apply_month_filter(df, months_choices)

def apply_month_filter(df, months_choices):
    """Filters the dataframe by selected months."""
    selected_months = [MONTHS_MAP[month] for month in months_choices]
    df["Month"] = df["date"].dt.month
    return df[df["Month"].isin(selected_months)]

# -------------------------------------------------------------------------------------------------
# Season Filter
# -------------------------------------------------------------------------------------------------
def apply_season_filter_ui(df):
    """
    UI for Season Filter. Filters dataframe based on selected seasons.
    """
    seasons_choices = st.sidebar.multiselect("Select Seasons", list(SEASON_MAP.keys()))
    if not seasons_choices:
        st.sidebar.warning("Please select at least one season.")
        seasons_choices = ["Winter"]
    return apply_season_filter(df, seasons_choices)

def apply_season_filter(df, seasons_choices):
    """Filters the dataframe by selected seasons."""
    selected_months = []
    for season in seasons_choices:
        selected_months.extend(SEASON_MAP[season])
    df["Season"] = df["date"].apply(
        lambda x: "Winter" if x.month in [12, 1, 2] else
                  "Spring" if x.month in [3, 4, 5] else
                  "Summer" if x.month in [6, 7, 8] else "Autumn"
    )
    return df[df["Season"].isin(seasons_choices)]

# -------------------------------------------------------------------------------------------------
# Quarter Filter
# -------------------------------------------------------------------------------------------------
def apply_quarter_filter_ui(df):
    """
    UI for Quarter Filter. Filters dataframe based on selected quarters.
    """
    quarters_choices = st.sidebar.multiselect("Select Business Quarters", ["Q1", "Q2", "Q3", "Q4"])
    if not quarters_choices:
        st.sidebar.warning("Please select at least one quarter.")
        quarters_choices = ["Q1"]
    return apply_quarter_filter(df, quarters_choices)

def apply_quarter_filter(df, quarters_choices):
    """Filters the dataframe by selected quarters."""
    df["Quarter"] = df["date"].apply(
        lambda x: "Q1" if x.month in [1, 2, 3] else
                  "Q2" if x.month in [4, 5, 6] else
                  "Q3" if x.month in [7, 8, 9] else "Q4"
    )
    return df[df["Quarter"].isin(quarters_choices)]

# -------------------------------------------------------------------------------------------------
# Week Filter (ISO Calendar)
# -------------------------------------------------------------------------------------------------
def apply_week_filter_ui(df):
    """
    UI for Week Filter. Filters dataframe based on selected weeks.
    """
    weeks_choices = st.sidebar.multiselect("Select Weeks", list(range(1, 53)))
    if not weeks_choices:
        st.sidebar.warning("Please select at least one week.")
        weeks_choices = [1]
    return apply_week_filter(df, weeks_choices)

def apply_week_filter(df, weeks_choices):
    """Filters the dataframe by selected weeks."""
    df["Week"] = df["date"].dt.isocalendar().week
    df = df[df["Week"] != 53]
    return df[df["Week"].isin(weeks_choices)]
