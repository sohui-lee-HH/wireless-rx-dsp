"""Additive white Gaussian noise, calibrated in Es/N0."""

from __future__ import annotations

import numpy as np


def awgn(
    x: np.ndarray,
    esn0_db: float,
    sps: int = 1,
    es: float = 1.0,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Add complex AWGN so that the symbol-level SNR after matched filtering is Es/N0.

    With unit-energy RRC taps, each symbol of energy ``es`` is spread over ``sps``
    samples, and a matched filter collects it back into one sample of amplitude
    sqrt(es). Adding noise of variance N0 per complex sample therefore gives exactly
    Es/N0 at the decision point.

    Convert from Eb/N0 with ``esn0_db = ebn0_db + 10*log10(bits_per_symbol)``.

    Parameters
    ----------
    x : oversampled baseband signal
    esn0_db : target Es/N0 in dB
    sps : samples per symbol (only documents the convention; noise is per sample)
    es : symbol energy of the transmitted constellation (1.0 for this package)
    rng : numpy Generator, for reproducible runs
    """
    rng = np.random.default_rng() if rng is None else rng
    n0 = es / 10 ** (esn0_db / 10)
    noise = np.sqrt(n0 / 2) * (rng.standard_normal(len(x)) + 1j * rng.standard_normal(len(x)))
    return x + noise
