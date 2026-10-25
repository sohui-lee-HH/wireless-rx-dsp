# Receiver requirements specification

Filled in at the end of W07 from measured results. Project 3 turns every row into an
automated test with these limits (verification matrix), so each requirement needs a
number, a condition and a way to measure it.

| ID | Requirement | Limit | Conditions | Measured by |
|----|-------------|-------|------------|-------------|
| RX-01 | BER, QPSK | ≤ 1e-3 | Eb/N0 = TBD dB, AWGN | `metrics.ber` |
| RX-02 | Implementation loss vs theory at BER 1e-3 | ≤ TBD dB | all impairments on | BER sweep |
| RX-03 | EVM, 16-QAM | ≤ TBD dB | Es/N0 = TBD dB | `metrics.evm_db` |
| RX-04 | Frequency-offset acquisition range | ± TBD kHz | fs = TBD | sweep CFO |
| RX-05 | Sample-rate offset tolerance | ± TBD ppm | | sweep ppm |
| RX-06 | Frame detection probability | ≥ TBD % | Es/N0 = TBD dB | 1000 bursts |
| RX-07 | False alarm rate | ≤ TBD | noise only | 1000 bursts |
| RX-08 | Sensitivity (input power for BER 1e-3) | ≤ TBD dBm | NF = TBD dB (from Project 3 front end) | power sweep |
