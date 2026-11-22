# Scientific scope and reproducibility statement

## Sources and provenance

The repository stores the locally available REFLEX computational scripts and technical reports from the current project: one early equilibrium/authority mini-benchmark, one REFLEX-T topology prototype, and the REFLEX-P/6.0 principal-aware verifier. The scripts are deterministic (explicit seeds where applicable) and the original output transcripts are included. The reports' reference links were updated to point to this exact GitHub repository. Prior-stage conceptual discussions without a surviving standalone code artifact are **not falsely represented as implemented experiments**.

## What was verified

The scripts were executed afresh on 22 November 2026 using Python 3.13.5 with local numerical dependencies. All built-in assertions passed. Exact small-instance enumeration supports the restricted model claims. These tests are author-level sanity checks, not external replication.

## What is not claimed

- No actual LLM-agent experiment, user study, or robustness comparison against modern agent audit baselines was performed by these scripts.
- No mechanism is yet proven incentive-compatible in arbitrary Bayesian or extensive-form games under collusion and delegation.
- Results that employ signed graph parity, coset codes, odd-cycle transversals, and standard hypothesis tests overlap well-established literature. Novel publication priority has not been demonstrated.
- No manuscript or research proposal was submitted to a conference or professor through this repository operation.
- No GitHub Actions run is claimed passed until the corresponding workflow execution actually finishes.

## How to reproduce

1. Install dependencies from `requirements.txt` under Python 3.10+.
2. Execute `bash reproduce.sh`.
3. Inspect the model assumptions and proofs in `papers/`.
4. When independently assessing novelty, compare theorem statements and assumptions directly against relevant group synchronization, coding theory, group feedback vertex set, optimal adversarial auditing, and delegation-game literature.
