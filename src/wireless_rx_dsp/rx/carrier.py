"""Carrier recovery (W04): a coarse open-loop estimate, then a closed loop for the residual."""

from __future__ import annotations

import numpy as np


def coarse_cfo(x: np.ndarray, fs: float, M: int = 4) -> float:
    """Estimate the frequency offset in Hz.

    Classic approach: raise to the M-th power to strip the modulation (for M-PSK), take
    an FFT and find the peak; the offset is peak_freq / M. Valid range is +/- fs/(2M).
    """
    raise NotImplementedError("W04: coarse frequency-offset estimate")


def costas(
    symbols: np.ndarray,
    M: int = 4,
    loop_bw: float = 0.02,
    damping: float = 1 / np.sqrt(2),
) -> tuple[np.ndarray, np.ndarray]:
    """Decision-directed Costas loop / second-order PLL at one sample per symbol.

    Returns
    -------
    corrected : de-rotated symbols
    phase : phase estimate per symbol (plot it to show lock-in)
    """
    raise NotImplementedError("W04: Costas loop / PLL")
