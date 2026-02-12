# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=invalid-name


# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
helpers.py

This module contains utility functions for the application, including file loading,
subprocess launching, dynamic navigation, and directory management logic. It is used
throughout the Financial Insight Tools system.
"""

# -------------------------------------------------------------------------------------------------
# Standard library
# -------------------------------------------------------------------------------------------------
import os
import random
import socket
import subprocess
from contextlib import contextmanager
from pathlib import Path

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st


# -------------------------------------------------------------------------------------------------
# Function: load_markdown_file
# Purpose: Load any markdown file
# Use By: All modules
# -------------------------------------------------------------------------------------------------
def load_markdown_file(file_path):
    """
    Load and return the contents of a markdown file.

    Args:
        file_path (str): Path to the markdown file.

    Returns:
        str or None: File content, or None if not found.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


# -------------------------------------------------------------------------------------------------
# Function: load_about_file
# Purpose: Load per-module or fallback markdown
# Use By: All modules
# -------------------------------------------------------------------------------------------------
def load_about_file(base_path, module_name):
    """
    Load the most specific About markdown file available.

    Tries:
    1. /apps/module_name/about/about_this_app.md
    2. /docs/about_and_support.md (fallback)

    Args:
        base_path (str): Absolute path to root.
        module_name (str): Module folder name.

    Returns:
        tuple: Title label and markdown string.
    """
    custom_about_path = os.path.join(base_path, "apps", module_name, "about", "about_this_app.md")
    default_about_path = os.path.join(base_path, "docs", "about_and_support.md")

    if os.path.exists(custom_about_path):
        return ("📘 About This App", load_markdown_file(custom_about_path))

    return ("📘 About & Support", load_markdown_file(default_about_path))


# -------------------------------------------------------------------------------------------------
# Function: render_module_dashboard
# Purpose: UI for launching modules
# Use By: Financial Insight Tools launcher
# -------------------------------------------------------------------------------------------------
def render_module_dashboard(modules, root_path):
    """
    Generate Insight Tools launcher UI with launch buttons.

    Args:
        modules (list): List of dicts (title, description, path, filename, button, column).
        root_path (str): Absolute path to project root.
    """
    st.header("📂 Main Modules")
    col1, col2 = st.columns(2)
    for module in modules:
        with col1 if module["column"] == 1 else col2:
            st.markdown(f"### {module['title']}")
            st.write(module["description"])
            if st.button(module["button"]):
                try:
                    full_path = Path(root_path) / Path(module["path"])
                    launch_streamlit_app(str(full_path), module["filename"])
                except FileNotFoundError:
                    st.error(
                        f"Launch failed: File not found at {module['path']}/{module['filename']}"
                    )
                except RuntimeError as e:
                    st.error(f"Launch failed: {str(e)}")
                except OSError as e:
                    st.error(f"OSError encountered: {e}")

            st.divider()


# -------------------------------------------------------------------------------------------------
# Function: get_project_base_path
# Purpose: Resolve root relative to core/helpers.py
# Use By: Country paths and shared logic
# -------------------------------------------------------------------------------------------------
def get_project_base_path():
    """
    Return the absolute path to the project root directory.

    Returns:
        str: One level up from current file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# -------------------------------------------------------------------------------------------------
# Function: get_parent_path
# Purpose: Traverse upwards N levels
# Use By: General path resolution
# -------------------------------------------------------------------------------------------------
def get_parent_path(path, levels_up=1):
    """
    Traverse up N levels from a given path.

    Args:
        path (str): Starting file or folder path.
        levels_up (int): Number of directory levels to go up.

    Returns:
        str: Absolute path N levels above the input.
    """
    for _ in range(levels_up):
        new_path = os.path.abspath(os.path.join(path, '..'))
        if new_path == path:
            break
        path = new_path
    return path


# -------------------------------------------------------------------------------------------------
# Function: get_named_paths
# Purpose: Named path map for N levels
# Use By: ALL apps
# -------------------------------------------------------------------------------------------------
def get_named_paths(current_file, max_levels=6):
    """
    Returns a dictionary of incrementally higher paths for flexible access.

    Keys:
        level_up_0 to level_up_n

    Args:
        current_file (str): Typically __file__
        max_levels (int): How many levels to return

    Returns:
        dict: Map of labelled paths
    """
    base = os.path.abspath(os.path.dirname(current_file))
    levels = {f"level_up_{i}": get_parent_path(base, i) for i in range(max_levels + 1)}
    return levels


# -------------------------------------------------------------------------------------------------
# Function: get_country_path
# Purpose: Economic Exploration folder resolution
# Use By: Economic Exploration
# -------------------------------------------------------------------------------------------------
def get_country_path(country_name):
    """
    Given a country name (e.g., 'United States'), return path to country folder.

    Args:
        country_name (str): Full name

    Returns:
        str: Absolute path under /economic_exploration/<country>
    """
    project_base = get_project_base_path()
    country_code = country_name.lower().replace(" ", "_")
    return os.path.join(project_base, "economic_exploration", country_code)


# -------------------------------------------------------------------------------------------------
# Function: find_open_port
# Purpose: Resolve port for subprocess app
# Use By: Economic Exploration
# -------------------------------------------------------------------------------------------------
def find_open_port(start=8601, max_tries=100):
    """
    Scan for an unused localhost port (for subprocess launches).

    Args:
        start (int): Starting port range
        max_tries (int): Attempts before giving up

    Returns:
        int: Available port number
    """
    for _ in range(max_tries):
        port = random.randint(start, start + 1000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("No available ports found.")


# -------------------------------------------------------------------------------------------------
# Function: launch_streamlit_app
# Purpose: Run Streamlit in subprocess
# Use By: Economic Exploration, Main Launcher
# -------------------------------------------------------------------------------------------------
def launch_streamlit_app(path, filename):
    """
    Launch a Streamlit app in a subprocess with an available port.

    Args:
        path (str): Absolute path to directory containing the app file.
        filename (str): Name of the Streamlit .py file to run.

    Returns:
        str: Localhost URL for the launched app instance.
    """
    full_path = os.path.join(path, filename)
    if not os.path.isfile(full_path):
        raise FileNotFoundError(f"{full_path} not found.")

    port = find_open_port()
    command = ["streamlit", "run", filename, "--server.port", str(port)]

    # pylint: disable=consider-using-with
    subprocess.Popen(
        command,
        cwd=path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    # pylint: enable=consider-using-with

    return f"http://localhost:{port}"


# -------------------------------------------------------------------------------------------------
# Function: temporary_change_dir
# Purpose: Context-managed directory switch
# Use By: Economic Exploration, Folium-style libraries
# -------------------------------------------------------------------------------------------------
@contextmanager
def temporary_change_dir(path):
    """
    Temporarily switch the working directory.

    Args:
        path (str): Directory to switch into

    Usage:
        with temporary_change_dir("/some/folder"):
            do_something()
    """
    original_path = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_path)


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
