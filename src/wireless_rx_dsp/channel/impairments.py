"""Channel impairments (W02).

Each function takes an oversampled complex baseband signal and returns the impaired
signal. They are deliberately separate so experiments can switch one impairment on at
a time and show the matching receiver block removing it.

The tests for these already exist in ``tests/test_channel.py`` (currently skipped):
implement a function, delete its ``skip`` marker, and run ``pytest``.
"""

from __future__ import annotations

import numpy as np


def frequency_offset(x: np.ndarray, f_offset_hz: float, fs: float, phase0: float = 0.0) -> np.ndarray:
    """Carrier frequency offset: rotate by exp(j*(2*pi*f_offset*n/fs + phase0)).

    Models LO mismatch between transmitter and receiver (and Doppler, if f_offset is
    made time-varying later). Undone by ``rx.carrier``.
    """
    raise NotImplementedError("W02: carrier frequency offset")


def fractional_delay(x: np.ndarray, delay_samples: float, ntaps: int = 41) -> np.ndarray:
    """Delay by a non-integer number of samples (windowed-sinc FIR).

    The receiver does not know where the symbol centres are; this shifts them off the
    sampling grid. Undone by ``rx.timing``. Keep the output the same length as x.
    """
    raise NotImplementedError("W02: fractional timing offset")


def sample_rate_offset(x: np.ndarray, ppm: float) -> np.ndarray:
    """Resample by (1 + ppm*1e-6) to model TX/RX clock mismatch.

    Unlike a fixed delay, the timing error now drifts across the burst, so the timing
    loop has to track it, not just estimate it once. Undone by ``rx.timing``.
    Hint: ``scipy.signal.resample_poly`` or interpolation on a stretched time axis.
    """
    raise NotImplementedError("W02: sample-rate offset")


def multipath(x: np.ndarray, taps: np.ndarray) -> np.ndarray:
    """Static multipath: convolve with a complex channel impulse response.

    Causes inter-symbol interference. Undone by ``rx.equalizer``. Keep the output the
    same length as x (truncate the tail) so delays stay easy to reason about.
    """
    raise NotImplementedError("W02: multipath")


def prepend_silence(x: np.ndarray, n_samples: int) -> np.ndarray:
    """Insert ``n_samples`` zeros before the burst, so the start is unknown to the RX.

    Add noise *after* this so the silence is noise, not zeros. Undone by ``rx.frame_sync``.
    """
    raise NotImplementedError("W02: unknown burst start")
