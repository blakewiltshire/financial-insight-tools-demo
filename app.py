"""
Financial Insight Tools Preview (FIT)

This is a focused public preview of the Financial Insight Tools environment.
It provides a contained view of the Trade & Portfolio Structuring workflow using
a small set of preloaded assets and structured preview records, using the same structural scaffolding as the full suite.

No trading, investment, or policy advice is provided.
"""

from __future__ import annotations

import os
from typing import Dict

import streamlit as st

from core.helpers import (  # pylint: disable=import-error
    load_markdown_file,
    get_named_paths,
)

from core.theme import inject_global_styles

inject_global_styles()


def _get_paths(current_file: str) -> Dict[str, str]:
    """
    Resolve key filesystem paths relative to the current file.

    Parameters
    ----------
    current_file : str
        Typically passed as __file__ from this module.

    Returns
    -------
    dict
        A dictionary containing important root-relative paths used for
        loading brand assets and documentation.
    """
    paths = get_named_paths(current_file)
    root_path = paths["level_up_0"]

    return {
        "root": root_path,
        "brand_logo": os.path.join(root_path, "brand", "blake_logo.png"),
        "sidebar_image": os.path.join(root_path, "images", "fit.png"),
        "about_support_md": os.path.join(root_path, "docs", "about_and_support.md"),
    }


# -------------------------------------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------------------------------------
def _render_sidebar(paths: Dict[str, str]) -> None:
    """
    Render a structured sidebar navigation using Streamlit's modern
    st.sidebar.page_link() API.
    """
    brand_logo = paths["brand_logo"]
    sidebar_image = paths["sidebar_image"]
    about_support_md = paths["about_support_md"]

    if os.path.isfile(brand_logo):
        st.logo(brand_logo)

    if os.path.isfile(sidebar_image):
        st.sidebar.image(sidebar_image, width="stretch")

    st.sidebar.title("Modules")
    st.sidebar.caption(
        "A focused Trade & Portfolio Structuring environment from the broader FIT suite."
    )

    st.sidebar.page_link(
        "pages/01_market_and_volatility_scanner.py",
        label="Market & Volatility Scanner"
    )

    st.sidebar.page_link(
        "pages/02_trade_timing_and_confirmation.py",
        label="Trade Timing & Confirmation"
    )

    st.sidebar.page_link(
        "pages/03_price_action_and_trend_confirmation.py",
        label="Price Action & Trend Confirmation"
    )

    st.sidebar.divider()

    with st.sidebar.expander("ℹ️ About & Support"):
        support_md = load_markdown_file(about_support_md)
        if support_md:
            st.markdown(support_md, unsafe_allow_html=True)
        else:
            st.warning("Support information not available.")


# -------------------------------------------------------------------------------------------------
# Main content helpers
# -------------------------------------------------------------------------------------------------
def _render_intro_block() -> None:
    """
    Intro / orientation.
    """
    st.write(
        """
A focused public Trade & Portfolio Structuring environment from the broader Financial Insight Tools (FIT) suite.

Three connected modules demonstrate how market behaviour, trade timing, and price structure can be examined as part of a structured investigation built upon consistent analytical frameworks.

The broader FIT environment extends those investigations through macroeconomic exploration, relationship analysis, company structure, market structure, observation preservation, and AI-assisted investigation.

No brokerage integration, automated execution, or investment recommendations are provided.
        """
    )


def _render_capabilities_block() -> None:
    """
    What the preview brings into view.
    """
    st.markdown("### The Investigation in View")
    st.write(
        """
The modules are designed to be used together as a structured sequence:

- **Market & Volatility Scanner**
  Establish statistical context through return distributions, volatility structure, and market behaviour.

- **Trade Timing & Confirmation**
  Assess whether market conditions support or challenge a potential trade idea.

- **Price Action & Trend Confirmation**
  Examine directional behaviour, momentum, and trend structure within the broader investigation.

Together these modules demonstrate one way a structured investigation can develop, encouraging market behaviour,
trade timing, and price structure to be examined collectively rather than as isolated technical observations.
        """
    )


def _render_scope_block() -> None:
    """
    Scope and limits.
    """
    st.markdown("### What This Environment Includes")
    st.write(
        """
- Three Trade & Portfolio Structuring modules
- A curated dataset for structured investigation
- A focused investigation environment representative of the broader FIT platform

This environment is intentionally focused to provide a clear introduction to the Trade & Portfolio Structuring
workflow while preserving the same investigation principles used throughout Financial Insight Tools.
        """
    )


def _render_structure_block() -> None:
    """
    The Broader Environment.
    """
    st.markdown("### The Broader Environment")
    st.write(
        """
The full **Financial Insight Tools (FIT)** suite extends beyond this focused environment into a broader
decision-support environment built around connected investigation environments.

Economic Exploration

↓

Intermarket & Correlation

↓

Trade & Portfolio Structuring

↓

Reference & Investigation Resources

↓

Observation & AI Export

FIT aligns with the **Navigating the World of Economics, Finance, and Markets** guide series — a
structured examination of economics and finance as interconnected systems shaped by institutions,
incentives, coordination mechanisms, and technological change.

Further reading:

• **Why We Built Financial Insight Tools (FIT)**
https://blakewiltshire.substack.com/p/financial-insight-tools-fit

• **Blake Wiltshire**
https://blakewiltshire.com
        """
    )


def _render_footer() -> None:
    """
    Render the standard footer caption for the FIT portal.
    """
    st.divider()
    st.caption(
        "© 2026 Blake Media Ltd. | Financial Insight Tools by Blake Wiltshire — No trading, "
        "investment, or policy advice provided."
    )


# -------------------------------------------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------------------------------------------
def main() -> None:
    """
    Entrypoint for the FIT public preview Streamlit home page.

    This function configures the Streamlit page, resolves filesystem paths,
    and renders the main layout components.
    """
    st.set_page_config(
        page_title="Financial Insight Tools",
        layout="wide",
    )

    paths = _get_paths(__file__)

    _render_sidebar(paths)

    st.title("Financial Insight Tools")
    st.caption(
        "*A focused Trade & Portfolio Structuring investigation environment from the broader FIT suite.*"
    )

    st.space()
    _render_intro_block()
    st.divider()
    _render_capabilities_block()
    st.divider()
    _render_scope_block()
    st.divider()
    _render_structure_block()
    _render_footer()


if __name__ == "__main__":
    main()
