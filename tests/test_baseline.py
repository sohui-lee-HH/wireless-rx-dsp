"""Known-answer tests for the parts that exist today: TX, AWGN, matched filter, genie receiver."""

import numpy as np
import pytest

from wireless_rx_dsp import Receiver, RxConfig
from wireless_rx_dsp.channel import awgn
from wireless_rx_dsp.metrics import ber, ber_theory, evm_db
from wireless_rx_dsp.tx import bits_per_symbol, demodulate, modulate, pulse_shape, rrc_taps
from wireless_rx_dsp.tx.symbols import SUPPORTED_M


def _burst(M, n_sym, sps, rng):
    bits = rng.integers(0, 2, n_sym * bits_per_symbol(M))
    sym = modulate(bits, M)
    cfg = RxConfig(M=M, sps=sps)
    rx = Receiver(cfg)
    return bits, sym, pulse_shape(sym, rx.taps, sps), rx


@pytest.mark.parametrize("M", SUPPORTED_M)
def test_modulation_roundtrip_and_unit_energy(M):
    rng = np.random.default_rng(0)
    bits = rng.integers(0, 2, 6000 * bits_per_symbol(M))
    sym = modulate(bits, M)
    assert np.array_equal(demodulate(sym, M), bits)
    assert np.mean(np.abs(sym) ** 2) == pytest.approx(1.0, rel=0.03)


@pytest.mark.parametrize("M", [4, 16, 64])
def test_gray_coding_nearest_neighbours_differ_by_one_bit(M):
    k = bits_per_symbol(M)
    all_bits = ((np.arange(M)[:, None] >> np.arange(k - 1, -1, -1)) & 1).ravel()
    pts = modulate(all_bits, M)
    labels = all_bits.reshape(M, k)
    d = np.abs(pts[:, None] - pts[None, :])
    dmin = np.min(d[d > 1e-9])
    for i, j in zip(*np.where(np.isclose(d, dmin))):
        assert np.sum(labels[i] != labels[j]) == 1


def test_rrc_cascade_is_nyquist():
    sps, span = 8, 10
    h = rrc_taps(sps, 0.35, span)
    assert np.sum(h**2) == pytest.approx(1.0)
    rc = np.convolve(h, h)
    c = len(rc) // 2
    samples = rc[c % sps :: sps]
    peak = np.argmax(np.abs(samples))
    assert samples[peak] == pytest.approx(1.0, abs=1e-3)
    isi = np.delete(samples, peak)
    # Truncating the filter to `span` symbols leaves a small residue (~ -45 dB for span=10).
    assert np.max(np.abs(isi)) < 1e-2


def test_genie_receiver_noiseless_is_perfect():
    rng = np.random.default_rng(1)
    bits, sym, tx, rx = _burst(16, 2000, 8, rng)
    res = rx.process(tx, n_symbols=len(sym))
    assert np.array_equal(res.bits, bits)
    assert evm_db(res.symbols, sym) < -40


def test_awgn_gives_requested_esn0_after_matched_filter():
    rng = np.random.default_rng(2)
    _, sym, tx, rx = _burst(4, 20000, 8, rng)
    esn0_db = 12.0
    res = rx.process(awgn(tx, esn0_db, sps=8, rng=rng), n_symbols=len(sym))
    measured = -evm_db(res.symbols, sym)  # with Es = 1, EVM^2 = N0 / Es
    assert measured == pytest.approx(esn0_db, abs=0.2)


@pytest.mark.parametrize("M, ebn0_db", [(4, 6.0), (16, 10.0)])
def test_genie_ber_matches_theory(M, ebn0_db):
    rng = np.random.default_rng(3)
    bits, sym, tx, rx = _burst(M, 100_000, 4, rng)
    esn0_db = ebn0_db + 10 * np.log10(bits_per_symbol(M))
    res = rx.process(awgn(tx, esn0_db, sps=4, rng=rng), n_symbols=len(sym))
    assert ber(bits, res.bits) == pytest.approx(ber_theory(ebn0_db, M), rel=0.2)


def test_enabling_an_unwired_block_fails_loudly():
    with pytest.raises(NotImplementedError):
        Receiver(RxConfig(timing=True)).process(np.zeros(1000, complex), n_symbols=10)
