# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Filtering Options Map (Refactored)

Central dispatch map for all interactive data filtering UI options used in
Streamlit-based financial data applications.

This module defines and exposes filtering logic by category:
- Range Filters (e.g., start and end dates)
- Temporal Filters (e.g., weekdays, months, quarters)
- Event-Based Filters (e.g., pre/post event analysis)

Location:
/apps/data_sources/financial_data/

Dependencies:
- range_and_event_filters.py
- temporal_filters.py

Used by:
- trade_portfolio_structuring apps
- market and volatility scanner

Standard Import:
    from data_sources.financial_data.filtering_options import filtering_options_map

"""

# -------------------------------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------------------------------
from .range_and_event_filters import (
    apply_date_range_filter_ui, apply_date_range_filter_ui_custom, apply_event_filter_ui,
)

from .temporal_filters import (
    apply_weekday_filter_ui, apply_month_filter_ui, apply_season_filter_ui,
    apply_quarter_filter_ui, apply_week_filter_ui
)

# -------------------------------------------------------------------------------------------------
# Filter Option Mapping
# -------------------------------------------------------------------------------------------------
filtering_options_map = {
    "Range": apply_date_range_filter_ui,
    "Temporal Patterns": {
        "Weekday": apply_weekday_filter_ui,
        "Month": apply_month_filter_ui,
        "Season": apply_season_filter_ui,
        "Business Quarter": apply_quarter_filter_ui,
        "Week": apply_week_filter_ui,
    },
    "Event-Based Analysis": apply_event_filter_ui
}

# -------------------------------------------------------------------------------------------------
# Optional Customisation Layer (For Multi-Asset Views)
# -------------------------------------------------------------------------------------------------
custom_filtering_options_map = {
    "Range": apply_date_range_filter_ui_custom,
}
