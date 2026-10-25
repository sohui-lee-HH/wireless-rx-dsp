"""Wireless channel model: noise plus the impairments the receiver has to undo.

| Impairment                       | Undone by (rx)            | Week |
|----------------------------------|---------------------------|------|
| ``fractional_delay``, ``sample_rate_offset`` | ``rx.timing``  | W03  |
| ``frequency_offset``             | ``rx.carrier``            | W04  |
| unknown burst start (``prepend_silence``)   | ``rx.frame_sync`` | W05  |
| ``multipath``                    | ``rx.equalizer``          | W06  |
"""

from .awgn import awgn
from .impairments import (
    fractional_delay,
    frequency_offset,
    multipath,
    prepend_silence,
    sample_rate_offset,
)

__all__ = [
    "awgn",
    "frequency_offset",
    "fractional_delay",
    "sample_rate_offset",
    "multipath",
    "prepend_silence",
]
