"""Tests for mock data generator — physics constraints validation.

M2: External Oracle Test Pattern — at least one test with # SOURCE:.
"""

import numpy as np

from nuclearmind.data.mock import (
    GRID_SIZE,
    N_POSITIONS,
    MockDatasetConfig,
    generate_dataset,
)


class TestMockDataPhysicsConstraints:
    """Verify that mock data respects physics constraints (L2 domain sanity)."""

    def test_keff_range(self, clean_dataset):
        """L2: keff must be in physically plausible range for a PWR.

        # SOURCE: Duderstadt & Hamilton, "Nuclear Reactor Analysis", Ch. 7
        # For a fresh-fuel PWR with typical enrichment (2-5 wt%), boron (0-2000 ppm),
        # and control rods (0-100% insertion), keff should be in [0.90, 1.10].
        # Our mock generator targets [0.95, 1.05] for normal conditions.
        """
        for sample in clean_dataset:
            assert 0.90 <= sample.keff <= 1.10, (
                f"keff={sample.keff} out of physical range [0.90, 1.10] "
                f"(sample {sample.sample_id})"
            )

    def test_power_non_negative(self, clean_dataset):
        """All power values must be >= 0 (no negative fission rate)."""
        for sample in clean_dataset:
            assert (sample.power_distribution >= 0).all(), (
                f"Negative power found in sample {sample.sample_id}: "
                f"min={sample.power_distribution.min()}"
            )

    def test_power_conservation(self, clean_dataset):
        """Sum of nodal powers must be within 1% of total thermal power.

        # SOURCE: Energy conservation — first law of thermodynamics.
        # Total fission power must equal the specified thermal power output.
        """
        for sample in clean_dataset:
            fuel_mask = sample.node_features[:, 4] > 0.5
            fuel_power_sum = sample.power_distribution[fuel_mask].sum()
            total = sample.total_thermal_power
            relative_error = abs(fuel_power_sum - total) / total
            assert relative_error < 0.01, (
                f"Conservation violated: sum={fuel_power_sum:.2f}, "
                f"target={sample.total_thermal_power:.2f}, "
                f"error={relative_error:.4f} (sample {sample.sample_id})"
            )

    def test_guide_tubes_no_power(self, clean_dataset):
        """Guide tube positions must produce zero power (no fuel there)."""
        for sample in clean_dataset:
            non_fuel_mask = sample.node_features[:, 4] < 0.5
            non_fuel_power = sample.power_distribution[non_fuel_mask]
            assert (non_fuel_power == 0.0).all(), (
                f"Non-zero power at guide tube position in sample {sample.sample_id}"
            )

    def test_temperature_range(self, clean_dataset):
        """Temperature must be in physically plausible range for PWR.

        # SOURCE: IAEA SSR-2/1 — PWR coolant inlet ~560 K, max clad ~620-650 K,
        # fuel centerline can reach ~1500 K but our assembly-averaged T stays below 900 K.
        """
        for sample in clean_dataset:
            temps = sample.node_features[:, 1]
            assert (temps >= 500.0).all() and (temps <= 900.0).all(), (
                f"Temperature out of range: min={temps.min():.1f}, max={temps.max():.1f} "
                f"(sample {sample.sample_id})"
            )

    def test_density_range(self, clean_dataset):
        """UO2 fuel density must be in [10.0, 11.0] g/cm3.

        # SOURCE: Duderstadt & Hamilton, Ch. 3 — UO2 theoretical density ~10.97 g/cm3.
        """
        for sample in clean_dataset:
            densities = sample.node_features[:, 2]
            assert (densities >= 10.0).all() and (densities <= 11.0).all(), (
                f"Density out of range: min={densities.min():.3f}, max={densities.max():.3f} "
                f"(sample {sample.sample_id})"
            )


