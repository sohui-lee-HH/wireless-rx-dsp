"""The receiver as one object: ``Receiver(cfg).process(iq) -> RxResult``.

This is the public API. Project 3's test bench imports it as the device under test,
so keep the signature stable and put every new estimate into ``RxResult`` rather than
printing it.

Right now only the matched filter runs, with ideal (known) timing and no carrier or
frame recovery: the "genie" baseline. Its BER must match theory on an AWGN channel.
As W03-W06 land, switch each block on through ``RxConfig`` and the receiver should
stay on the theory curve with the matching impairment switched on.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..tx.pulse import rrc_taps
from ..tx.symbols import demodulate
from .matched_filter import matched_filter


@dataclass
class RxConfig:
    M: int = 4
    sps: int = 8
    rolloff: float = 0.35
    span: int = 10
    fs: float = 1.0e6
    # Blocks are switched on as they are implemented (W03-W06).
    timing: bool = False
    carrier: bool = False
    frame_sync: bool = False
    equalizer: str | None = None  # None | "lms" | "cma"


@dataclass
class RxResult:
    symbols: np.ndarray
    bits: np.ndarray
    # Estimates each block reports. Project 3 checks these against what it injected.
    cfo_hz: float | None = None
    timing_mu: np.ndarray | None = None
    frame_start: int | None = None
    eq_taps: np.ndarray | None = None
    info: dict = field(default_factory=dict)


class Receiver:
    def __init__(self, cfg: RxConfig | None = None):
        self.cfg = cfg or RxConfig()
        self.taps = rrc_taps(self.cfg.sps, self.cfg.rolloff, self.cfg.span)

    def process(self, iq: np.ndarray, n_symbols: int) -> RxResult:
        """Recover ``n_symbols`` symbols and their bits from a received burst."""
        c = self.cfg
        for flag, week in ((c.timing, "W03"), (c.carrier, "W04"), (c.frame_sync, "W05"), (c.equalizer, "W06")):
            if flag:
                raise NotImplementedError(f"{week} block enabled in RxConfig but not wired into Receiver yet")

        y = matched_filter(iq, self.taps)
        delay = len(self.taps) - 1  # genie timing: TX + RX filter group delay
        symbols = y[delay : delay + n_symbols * c.sps : c.sps]
        if len(symbols) < n_symbols:
            raise ValueError("received burst is shorter than n_symbols")

        return RxResult(symbols=symbols, bits=demodulate(symbols, c.M), info={"mode": "genie baseline"})
