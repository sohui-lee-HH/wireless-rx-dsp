"""wireless-rx-dsp: a digital receiver built block by block, plus an FMCW radar chain.

Signal path::

    bits -> tx (symbols, pulse shaping) -> channel (impairments) -> rx (Receiver) -> bits

Each impairment in ``channel`` is undone by one block in ``rx``.
"""

from .rx.receiver import Receiver, RxConfig, RxResult

__all__ = ["Receiver", "RxConfig", "RxResult"]
__version__ = "0.1.0"
