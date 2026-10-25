# wireless-rx-dsp

**A digital wireless receiver built from scratch in Python (timing, carrier, frame sync, equalisation), extended to OFDM, plus an FMCW automotive-radar processing chain.**

<!-- HERO FIGURE (add in W06): four constellations side by side —
     raw received → after timing recovery → after carrier recovery → after equaliser -->

[![tests](https://github.com/sohui-lee-HH/wireless-rx-dsp/actions/workflows/ci.yml/badge.svg)](https://github.com/sohui-lee-HH/wireless-rx-dsp/actions/workflows/ci.yml)

## What's inside

Every impairment the channel adds is removed by one receiver block, and each block has a known-answer test.

| Channel impairment | Receiver block | Result | Status |
|---|---|---|---|
| Noise (AWGN) | Matched filter, genie timing | BER on the theory curve | ✅ |
| Timing offset, sample-rate drift | Gardner timing recovery | Eye re-opened, drift tracked | ⬜ W03 |
| Carrier frequency offset | Coarse FFT estimate + Costas loop | Constellation de-rotated | ⬜ W04 |
| Unknown burst start | Zadoff-Chu preamble + correlator | Frame located | ⬜ W05 |
| Multipath (ISI) | LMS and blind CMA equalisers | ISI removed | ⬜ W06 |
| Frequency-selective channel | OFDM: CP sync, pilot channel estimation | EVM per subcarrier | ⬜ W07 |
| — | FMCW radar: range-Doppler, CA-CFAR, angle FFT | Targets detected | ⬜ W08 |

## Results

### Baseline: genie receiver vs theory

![BER vs Eb/N0](docs/figures/baseline_ber.png)

With ideal synchronisation the simulated BER sits on the theoretical curves for QPSK, 16-QAM and 64-QAM. This is the reference: each later block is judged by how closely it brings an impaired signal back to this curve.

<!-- W05: BER with all impairments on vs theory, and the implementation loss in dB -->
<!-- W07: OFDM EVM per subcarrier on a multipath channel -->
<!-- W08: range-Doppler map with CFAR detections -->

## Architecture

```mermaid
flowchart LR
    B[bits] --> TX[modulate + RRC]
    TX --> CH[channel: delay, SRO, CFO, multipath, AWGN]
    CH --> MF[matched filter]
    MF --> TR[timing recovery]
    TR --> CR[carrier recovery]
    CR --> FS[frame sync]
    FS --> EQ[equaliser]
    EQ --> D[bits, EVM, BER]
```

The whole receiver is one object, so other code (including the test bench in Project 3) can drive it:

```python
from wireless_rx_dsp import Receiver, RxConfig

rx = Receiver(RxConfig(M=16, sps=8))
result = rx.process(iq, n_symbols=1000)   # result.bits, result.symbols, result.cfo_hz, ...
```

## Receiver specification

[`docs/receiver_spec.md`](docs/receiver_spec.md) states the receiver's requirements (sensitivity, EVM, BER, offset ranges). They are verified automatically in Project 3, [rf-test-bench](https://github.com/sohui-lee-HH/rf-test-bench). <!-- link once it exists -->

## Quickstart

```bash
git clone https://github.com/sohui-lee-HH/wireless-rx-dsp.git
cd wireless-rx-dsp
conda env create -f environment.yml
conda activate wrx
pytest
python experiments/00_baseline_ber.py
```

Or with plain pip: `pip install -e ".[dev]"`.

## Repository layout

```
src/wireless_rx_dsp/
├── tx/          constellation mapping, RRC pulse shaping
├── channel/     AWGN and impairments
├── rx/          matched filter, timing, carrier, frame sync, equaliser, Receiver
├── ofdm/        OFDM modem, CP synchronisation, channel estimation
├── radar/       FMCW simulation, range-Doppler, CFAR, angle estimation
└── metrics.py   BER, EVM, theoretical curves
experiments/     one script per figure in this README
tests/           known-answer tests for every block
docs/            receiver spec, figures
```

## Related work

Builds on [iqmodrec](https://github.com/sohui-lee-HH/iqmodrec), my CNN modulation classifier, and reuses its modulators.

## Design notes and limitations

<!-- Fill in as you go: choices you made (loop bandwidths, why Gardner over Mueller-Müller,
     why a ZC preamble), what you measured, and what is out of scope (e.g. no channel coding). -->

## License

MIT
