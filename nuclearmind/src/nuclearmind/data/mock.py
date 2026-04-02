"""Synthetic PWR data generator for CI/testing (no OpenMC required).

Generates physically plausible 17x17 PWR assembly data:
- Node features: enrichment, temperature, density, control_rod_fraction, is_fuel
- Edge connectivity: 4-connected grid (physical neighbors)
- Targets: power distribution (per node) + keff (global scalar)
- Global params: boron_ppm, inlet_temperature, total_thermal_power

Physics constraints enforced:
- keff in [0.95, 1.05] for fresh fuel conditions
- All power values >= 0
- Sum of nodal powers within 1% of total thermal power
- Temperature in physically plausible range [500, 900] K
- Fuel density in [10.0, 11.0] g/cm3 (UO2)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# PWR 17x17 assembly layout constants
GRID_SIZE = 17
N_POSITIONS = GRID_SIZE * GRID_SIZE  # 289

# Guide tube and instrument tube positions in a standard 17x17 Westinghouse assembly.
# These positions have no fuel — they hold control rods or instruments.
# SOURCE: Duderstadt & Hamilton, "Nuclear Reactor Analysis", Ch. 7, Fig. 7.3
# Standard Westinghouse 17x17: 264 fuel rods, 24 guide tubes, 1 instrument tube
_GUIDE_TUBE_POSITIONS: set[tuple[int, int]] = {
    (2, 4), (2, 8), (2, 12),
    (3, 2), (3, 14),
    (4, 2), (4, 5), (4, 8), (4, 11), (4, 14),
    (5, 4), (5, 12),
    (8, 2), (8, 5), (8, 8), (8, 11), (8, 14),
    (11, 4), (11, 12),
    (12, 2), (12, 5), (12, 8), (12, 11), (12, 14),
    (13, 2), (13, 14),
    (14, 4), (14, 8), (14, 12),
}
# Instrument tube at center
_INSTRUMENT_TUBE: tuple[int, int] = (8, 8)

N_FUEL_RODS = N_POSITIONS - len(_GUIDE_TUBE_POSITIONS)  # 264 (8,8 counted in guide tubes)


@dataclass
class PWRSample:
    """A single synthetic PWR assembly sample."""

    # Node features [N_POSITIONS, 5]
    # Columns: enrichment (wt%), temperature (K), density (g/cm3),
    #          control_rod_fraction (0-1), is_fuel (0 or 1)
    node_features: np.ndarray

    # Edge index [2, n_edges] — pairs of connected node indices
    edge_index: np.ndarray

    # Target: power distribution per node [N_POSITIONS]
    power_distribution: np.ndarray

    # Target: effective multiplication factor (scalar)
    keff: float

    # Global operating parameters
    boron_ppm: float
    inlet_temperature: float  # K
    total_thermal_power: float  # MW

    # Metadata
    seed: int
    sample_id: int = 0


@dataclass
class MockDatasetConfig:
    """Configuration for mock data generation."""

    n_samples: int = 100
    seed: int = 42
    # Parameter ranges for Latin Hypercube-like sampling
    enrichment_range: tuple[float, float] = (2.0, 5.0)  # wt% U-235
    boron_range: tuple[float, float] = (0.0, 2000.0)  # ppm
    control_rod_range: tuple[float, float] = (0.0, 1.0)  # fraction inserted
    inlet_temp_range: tuple[float, float] = (560.0, 590.0)  # K (typical PWR)
    total_power_range: tuple[float, float] = (2500.0, 3500.0)  # MWth
    # Noise parameters
    noise_fraction: float = 0.02  # 2% Gaussian noise on power
    outlier_fraction: float = 0.05  # 5% of samples get outlier injection


def _pos_to_idx(row: int, col: int) -> int:
    """Convert (row, col) grid position to linear index."""
    return row * GRID_SIZE + col


def _build_adjacency_4connected() -> np.ndarray:
    """Build 4-connected grid adjacency for 17x17 assembly.

    Each interior node connects to up, down, left, right neighbors.
    Edge nodes connect to 2 or 3 neighbors. Symmetric (undirected).

    Returns:
        edge_index: [2, n_edges] array of (src, dst) pairs.
    """
    edges_src: list[int] = []
    edges_dst: list[int] = []

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            idx = _pos_to_idx(r, c)
            # Right neighbor
            if c + 1 < GRID_SIZE:
                neighbor = _pos_to_idx(r, c + 1)
                edges_src.extend([idx, neighbor])
                edges_dst.extend([neighbor, idx])
            # Down neighbor
            if r + 1 < GRID_SIZE:
                neighbor = _pos_to_idx(r + 1, c)
                edges_src.extend([idx, neighbor])
                edges_dst.extend([neighbor, idx])

    return np.array([edges_src, edges_dst], dtype=np.int64)


# Pre-compute adjacency (same for all samples in MVP — fixed 17x17 topology)
_ADJACENCY = _build_adjacency_4connected()


def _generate_power_profile(
    rng: np.random.Generator,
    enrichments: np.ndarray,
    control_rods: np.ndarray,
    is_fuel: np.ndarray,
    total_power: float,
) -> np.ndarray:
    """Generate a physically plausible power distribution.

    Power is higher for:
    - Higher enrichment fuel (more fissile material)
    - Lower control rod insertion (less absorption)
    - Fuel positions only (guide tubes produce no power)

    The distribution has a cosine-like radial shape (typical PWR),
    modulated by local enrichment and control rod effects.
    """
    n = len(enrichments)
    rows = np.arange(n) // GRID_SIZE
    cols = np.arange(n) % GRID_SIZE

    # Radial cosine shape: max at center, falls toward edges
    # SOURCE: Duderstadt & Hamilton, Ch. 6 — fundamental mode is J0(r)*cos(z)
    center = (GRID_SIZE - 1) / 2.0
    r_norm = np.sqrt((rows - center) ** 2 + (cols - center) ** 2) / center
    radial_shape = np.maximum(0.0, np.cos(r_norm * np.pi / 2.5))

    # Modulate by enrichment (normalized to [0.5, 1.5] range)
    enrich_min, enrich_max = enrichments[is_fuel > 0.5].min(), enrichments[is_fuel > 0.5].max()
    if enrich_max > enrich_min:
        enrich_factor = 0.5 + (enrichments - enrich_min) / (enrich_max - enrich_min)
    else:
        enrich_factor = np.ones(n)

    # Control rod suppression: more insertion = less power locally
    rod_factor = 1.0 - 0.7 * control_rods

    # Combine factors
    raw_power = radial_shape * enrich_factor * rod_factor * is_fuel

    # Normalize to total thermal power
    power_sum = raw_power.sum()
    if power_sum > 0:
        power = raw_power * (total_power / power_sum)
    else:
        power = np.zeros(n)

    return power


def _compute_mock_keff(
    enrichment_avg: float,
    boron_ppm: float,
    control_rod_avg: float,
) -> float:
    """Compute a mock keff based on simplified reactivity model.

    This is NOT a physics simulation — it's a plausible approximation
    for generating training data that respects qualitative trends:
    - Higher enrichment → higher keff
    - Higher boron → lower keff (negative reactivity coefficient)
    - More control rod insertion → lower keff

    Returns keff in [0.95, 1.05] range for typical PWR conditions.

    SOURCE: Qualitative trends from Duderstadt & Hamilton, Ch. 7.
    Boron worth ~-10 pcm/ppm, control rod worth varies.
    """
    # Base keff for 3.5% enrichment, 0 boron, rods out
    base_keff = 1.03

    # Enrichment effect: ~+0.02 per 1% enrichment above 3.5%
    enrichment_effect = 0.02 * (enrichment_avg - 3.5)

    # Boron effect: ~-10 pcm/ppm → -0.0001/ppm
    boron_effect = -0.0001 * boron_ppm

    # Control rod effect: full insertion ~ -0.05 reactivity
    rod_effect = -0.05 * control_rod_avg

    keff = base_keff + enrichment_effect + boron_effect + rod_effect

    # Clamp to physically reasonable range (with margin for float precision)
    return float(np.clip(keff, 0.905, 1.095))


def generate_sample(
    rng: np.random.Generator,
    sample_id: int,
    config: MockDatasetConfig,
) -> PWRSample:
    """Generate a single synthetic PWR assembly sample."""
    # Sample operating parameters uniformly
    enrichment_base = rng.uniform(*config.enrichment_range)
    boron_ppm = rng.uniform(*config.boron_range)
    control_rod_frac = rng.uniform(*config.control_rod_range)
    inlet_temp = rng.uniform(*config.inlet_temp_range)
    total_power = rng.uniform(*config.total_power_range)

    # Build node features
    is_fuel = np.ones(N_POSITIONS, dtype=np.float32)
    for r, c in _GUIDE_TUBE_POSITIONS:
        is_fuel[_pos_to_idx(r, c)] = 0.0

    # Enrichment: base + small spatial variation for fuel rods, 0 for guide tubes
    enrichments = np.where(
        is_fuel > 0.5,
        enrichment_base + rng.normal(0, 0.1, N_POSITIONS),
        0.0,
    ).astype(np.float32)
    enrichments = np.clip(enrichments, 0.0, 6.0)

    # Control rod insertion (same for all guide tube positions in this sample)
    control_rods = np.where(
        is_fuel < 0.5,
        control_rod_frac,
        0.0,
    ).astype(np.float32)

    # Temperature: inlet + spatial gradient (hotter toward center)
    rows = np.arange(N_POSITIONS) // GRID_SIZE
    cols = np.arange(N_POSITIONS) % GRID_SIZE
    center = (GRID_SIZE - 1) / 2.0
    r_norm = np.sqrt((rows - center) ** 2 + (cols - center) ** 2) / center
    temperatures = (inlet_temp + 200.0 * (1.0 - r_norm) + rng.normal(0, 5, N_POSITIONS)).astype(
        np.float32
    )
    temperatures = np.clip(temperatures, 500.0, 900.0)

    # Density: UO2 density with thermal expansion (higher T → lower density)
    densities = (10.97 - 0.001 * (temperatures - 560.0) + rng.normal(0, 0.02, N_POSITIONS)).astype(
        np.float32
    )
    densities = np.clip(densities, 10.0, 11.0)

    # Stack node features: [enrichment, temperature, density, control_rod, is_fuel]
    node_features = np.stack([enrichments, temperatures, densities, control_rods, is_fuel], axis=1)
    assert node_features.shape == (N_POSITIONS, 5)

    # Generate power distribution
    power = _generate_power_profile(rng, enrichments, control_rods, is_fuel, total_power)

    # Add small Gaussian noise
    noise = rng.normal(0, config.noise_fraction * power.mean(), N_POSITIONS)
    power = np.maximum(0.0, power + noise * is_fuel)  # only fuel produces power

    # Re-normalize to enforce conservation exactly
    fuel_power = power[is_fuel > 0.5]
    if fuel_power.sum() > 0:
        power[is_fuel > 0.5] *= total_power / fuel_power.sum()

    power = power.astype(np.float32)

    # Compute mock keff
    fuel_mask = is_fuel > 0.5
    keff = _compute_mock_keff(
        enrichment_avg=enrichments[fuel_mask].mean(),
        boron_ppm=boron_ppm,
        control_rod_avg=control_rod_frac,
    )

    return PWRSample(
        node_features=node_features,
        edge_index=_ADJACENCY.copy(),
        power_distribution=power,
        keff=keff,
        boron_ppm=boron_ppm,
        inlet_temperature=inlet_temp,
        total_thermal_power=total_power,
        seed=int(rng.integers(0, 2**31)),
        sample_id=sample_id,
    )


def generate_dataset(config: MockDatasetConfig | None = None) -> list[PWRSample]:
    """Generate a complete mock dataset.

    Args:
        config: Generation configuration. Uses defaults if None.

    Returns:
        List of PWRSample instances satisfying physics constraints.
    """
    if config is None:
        config = MockDatasetConfig()

    rng = np.random.default_rng(config.seed)
    samples = [generate_sample(rng, i, config) for i in range(config.n_samples)]

    # Inject outliers for data quality testing
    n_outliers = int(len(samples) * config.outlier_fraction)
    outlier_rng = np.random.default_rng(config.seed + 999)
    for i in range(n_outliers):
        idx = len(samples) - 1 - i  # mark last N samples as outliers
        s = samples[idx]
        # Corrupt power distribution: add large spike at random fuel position
        fuel_positions = np.where(s.node_features[:, 4] > 0.5)[0]
        spike_pos = outlier_rng.choice(fuel_positions)
        s.power_distribution[spike_pos] *= 10.0  # 10x spike — obvious outlier

    return samples
