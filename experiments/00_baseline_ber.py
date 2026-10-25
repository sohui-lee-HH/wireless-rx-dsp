"""Genie-receiver BER vs Eb/N0 on AWGN, against theory.

This is the reference every later experiment is compared to: with an impairment
switched on and its receiver block enabled, the curve should land back on this one.

Run from the repo root:  python experiments/00_baseline_ber.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from wireless_rx_dsp import Receiver, RxConfig
from wireless_rx_dsp.channel import awgn
from wireless_rx_dsp.metrics import ber, ber_theory
from wireless_rx_dsp.tx import bits_per_symbol, modulate, pulse_shape

OUT = Path(__file__).resolve().parents[1] / "docs" / "figures" / "baseline_ber.png"
SPS = 4
TARGET_ERRORS = 200
MAX_BITS = 4_000_000


def simulate(M: int, ebn0_db: float, rng: np.random.Generator) -> float:
    rx = Receiver(RxConfig(M=M, sps=SPS))
    k = bits_per_symbol(M)
    esn0_db = ebn0_db + 10 * np.log10(k)
    errors = n_bits = 0
    while errors < TARGET_ERRORS and n_bits < MAX_BITS:
        bits = rng.integers(0, 2, 50_000 * k)
        sym = modulate(bits, M)
        tx = pulse_shape(sym, rx.taps, SPS)
        res = rx.process(awgn(tx, esn0_db, sps=SPS, rng=rng), n_symbols=len(sym))
        errors += int(round(ber(bits, res.bits) * bits.size))
        n_bits += bits.size
    return errors / n_bits


def main() -> None:
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    for M, name, ebn0 in [(4, "QPSK", np.arange(0, 11)), (16, "16-QAM", np.arange(0, 15)), (64, "64-QAM", np.arange(4, 19))]:
        sim = np.array([simulate(M, e, rng) for e in ebn0])
        fine = np.linspace(ebn0[0], ebn0[-1], 200)
        (line,) = ax.semilogy(fine, ber_theory(fine, M), lw=1.2, label=f"{name} theory")
        keep = sim > 0
        ax.semilogy(ebn0[keep], sim[keep], "o", ms=4, color=line.get_color(), label=f"{name} simulated")
        print(name, " ".join(f"{e:>2}dB:{b:.2e}" for e, b in zip(ebn0, sim)))

    ax.set_xlabel("Eb/N0 (dB)")
    ax.set_ylabel("Bit error rate")
    ax.set_ylim(1e-5, 0.5)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8, ncol=2)
    ax.set_title("Genie receiver on AWGN vs theory (RRC, beta = 0.35)")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    print(f"saved {OUT}")


if __name__ == "__main__":
    main()
