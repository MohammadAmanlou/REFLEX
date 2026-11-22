# REFLEX-T / Research package (22 November 2026)

## Status
**Working, non-peer-reviewed scientific research note; NOT ready for submission to AAMAS, IJCAI, AAAI, NeurIPS, ICLR, or ICML.** This package does not establish that its mathematical claims are historically novel. It makes no claim of supervisor endorsement or funding.

## Files
- `REFLEX_Audit_Topology_Research_Draft.pdf` — six-page technical research note, model, theorems, proofs, programmatic results, direct prior-art positioning, limitations, open contribution.
- `REFLEX_Audit_Topology_Research_Draft.tex` — editable LaTeX source (compile twice with `pdflatex`).
- `reflex_audit_topology_prototype.py` — Python standard-library-only baseline; tests parity identifiability, exact Hamming-coset distances, minimum odd-sensitive cycles against brute force, edge-disjoint cycle certificates and exact noisy decoder metrics.

## Run
```bash
python3 reflex_audit_topology_prototype.py
pdflatex -interaction=nonstopmode REFLEX_Audit_Topology_Research_Draft.tex
pdflatex -interaction=nonstopmode REFLEX_Audit_Topology_Research_Draft.tex
```

## Key model
`y_e = s_u XOR s_v XOR b_e h XOR eta_e` with consistent per-node strategic conventions, externally verifiable binary edge sensitivity, and a bounded number of adversarial edge errors.

## Provable restricted results
1. Noiseless identifiability iff a parity-sensitive cycle exists.
2. Unique decoding under up to `t` edge corruptions iff `d*=min_s wt(b XOR D s)>2t`.
3. Cheapest noiseless witness is a minimum-cost parity-sensitive cycle, polynomial-time.
4. Computing exact worst-case corruption robustness on arbitrary graphs subsumes MaxCut (NP-hard).
5. `2t+1` edge-disjoint parity-sensitive cycles give an elementary majority-based corruption certificate.
6. Strict reporting incentives are sufficient in a restricted one-reporter-per-edge audit model when `q_e F_e >= g_e + kappa`.

## IMPORTANT scope limits
The listed mathematical constructions derive substantially from prior signed-graph balance, synchronization, error correction, and elementary auditing. They are not by themselves a high-novelty conference contribution. To reach publication readiness, one must supply and prove a truly new strategic multi-principal mechanism result, reproduce relevant state-of-the-art baselines, and complete genuine benchmark experiments. Edge sensitivity `b_e` and node convention consistency must be independently justified, not assumed by assigning favorable numbers.