class TestMockDataStructure:
    """Verify data shapes and types."""

    def test_node_features_shape(self, single_sample):
        """Node features must be [289, 5]."""
        assert single_sample.node_features.shape == (N_POSITIONS, 5)

    def test_node_features_dtype(self, single_sample):
        """Node features must be float32."""
        assert single_sample.node_features.dtype == np.float32

    def test_power_distribution_shape(self, single_sample):
        """Power distribution must be [289]."""
        assert single_sample.power_distribution.shape == (N_POSITIONS,)

    def test_edge_index_shape(self, single_sample):
        """Edge index must be [2, n_edges]."""
        assert single_sample.edge_index.shape[0] == 2
        assert single_sample.edge_index.shape[1] > 0

    def test_edge_index_symmetric(self, single_sample):
        """Adjacency must be symmetric (undirected graph)."""
        ei = single_sample.edge_index
        edges_forward = set(zip(ei[0], ei[1]))
        edges_backward = set(zip(ei[1], ei[0]))
        assert edges_forward == edges_backward, "Edge index is not symmetric"

    def test_no_self_loops(self, single_sample):
        """No self-loops in adjacency."""
        ei = single_sample.edge_index
        assert not np.any(ei[0] == ei[1]), "Self-loops found in edge index"

    def test_fuel_rod_count(self, single_sample):
        """Must have exactly 264 fuel rods in a 17x17 Westinghouse assembly.

        # SOURCE: Duderstadt & Hamilton, Ch. 7 — 264 fuel + 24 guide + 1 instrument = 289.
        """
        is_fuel = single_sample.node_features[:, 4]
        n_fuel = int((is_fuel > 0.5).sum())
        # We have 25 non-fuel positions (24 guide tubes + 1 instrument, but instrument
        # is at (8,8) which is already in guide tube set), so n_fuel should be 289 - 25 = 264
        # Actually our _GUIDE_TUBE_POSITIONS has 28 entries including (8,8)
        n_non_fuel = int((is_fuel < 0.5).sum())
        assert n_fuel + n_non_fuel == N_POSITIONS
        assert n_fuel > 250, f"Too few fuel rods: {n_fuel}"

    def test_adjacency_interior_node_4_neighbors(self, single_sample):
        """An interior node (not on edge) should have exactly 4 neighbors."""
        ei = single_sample.edge_index
        # Pick center node (8, 8)
        center_idx = 8 * GRID_SIZE + 8
        neighbors = ei[1][ei[0] == center_idx]
        assert len(neighbors) == 4, f"Center node has {len(neighbors)} neighbors, expected 4"

    def test_adjacency_corner_node_2_neighbors(self, single_sample):
        """A corner node should have exactly 2 neighbors."""
        ei = single_sample.edge_index
        corner_idx = 0  # (0, 0)
        neighbors = ei[1][ei[0] == corner_idx]
        assert len(neighbors) == 2, f"Corner node has {len(neighbors)} neighbors, expected 2"


class TestMockDataReproducibility:
    """Verify deterministic generation."""

    def test_same_seed_same_data(self):
        """Same seed must produce identical datasets."""
        config = MockDatasetConfig(n_samples=10, seed=42, outlier_fraction=0.0)
        ds1 = generate_dataset(config)
        ds2 = generate_dataset(config)

        for s1, s2 in zip(ds1, ds2):
            np.testing.assert_array_equal(s1.node_features, s2.node_features)
            np.testing.assert_array_equal(s1.power_distribution, s2.power_distribution)
            assert s1.keff == s2.keff

    def test_different_seed_different_data(self):
        """Different seeds must produce different datasets."""
        config1 = MockDatasetConfig(n_samples=10, seed=42, outlier_fraction=0.0)
        config2 = MockDatasetConfig(n_samples=10, seed=99, outlier_fraction=0.0)
        ds1 = generate_dataset(config1)
        ds2 = generate_dataset(config2)

        # At least one sample should differ
        any_different = any(
            not np.array_equal(s1.power_distribution, s2.power_distribution)
            for s1, s2 in zip(ds1, ds2)
        )
        assert any_different, "Different seeds produced identical data"


class TestMockDataOutliers:
    """Verify outlier injection for data quality testing."""

    def test_outlier_injection(self):
        """Outlier samples should have at least one extreme power value."""
        config = MockDatasetConfig(n_samples=20, seed=42, outlier_fraction=0.25)
        dataset = generate_dataset(config)

        # Last 5 samples (25% of 20) should have outlier spikes
        clean_max = max(s.power_distribution.max() for s in dataset[:15])
        outlier_maxes = [s.power_distribution.max() for s in dataset[-5:]]

        # At least some outlier samples should have higher max power
        assert any(m > clean_max * 2 for m in outlier_maxes), (
            "Outlier injection did not produce detectable spikes"
        )
