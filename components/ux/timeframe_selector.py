# -------------------------------------------------------------------------------------------------
# ⏳ Timeframe Selector (Platinum Canonical — Period-Based Labeling)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error

# -------------------------------------------------------------------------------------------------
# 📘 Docstring
# -------------------------------------------------------------------------------------------------
"""
📊 Timeframe Selector UI Component — Economic Exploration Suite
---------------------------------------------------------------

✅ System Role:
- Provides standardised sidebar interface for timeframe selection across all
  Economic Exploration thematic modules.

✅ Period-Based Governance:
- Timeframes are row-based, frequency-neutral selections (not calendar dependent).
- Supports datasets across quarterly, monthly, weekly or mixed-period inputs.
- Downstream signal processing functions receive correctly pre-sliced datasets.

✅ Returned Payload:
- `selected`: internal timeframe key used by downstream slicer functions.
- `label`: user-readable string for annotation, AI persona reference, or export metadata.

---------------------------------------------------------------
🔐 Canonical Platinum Rule — System Locked:
- This module governs uniform user interface behavior across all themes.
- Never embed frequency assumptions into downstream logic — slicing remains fully decoupled.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st

# -------------------------------------------------------------------------------------------------
# Timeframe Selector Core Logic
# -------------------------------------------------------------------------------------------------
def render_timeframe_selector() -> tuple[str, str]:
    """
    Sidebar timeframe selector for Economic Exploration modules.

    Returns:
        tuple: (selected timeframe key, readable label)
    """

    TIMEFRAME_OPTIONS = {
        "Latest": "Latest Period Only",
        "3P": "Last 3 Periods",
        "6P": "Last 6 Periods",
        "12P": "Last 12 Periods",
        "All": "Full History"
    }

    st.sidebar.title("🕒 Select Timeframe for Analysis")
    selected = st.sidebar.selectbox(
        "Timeframe",
        options=list(TIMEFRAME_OPTIONS.keys()),
        format_func=lambda x: f"{x} – {TIMEFRAME_OPTIONS[x]}"
    )
    label = TIMEFRAME_OPTIONS[selected]
    st.sidebar.caption(f"🔍 Analyzing: **{label}**")

    with st.sidebar.expander("🧭 Timeframe Guidance"):
        st.markdown("""
- **📉 Latest**: Focuses on the most recent available observation period.
- **3P / 6P / 12P**: Captures short to medium term dynamics based on the data frequency
  of the selected dataset (monthly, quarterly, or weekly).
- **📈 All**: Full available history for structural pattern analysis.

_Note: Actual period length depends on the underlying dataset frequency
(monthly, quarterly, or weekly)._

These options guide the **macro signal summary** calculations.
For detailed historical exploration, see the **chart tabs**.
        """)

    return selected, label
