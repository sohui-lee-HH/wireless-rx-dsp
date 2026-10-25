"""Matched filter: correlate with the transmit pulse to maximise SNR at the sampling instant."""

from __future__ import annotations

import numpy as np


def matched_filter(x: np.ndarray, taps: np.ndarray) -> np.ndarray:
    """Filter with the time-reversed conjugate of the TX pulse (full convolution).

    For the symmetric real RRC this equals the TX taps; written generally so it still
    holds if the pulse changes. TX filter + matched filter delay = ``len(taps) - 1``.
    """
    return np.convolve(x, np.conj(taps[::-1]))
