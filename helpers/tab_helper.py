# -------------------------------------------------------------------------------------------------
# 📁 Tab Helper — Timeframe Slicing Based on Frequency
# -------------------------------------------------------------------------------------------------
# Location: /apps/helpers/tab_helper.py
# -------------------------------------------------------------------------------------------------
"""
Provides reusable logic for generating Streamlit tab labels and associated time-sliced data views.
Supports different time frequencies (weekly, monthly, quarterly) used across economic modules.
"""

import streamlit as st
import pandas as pd


def get_tab_labels_and_data(df: pd.DataFrame, frequency: str = "quarterly") -> tuple[list[str], dict]:
    """
    Returns tab labels and associated sliced DataFrames based on frequency.

    Args:
        df (pd.DataFrame): The base dataframe (cleaned and indexed by date).
        frequency (str): One of 'weekly', 'monthly', or 'quarterly'.

    Returns:
        tuple:
            - list[str]: Streamlit tab labels.
            - dict: Mapping of tab to sliced DataFrame.
    """
    if df is None or df.empty:
        return [], {}

    # Define slicing windows per frequency
    freq_settings = {
        "weekly": {
            "Recent Weeks": 4,
            "1 Month": 5,
            "3 Months": 13,
            "6 Months": 26,
            "1 Year": 52,
            "Full History": None
        },
        "monthly": {
            "Recent Months": 3,
            "1 Year": 12,
            "2 Years": 24,
            "3 Years": 36,
            "5 Years": 60,
            "Full History": None
        },
        "quarterly": {
            "📉 Recent Quarters": 4,
            "📊 One Year": 8,
            "📈 3-Year View": 12,
            "🕰️ 5-Year View": 20,
            "🧭 10-Year View": 40,
            "🗂️ Full History": None
        }
    }

    settings = freq_settings.get(frequency.lower(), freq_settings["quarterly"])
    labels = list(settings.keys())

    tab_mapping = {}
    for label, window in settings.items():
        if window is None:
            tab_mapping[label] = df
        else:
            tab_mapping[label] = df.tail(window)

    return labels, tab_mapping
