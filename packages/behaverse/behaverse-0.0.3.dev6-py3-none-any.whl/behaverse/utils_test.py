"""Test utility functions."""

from .utils import list_datasets


def test_list_datasets():
    """List available datasets."""
    datasets = list_datasets()
    print(datasets)
