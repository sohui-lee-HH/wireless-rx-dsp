"""Root-raised-cosine pulse shaping.

The same RRC taps are used at the transmitter and (time-reversed, conjugated) as the
receiver's matched filter. Their cascade is a raised-cosine pulse: zero ISI at the
correct sampling instants.
"""

from __future__ import annotations

import numpy as np


def rrc_taps(sps: int, rolloff: float = 0.35, span: int = 10) -> np.ndarray:
    """Root-raised-cosine FIR taps, normalised to unit energy.

    Parameters
    ----------
    sps : samples per symbol
    rolloff : excess bandwidth beta, 0 < beta <= 1
    span : filter length in symbols (total taps = span * sps + 1)
    """
    if not 0 < rolloff <= 1:
        raise ValueError("rolloff must be in (0, 1]")
    n = np.arange(-span * sps / 2, span * sps / 2 + 1)
    t = n / sps
    b = rolloff
    h = np.empty_like(t, dtype=float)

    center = np.isclose(t, 0.0)
    edge = np.isclose(np.abs(t), 1.0 / (4.0 * b))
    rest = ~(center | edge)

    h[center] = 1.0 + b * (4.0 / np.pi - 1.0)
    h[edge] = (b / np.sqrt(2.0)) * (
        (1 + 2 / np.pi) * np.sin(np.pi / (4 * b)) + (1 - 2 / np.pi) * np.cos(np.pi / (4 * b))
    )
    tr = t[rest]
    h[rest] = (
        np.sin(np.pi * tr * (1 - b)) + 4 * b * tr * np.cos(np.pi * tr * (1 + b))
    ) / (np.pi * tr * (1 - (4 * b * tr) ** 2))

    return h / np.sqrt(np.sum(h**2))


def pulse_shape(symbols: np.ndarray, taps: np.ndarray, sps: int) -> np.ndarray:
    """Upsample by ``sps`` (zero insertion) and filter with ``taps``.

    Output length is ``len(symbols) * sps + len(taps) - 1`` (full convolution), so the
    filter tails are kept and the receiver can see the whole burst.
    """
    up = np.zeros(len(symbols) * sps, dtype=complex)
    up[::sps] = symbols
    return np.convolve(up, taps)
