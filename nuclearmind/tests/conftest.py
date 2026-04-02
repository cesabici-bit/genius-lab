"""Shared test fixtures for NuclearMind."""

import numpy as np
import pytest

from nuclearmind.data.mock import MockDatasetConfig, generate_dataset, generate_sample


@pytest.fixture(scope="session")
def mock_dataset():
    """Generate a mock dataset of 100 samples (shared across all tests in session)."""
    config = MockDatasetConfig(n_samples=100, seed=42)
    return generate_dataset(config)


@pytest.fixture(scope="session")
def clean_dataset():
    """Generate a clean dataset without outlier injection (for physics checks)."""
    config = MockDatasetConfig(n_samples=50, seed=123, outlier_fraction=0.0)
    return generate_dataset(config)


@pytest.fixture
def single_sample():
    """Generate a single clean sample for unit tests."""
    rng = np.random.default_rng(42)
    config = MockDatasetConfig(n_samples=1, seed=42, outlier_fraction=0.0)
    return generate_sample(rng, sample_id=0, config=config)
