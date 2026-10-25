"""Known-answer tests for the W02 channel impairments.

They are written ahead of the code: implement a function in channel/impairments.py,
delete the matching ``@todo`` line, and run ``pytest``.
"""

import numpy as np
import pytest

from wireless_rx_dsp.channel import (
    fractional_delay,
    frequency_offset,
    multipath,
    prepend_silence,
    sample_rate_offset,
)

todo = pytest.mark.skip(reason="W02: not implemented yet")


@todo
def test_frequency_offset_rotates_at_the_right_rate():
    fs, f = 1e6, 1.2e3
    y = frequency_offset(np.ones(2000, complex), f, fs)
    step = np.angle(y[1:] * np.conj(y[:-1]))
    assert np.allclose(step, 2 * np.pi * f / fs)
    assert np.allclose(np.abs(y), 1.0)


@todo
@pytest.mark.parametrize("d", [3.0, 0.5, 2.25])
def test_fractional_delay_shifts_a_slow_tone(d):
    n = np.arange(4000)
    f0 = 0.01  # cycles per sample, well inside the passband
    x = np.exp(2j * np.pi * f0 * n)
    y = fractional_delay(x, d)
    assert len(y) == len(x)
    mid = slice(500, 3500)  # ignore filter edges
    assert np.allclose(y[mid], x[mid] * np.exp(-2j * np.pi * f0 * d), atol=1e-3)


@todo
def test_sample_rate_offset_stretches_the_signal():
    x = np.exp(2j * np.pi * 0.01 * np.arange(100_000))
    ppm = 100.0
    y = sample_rate_offset(x, ppm)
    assert abs(len(y) - len(x) * (1 + ppm * 1e-6)) <= 2


@todo
def test_multipath_impulse_response_is_the_taps():
    taps = np.array([1.0, 0.0, 0.4j, -0.2])
    x = np.zeros(50, complex)
    x[0] = 1.0
    y = multipath(x, taps)
    assert len(y) == len(x)
    assert np.allclose(y[: len(taps)], taps)
    assert np.allclose(y[len(taps) :], 0)


@todo
def test_prepend_silence():
    x = np.ones(100, complex)
    y = prepend_silence(x, 37)
    assert len(y) == 137
    assert np.all(y[:37] == 0) and np.array_equal(y[37:], x)
