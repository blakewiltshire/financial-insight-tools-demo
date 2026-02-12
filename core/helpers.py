"""
helpers.py

Minimal helper utilities for the FIT Demo.

Only the functions actively used across FIT pages are included here:
- load_markdown_file: safe markdown loader
- get_named_paths: lightweight project path resolver

This file is intentionally cloud-safe and contains no subprocess,
network, or system-level operations.
"""

from __future__ import annotations

import os
from typing import Dict


def load_markdown_file(file_path: str) -> str | None:
    """
    Load and return the contents of a markdown file.

    Parameters
    ----------
    file_path : str
        Absolute or relative path to the markdown file.

    Returns
    -------
    str or None
        Markdown file content if readable, otherwise None.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (FileNotFoundError, OSError):
        return None


def get_named_paths(current_file: str, max_levels: int = 6) -> Dict[str, str]:
    """
    Generate incrementally higher-level project paths relative to the calling file.

    Parameters
    ----------
    current_file : str
        Typically passed as __file__ from the calling module.
    max_levels : int, optional
        Number of directory levels to traverse upwards, by default 6.

    Returns
    -------
    dict
        A mapping:
            "level_up_0": directory of current_file
            "level_up_1": 1 directory above
            ...
            "level_up_n": n directories above
    """
    base_dir = os.path.abspath(os.path.dirname(current_file))
    paths = {
        f"level_up_{i}": os.path.abspath(
            os.path.join(base_dir, *([".."] * i))
        )
        for i in range(max_levels + 1)
    }
    return paths


# -------------------------------------------------------------------------------------------------
# Function: build_sidebar_links
# Purpose: Auto-detect pages/*py for navigation
# Use By: All apps in modular pages format
# -------------------------------------------------------------------------------------------------
def build_sidebar_links(pages_dir="pages", exclude=None):
    """
    Dynamically build Streamlit sidebar links from `pages_dir`.

    Args:
        pages_dir (str): Directory to scan
        exclude (list): Optional filenames to skip

    Returns:
        list: Tuples of (file_path, label)
    """
    if exclude is None:
        exclude = []

    links = []
    if os.path.exists(pages_dir):
        for f in os.listdir(pages_dir):
            if f.endswith(".py") and f[0:2].isdigit() and f not in exclude:
                label = f.split("_", 1)[1].replace(".py", "").replace("_", " ").title()
                file_path = f"{pages_dir}/{f}"
                links.append((file_path, label))

    return sorted(links, key=lambda x: int(x[0].split("/")[1].split("_")[0]))
