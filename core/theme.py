# core/theme.py

import streamlit as st

def inject_global_styles() -> None:
    """
    Injects CRT-wide styling:
    - Nunito font
    - Core typography baseline
    """
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap');

          html, body, [class*="css"]  {
            font-family: 'Nunito', system-ui, -apple-system, BlinkMacSystemFont,
                         'Segoe UI', sans-serif !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
