"""Frame synchronisation (W05): find where the burst starts using a known preamble."""

from __future__ import annotations

import numpy as np


def zadoff_chu(length: int, root: int = 25) -> np.ndarray:
    """Zadoff-Chu sequence (constant amplitude, ideal periodic autocorrelation).

    Same family as the 5G NR / LTE PSS. ``root`` must be coprime with ``length``.
    """
    raise NotImplementedError("W05: Zadoff-Chu preamble")


def detect_preamble(x: np.ndarray, preamble: np.ndarray, threshold: float = 0.5) -> int:
    """Return the index where the preamble starts, via normalised cross-correlation.

    Normalise by the local signal energy so the threshold does not depend on SNR or
    gain. Raise or return -1 if nothing crosses the threshold.
    """
    raise NotImplementedError("W05: correlator")
