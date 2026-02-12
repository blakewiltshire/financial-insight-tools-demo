# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name
# pylint: disable=unused-argument

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------

"""
Indicator Placeholder Module

This file defines placeholder functions and a compatible mapping
for future integration into indicator toggles, chart displays, and summaries.
"""

# -------------------------------------------------------------------------------------------------
# Example Indicator placeholder
# -------------------------------------------------------------------------------------------------
# Calculates signals for:
# - Example placeholder
# -------------------------------------------------------------------------------------------------

# --- Example placeholder ---
def indicator_1(df=None, period=14):
    """ . """
    return "Placeholder for Indicator 1"

def indicator_2(df=None, period=14):
    """ . """
    return "Placeholder for Indicator 2"

# -------------------------------------------------------------------------------------------------
# Indicator Function Mapping for Use Case Apps
# -------------------------------------------------------------------------------------------------
options_indicator_map = {
    "Indicator 1": indicator_1,
    "Indicator 2": indicator_2
}
