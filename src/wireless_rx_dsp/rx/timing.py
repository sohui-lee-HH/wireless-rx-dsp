"""Symbol timing recovery (W03).

Goal: find the best sampling instant inside each symbol and track it as it drifts
(sample-rate offset), so the downsampler hits the eye at its widest opening.
"""

from __future__ import annotations

import numpy as np


def gardner(
    x: np.ndarray,
    sps: int,
    loop_bw: float = 0.01,
    damping: float = 1 / np.sqrt(2),
) -> tuple[np.ndarray, np.ndarray]:
    """Gardner timing-error detector + PI loop filter + interpolator.

    Parameters
    ----------
    x : matched-filtered signal at ``sps`` samples per symbol
    loop_bw : normalised loop bandwidth (per symbol)

    Returns
    -------
    symbols : one sample per symbol at the recovered timing
    mu : fractional timing estimate per symbol, for plotting convergence

    Gardner TED (2 samples/symbol view): e[k] = Re{ conj(y[k] - y[k-1]) * y[k-1/2] }
    """
    raise NotImplementedError("W03: Gardner timing recovery")
