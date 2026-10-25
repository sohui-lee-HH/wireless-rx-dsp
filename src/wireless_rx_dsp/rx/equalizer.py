"""Adaptive equalisation (W06): undo multipath ISI."""

from __future__ import annotations

import numpy as np


def lms(
    symbols: np.ndarray,
    training: np.ndarray,
    ntaps: int = 11,
    mu: float = 0.01,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Trained LMS equaliser (switch to decision-directed after the training symbols).

    Returns
    -------
    equalised : output symbols
    taps : final equaliser taps
    err : |error|^2 per symbol (learning curve)
    """
    raise NotImplementedError("W06: LMS equaliser")


def cma(
    symbols: np.ndarray,
    ntaps: int = 11,
    mu: float = 1e-3,
    R2: float | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Blind constant-modulus equaliser: needs no training, only the constellation's modulus.

    R2 defaults to E|s|^4 / E|s|^2 for the constellation in use.
    """
    raise NotImplementedError("W06: CMA equaliser")
