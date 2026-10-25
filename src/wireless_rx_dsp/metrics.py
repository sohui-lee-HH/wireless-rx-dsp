"""Figures of merit and their theoretical references."""

from __future__ import annotations

import numpy as np
from scipy.special import erfc


def ber(tx_bits: np.ndarray, rx_bits: np.ndarray) -> float:
    tx_bits, rx_bits = np.asarray(tx_bits).ravel(), np.asarray(rx_bits).ravel()
    if tx_bits.shape != rx_bits.shape:
        raise ValueError("bit arrays differ in length")
    return float(np.mean(tx_bits != rx_bits))


def evm_rms(rx: np.ndarray, ref: np.ndarray) -> float:
    """RMS error vector magnitude, as a fraction of RMS reference power (x100 for %)."""
    return float(np.sqrt(np.mean(np.abs(rx - ref) ** 2) / np.mean(np.abs(ref) ** 2)))


def evm_db(rx: np.ndarray, ref: np.ndarray) -> float:
    return 20 * np.log10(evm_rms(rx, ref))


def qfunc(x: np.ndarray) -> np.ndarray:
    return 0.5 * erfc(np.asarray(x) / np.sqrt(2))


def ber_theory(ebn0_db: np.ndarray, M: int) -> np.ndarray:
    """Theoretical BER on AWGN with Gray coding.

    Exact for BPSK and QPSK; the standard nearest-neighbour approximation for square
    M-QAM (tight at the BERs we plot).
    """
    g = 10 ** (np.asarray(ebn0_db, dtype=float) / 10)
    if M in (2, 4):
        return qfunc(np.sqrt(2 * g))
    k = np.log2(M)
    return (4 / k) * (1 - 1 / np.sqrt(M)) * qfunc(np.sqrt(3 * k / (M - 1) * g))
