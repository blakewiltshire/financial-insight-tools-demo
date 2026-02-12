# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
#
# Add any global disables if required (e.g., unused-import)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
use_case_helpers.py

Shared helper functions for managing predefined use cases and indicator auto-selection
in Streamlit-based analytical modules.

This file supports:
- Structured sidebar help text for use case selectors
- Auto-indicator population logic by selected template
- Consistent UX and code reuse across all Financial Insight Tools apps

Modules using this helper include:
- Price Action & Trend Confirmation

"""

# -------------------------------------------------------------------------------------------------
# Function: generate_use_case_help_text
# Purpose: Generates structured markdown help text for Streamlit use case dropdown
# Use Case: Sidebar tooltips in trading, macro, and confirmation modules
# -------------------------------------------------------------------------------------------------
def generate_use_case_help_text(use_cases: dict, default_label: str = "Naked Charts") -> str:
    """
    Generate a structured help text string for Streamlit sidebar use case selection.

    Parameters:
        use_cases (dict): Dictionary of use cases (label → metadata including Description).
        default_label (str): Default label (e.g., 'Naked Charts') that bypasses auto-selection.

    Returns:
        str: Multi-line help text string for display in Streamlit.
    """
    help_text = (
        f"**Select a predefined analytical template to auto-enable relevant indicators.**\n\n"
        f"- **📊 {default_label}**: Clean chart without overlays or summaries.\n"
    )
    for label, meta in use_cases.items():
        description = meta.get("Description", "No description provided.")
        help_text += f"- **{label}**: {description}\n"

    return help_text

# -------------------------------------------------------------------------------------------------
# Function: apply_use_case_mapping
# Purpose: Maps the selected use case to relevant indicators by category
# Use Case: Shared across modules with auto-populated sidebar workflows
# -------------------------------------------------------------------------------------------------
def apply_use_case_mapping(
    selected_use_case: str,
    use_cases: dict,
    indicator_categories: dict,
    default_label: str = "Naked Charts"
) -> dict:
    """
    Maps selected use case to corresponding indicators by category.

    Parameters:
        selected_use_case (str): Use case selected in sidebar dropdown.
        use_cases (dict): Dictionary containing all use case metadata.
        indicator_categories (dict): Available indicator categories in the app.
        default_label (str): Label used to skip mapping logic (default = 'Naked Charts').

    Returns:
        dict: Dictionary mapping category → list of active indicators.
    """
    auto_selected = {category: [] for category in indicator_categories.keys()}

    if selected_use_case != default_label and selected_use_case in use_cases:
        use_case_entry = use_cases[selected_use_case]
        indicators = use_case_entry.get("Indicators", [])
        for category in use_case_entry.get("Categories", []):
            if category in indicator_categories:
                auto_selected[category].extend(indicators)

    return auto_selected

# -------------------------------------------------------------------------------------------------
# Function: resolve_canonical_use_case
# Purpose: Ensures selected label matches the metadata registry key
# Use Case: Enables AI Export to retrieve correct metadata block
# -------------------------------------------------------------------------------------------------
def resolve_canonical_use_case(selected_use_case: str, use_case_registry: dict) -> str:
    """
    Resolves a UI label or alternate title to the correct canonical use case key from the registry.
    Returns a matching key if found, else returns 'Unknown'.
    """
    if selected_use_case in use_case_registry:
        return selected_use_case

    for key, value in use_case_registry.items():
        if value.get("title", "") == selected_use_case:
            return key

    return "Unknown"
