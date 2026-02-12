# -------------------------------------------------------------------------------------------------
#  ---- pylint global exceptions ----
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order
# pylint: disable=invalid-name, non-ascii-file-name

# -------------------------------------------------------------------------------------------------
# 📄 registry_loader.py
# Modular loader and plot-filter builder for dataset registry
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# Docstring
# -------------------------------------------------------------------------------------------------
"""
Dataset Registry Utilities

This module provides standardised utilities for:
1. Loading all datasets defined in a registry with cleaning functions.
2. Constructing a filtered dataset map based on 'plot' eligibility.

Intended for use in Economic Exploration modules and other multi-country apps.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import pandas as pd
from typing import Callable


# -------------------------------------------------------------------------------------------------
# Loader — Full Registry Loader with Cleaning
# -------------------------------------------------------------------------------------------------
def load_all_datasets_from_registry(dataset_registry: dict) -> dict:
    """
    Load and clean all datasets defined in the registry.

    Args:
        dataset_registry (dict): Configuration mapping for datasets.

    Returns:
        dict: Dictionary of cleaned DataFrames keyed by dataset name.
    """
    loaded_datasets = {}
    for key, config in dataset_registry.items():
        file_path = config["folder"] / config["file"]
        cleaner_func: Callable = config["cleaner"]
        try:
            raw_df = pd.read_csv(file_path)
            cleaned_df = cleaner_func(raw_df)
            loaded_datasets[key] = cleaned_df
        except Exception as e:
            print(f"[!] Failed to load dataset '{key}': {e}")
    return loaded_datasets


# -------------------------------------------------------------------------------------------------
# Builder — Plot-Eligible Dataset Filter
# -------------------------------------------------------------------------------------------------
def build_df_map_from_registry(dataset_registry: dict, loaded_datasets: dict) -> dict:
    """
    Extract a filtered chart-ready dataset map from full loaded datasets.

    Only includes datasets flagged with `plot: True`.

    Args:
        dataset_registry (dict): Dataset metadata definitions.
        loaded_datasets (dict): Dictionary of preloaded and cleaned DataFrames.

    Returns:
        dict: Dictionary of datasets to be used for plotting.
    """
    return {
        key: loaded_datasets[key]
        for key, meta in dataset_registry.items()
        if meta.get("plot", False) and key in loaded_datasets
    }
