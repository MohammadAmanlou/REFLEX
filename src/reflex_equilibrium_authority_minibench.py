"""REFLEX restricted-model sanity checks (22 November 2026).

Illustrative theoretical check only—not evidence of publication novelty.
Requires numpy and scipy.
Run: python reflex_equilibrium_authority_minibench.py
"""
import math
from itertools import combinations
import numpy as np
from scipy.stats import binom, norm

def separated_binary_observation_sets(null_set, alt_set):
    a, b = null_set
    c, d = alt_set
    assert 0 <= a <= b <= 1 and 0 <= c <= d <= 1
    return b < c or d < a

def simple_majority_errors(n, p0, p1):
    # Decision H1 iff the observed count > n/2; ties assigned H0.
    return float(binom.sf(n // 2, n, p0)), float(binom.cdf(n // 2, n, p1))

def main():
    # Same strategic cheap-talk report in both worlds: no statistical distinction.
    assert not separated_binary_observation_sets((1, 1), (1, 1))
    print("Unverifiable report: identical laws, worst-case error >= 1/2")

    # Under authorized independent audit, the equilibrium-induced laws may
    # be nonstationary/adaptive, yet stay inside the following Bernoulli sets.
    null_set = (.15, .25)
    alt_set = (.75, .85)
    assert separated_binary_observation_sets(null_set, alt_set)
    gamma = alt_set[0] - null_set[1]
    n = math.ceil(2*math.log(1/.05)/gamma**2)
    assert n == 24
    e0, e1 = simple_majority_errors(n, .25, .75)
    assert max(e0, e1) < .05
    print("Audited laws:", null_set, "versus", alt_set)
    print("Separating gap:", gamma, "Hoeffding sufficient n:", n)
    print("Exact fixed-i.i.d. endpoint error probabilities:", round(e0, 8), round(e1, 8))

    # Idealized known-diagnostic setting: m equipriced permissions,
    # just one is relevant to the revealed task type.
    for m in (2, 4, 8, 16):
        print(f"m={m}: ex ante cost {m}, diagnosis-adaptive cost 1, ratio {m}:1")

    # Three-way interaction invisible to tests restricted to <=2 agents.
    subsets = [s for r in range(4) for s in combinations(range(3), r)]
    queries = [t for t in subsets if len(t) <= 2]
    design = np.array(
        [[int(set(s).issubset(t)) for s in subsets] for t in queries],
        dtype=int,
    )
    assert np.linalg.matrix_rank(design) == 7 and len(subsets) == 8
    print("Partial interaction-design rank:", np.linalg.matrix_rank(design), "of 8")
    print("PASS. No claim of empirical LLM superiority or novel publication.")

if __name__ == "__main__":
    main()
