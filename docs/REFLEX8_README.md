# REFLEX 8.0 — Refutable Certificates without a State Oracle

**Repository:** https://github.com/MohammadAmanlou/REFLEX  
**Status:** Exploratory mathematical working paper (22 November 2026); not peer reviewed and not a conference submission.

## Main contribution (scope limited)

For the owner-labelled binary audit model `y_e = s_u XOR s_v XOR b_e*h XOR eta_e` with at most `k` corrupted authentic principals and decision-sensitive odd cycles, the exact conditions are:

- `tau <= k`: no transcript-based rule can be both complete on uncorrupted data and sound under `k` corruptions.
- `k < tau <= 2k`: correct-or-abstain is achievable; forced correct recovery is impossible.
- `tau > 2k`: uniformly correct recovery is achievable.

An incentive-controlled challenge subgame makes **false finalization impossible in all its Nash equilibria** when an uncompromised rational custodian has a verifiable refutation and its guaranteed bounty exceeds effort costs plus any bounded countervailing benefit. The verifier checks a signed cycle-parity contradiction; it does not know the hidden binary state. General strategic reporting without bounded corruption, credible authenticated receipts, and bounded outside incentives is **not solved**.

A second theorem uses a custody-aware witness cut `lambda_A` for the case where only designated authentic owners can independently assemble valid evidence. An exact small-instance weighted custody-set-cover baseline is implemented.

## Files

- `papers/REFLEX8_No_Oracle_Certification.pdf`: five-page note with definitions, proofs, examples, limits and sources.
- `papers/REFLEX8_No_Oracle_Certification.tex`: LaTeX source.
- `src/reflex8_refutable_certification.py`: dependency-free, deterministic formal sanity checks.
- `results/reflex8_stdout.txt`: captured output from the code.

## Reproduction

Requires Python 3.10 or newer (no external packages):

```bash
python src/reflex8_refutable_certification.py
```

## What the script checks

- 180 seeded small random owner-labelled signed graphs, exhaustively enumerating all valid transcripts under bounded corruptions.
- Exact one-sided and two-sided transcript intersection conditions (`tau>k` and `tau>2k`).
- The six-owner, two-triangle **middle regime**, with 32 ambiguous attacked transcripts and zero false unanimous-cycle certifications.
- Three independent odd cycles, whose owner transversal equals 3.
- Counterexample: same measurement graph, different custody grants, `lambda_A=1` versus `lambda_A=2`.
- An exact four-grant custody optimization with minimum toy cost 2.2.
- Exact Nash enumeration of a bounded-payoff challenge game, including a low-bounty failure example.

All evaluations are on synthetic binary models, **not** LLMs, users, human preferences, or top-tier peer-review benchmarks. Classical coding, signed graph, evidence implementation, fraud-proof, and peer-prediction research already cover important parts of these ideas; historical originality is unverified.
