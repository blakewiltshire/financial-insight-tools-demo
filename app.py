"""
Financial Insight Tools Demo (FIT-Demo)

This is a lightweight public demo build of the Financial Insight Tools environment.
It provides a focused subset of the Trade & Portfolio Structuring workflow using a
small set of preloaded assets (Mag 7) and the same structural scaffolding as the
full suite.

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
        # Sidebar image (e.g., grouping / overview visual)
        "sidebar_image": os.path.join(root_path, "images", "fit.png"),
        # About & Support
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

    # Branding
    if os.path.isfile(brand_logo):
        st.logo(brand_logo)

    # Optional sidebar image
    if os.path.isfile(sidebar_image):
        st.sidebar.image(sidebar_image, width="stretch")

    # ---------------------------
    # Demo Navigation
    # ---------------------------
    st.sidebar.title("Demo Modules")
    st.sidebar.caption(
        "A focused subset of the Trade & Portfolio Structuring workflow."
    )

    st.sidebar.page_link(
        "pages/01_market_and_volatility_scanner.py",
        label="Market & Volatility Scanner",
        icon="🔎",
    )

    st.sidebar.page_link(
        "pages/02_trade_timing_and_confirmation.py",
        label="Trade Timing & Confirmation",
        icon="⏳",
    )

    st.sidebar.page_link(
        "pages/03_price_action_and_trend_confirmation.py",
        label="Price Action & Trend Confirmation",
        icon="📊",
    )

    st.sidebar.divider()

    # --- About & Support ---
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
This Streamlit instance is a lightweight public demonstration of **Financial Insight Tools (FIT)** —
a modular research environment for exploring market structure through consistent analytical scaffolding.

The demo centres on a focused workflow: **Trade & Portfolio Structuring**.
Three integrated modules are available in the sidebar, supported by a curated asset set (Mag 7)
to ensure fast, stable performance in Streamlit Cloud.

**No brokerage integration, no automated execution, and no investment recommendations are provided.**
        """
    )

def _render_capabilities_block() -> None:
    """
    What the demo brings into view.
    """
    st.markdown("### The Workflow in View")
    st.write(
        """
The modules are designed to be used together as a structured sequence:

- **🔎 Market & Volatility Scanner**
  Surface distribution structure, dispersion patterns, and volatility context.

- **⏳ Trade Timing & Confirmation**
  Assess timing alignment across timeframes and technical confirmation layers.

- **📊 Price Action & Trend Confirmation**
  Reinforce directional logic through structured price action and momentum framing.

Outputs are exploratory and interpretive.
The purpose is structured reasoning — not signal generation.
        """
    )

def _render_scope_block() -> None:
    """
    Scope and limits.
    """
    st.markdown("### What This Demo Includes")
    st.write(
        """
- Three Trade & Portfolio Structuring modules
- A small preloaded dataset (Magnificent 7)
- A streamlined interface representative of the broader environment
        """
    )

def _render_structure_block() -> None:
    """
    The Broader Environment.
    """
    st.markdown("### The Broader Environment")
    st.write(
        """
The full **Financial Insight Tools** suite extends beyond this demo into:

- Macroeconomic exploration and country indicator systems
- Cross-asset and thematic correlation mapping
- Portfolio monitoring and structured trade review
- Supporting calculators and risk diagnostics
- Observation capture and AI-ready export workflows

FIT aligns with the **Navigating the World of Economics, Finance, and Markets** guide series — a structured
examination of economics and finance as interconnected systems shaped by institutions, incentives,
coordination mechanisms, and technological change.

Further context:
**www.blakewiltshire.com**
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
    Entrypoint for the FIT Demo Streamlit home page.

    This function configures the Streamlit page, resolves filesystem paths,
    and renders the main layout components.
    """
    st.set_page_config(
        page_title="Financial Insight Tools Demo (FIT-Demo)",
        layout="wide",
    )

    paths = _get_paths(__file__)

    # Sidebar content
    _render_sidebar(paths)

    # Header
    st.title("Financial Insight Tools Demo")
    st.caption(
        "*A focused Trade & Portfolio Structuring workflow using a small preloaded dataset.*"
    )

    st.divider()
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
