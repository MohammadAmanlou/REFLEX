# REFLEX 7.0 — Topology–Incentive Frontier

Research owner: Mohammad Amanlou. Study status: restricted mathematical research working draft — **NOT** a peer-reviewed paper, top-conference submission, historical novelty certification, full strategic implementation, or LLM evaluation.

Repository: https://github.com/MohammadAmanlou/REFLEX

## What is proved (in the restricted binary model)

1. The exact minimum owner-weight to force a **wrong** $k$-explanation certificate has a constructive combinatorial formulation, supported by an independently exhaustive transcript oracle.
2. With unit weights this reduces to $\tau_{P}-k$ when $\tau_P>2k$.
3. Abstention can be strictly cheaper than false certification, so incentives must protect both failure modes.
4. A **conditional** coalition-deterrence proposition applies only if dishonest report modifications are independently detectable with an attributed owner-specific audit, deposits are genuinely collectible, truthful logging has zero cost, and all coalition gains from changed outcomes are bounded. No claim that all equilibria are truthful.
5. A fixed-network, wrong-certificate-only covering LP produces a synthetic optimum for three owner-disjoint triangles; full dynamic, all-outcome synthesis remains open.

## Reproduce

```bash
python -m pip install numpy scipy
python src/reflex7_economic_frontier.py
```

The script runs standard-library exact tests plus a small SciPy HiGHS LP. Current output is recorded at `results/reflex7_stdout.txt`. The narrative with proofs and limitations is `papers/REFLEX7_Topology_Incentive_Frontier.pdf`, with editable TeX source alongside.

## Critical assumptions

- Trusted true principal-to-delegate identity registry; sensitivity vector $b$ correctly authenticated.
- Error-free measurement semantics for noncompromised principals and within-episode consistent hidden offsets.
- For the economic theorem ONLY: owner-attributable tampering, a verified raw measurement log, secret randomized post-commit audit and enforceable penalties.
- An LLM that signs a fabricated raw measurement does **not** satisfy that last assumption.

**Research blockers**: Noncircular provenance; general all-equilibria implementation; scalable joint graph-and-payment synthesis; noisy correlated evidence; empirical LLM-agent benchmarks and comparisons against contemporary baselines; independent proof and novelty audit.