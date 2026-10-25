"""Constellation mapping and hard-decision demapping.

This is the single place where Project 1 (iqmodrec) plugs in. For now it holds a
minimal Gray-coded BPSK / square-QAM mapper so the baseline runs on its own. Once
iqmodrec is installable, replace the bodies of ``modulate`` / ``demodulate`` with
calls into it and keep these signatures, so nothing else in the package changes.

All constellations are normalised to unit average symbol energy (Es = 1).
"""

from __future__ import annotations

import numpy as np

SUPPORTED_M = (2, 4, 16, 64)


def bits_per_symbol(M: int) -> int:
    if M not in SUPPORTED_M:
        raise ValueError(f"M={M} not supported, choose one of {SUPPORTED_M}")
    return int(np.log2(M))


def _gray(n: np.ndarray) -> np.ndarray:
    return n ^ (n >> 1)


def _axis_tables(m: int) -> tuple[np.ndarray, np.ndarray]:
    """Gray label of each PAM level index, and its inverse (label -> level index)."""
    idx = np.arange(m)
    label = _gray(idx)
    inv = np.empty(m, dtype=int)
    inv[label] = idx
    return label, inv


def _bits_to_int(b: np.ndarray) -> np.ndarray:
    weights = 1 << np.arange(b.shape[1] - 1, -1, -1)
    return b @ weights


def _int_to_bits(v: np.ndarray, n: int) -> np.ndarray:
    shifts = np.arange(n - 1, -1, -1)
    return ((v[:, None] >> shifts) & 1).astype(np.uint8)


def modulate(bits: np.ndarray, M: int = 4) -> np.ndarray:
    """Map a bit array to complex symbols (Gray coded, Es = 1)."""
    k = bits_per_symbol(M)
    bits = np.asarray(bits, dtype=np.int64).ravel()
    if bits.size % k:
        raise ValueError(f"number of bits ({bits.size}) must be a multiple of {k}")
    b = bits.reshape(-1, k)
    if M == 2:
        return (2.0 * b[:, 0] - 1.0).astype(complex)

    m = int(np.sqrt(M))
    half = k // 2
    _, inv = _axis_tables(m)
    i_amp = 2 * inv[_bits_to_int(b[:, :half])] - (m - 1)
    q_amp = 2 * inv[_bits_to_int(b[:, half:])] - (m - 1)
    norm = np.sqrt(2.0 * (M - 1) / 3.0)
    return (i_amp + 1j * q_amp) / norm


def demodulate(symbols: np.ndarray, M: int = 4) -> np.ndarray:
    """Hard-decision demapping back to bits (nearest constellation point)."""
    k = bits_per_symbol(M)
    s = np.asarray(symbols).ravel()
    if M == 2:
        return (s.real > 0).astype(np.uint8)

    m = int(np.sqrt(M))
    half = k // 2
    label, _ = _axis_tables(m)
    norm = np.sqrt(2.0 * (M - 1) / 3.0)

    def axis(a: np.ndarray) -> np.ndarray:
        idx = np.clip(np.round((a * norm + (m - 1)) / 2.0), 0, m - 1).astype(int)
        return _int_to_bits(label[idx], half)

    return np.hstack([axis(s.real), axis(s.imag)]).ravel()
