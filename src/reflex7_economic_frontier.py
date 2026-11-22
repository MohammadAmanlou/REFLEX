"""REFLEX 7.0: reproducible restricted-model strategic attack-cost frontier.

This extends REFLEX-P's *conditional* robust decision theorem with an exact
weighted minimum cost of forcing a WRONG certificate using owner-controlled
reports, and a conditional coalition-deterrence result. This is NOT a general
incentive-compatible agent protocol, a historical novelty proof, or an LLM test.

Run from repository root:
    python src/reflex7_economic_frontier.py
Python >= 3.10, standard library only.
"""
from itertools import combinations
from random import Random


def subsets(labels):
    labels = tuple(labels)
    for j in range(len(labels) + 1):
        yield from combinations(labels, j)


def compromised_edges(edges, owners, subset):
    S = set(subset)
    return sum(1 << j for j, (u, v, b, c) in enumerate(edges)
               if owners[u] in S or owners[v] in S)


def consistent(n, edges, owners, deleted, labels):
    """Find s such that s_u XOR s_v = labels[e] on undeleted edges.

    Return one offset assignment, or None when inconsistent.
    """
    deleted = set(deleted)
    graph = [[] for _ in range(n)]
    for j, (u, v, _b, _cost) in enumerate(edges):
        if owners[u] in deleted or owners[v] in deleted:
            continue
        graph[u].append((v, (labels >> j) & 1))
        graph[v].append((u, (labels >> j) & 1))
    s = [None] * n
    for r in range(n):
        if s[r] is not None:
            continue
        s[r] = 0
        stack = [r]
        while stack:
            u = stack.pop()
            for v, parity in graph[u]:
                val = s[u] ^ parity
                if s[v] is None:
                    s[v] = val
                    stack.append(v)
                elif s[v] != val:
                    return None
    return s


def b_mask(edges):
    return sum((b & 1) << j for j, (u, v, b, c) in enumerate(edges))


def tau(n, edges, owners):
    principals = tuple(sorted(set(owners), key=str))
    b = b_mask(edges)
    for S in subsets(principals):
        if consistent(n, edges, owners, S, b) is not None:
            return len(S), tuple(S)
    raise AssertionError('all deleted should be feasible')


def explainable(n, edges, owners, k, y, h):
    principal_labels = tuple(sorted(set(owners), key=str))
    rhs = y ^ (b_mask(edges) if h else 0)
    for j in range(min(k, len(principal_labels)) + 1):
        for W in combinations(principal_labels, j):
            if consistent(n, edges, owners, W, rhs) is not None:
                return True
    return False


def certificate(n, edges, owners, k, y):
    feasible = [h for h in (0, 1) if explainable(n, edges, owners, k, y, h)]
    return feasible[0] if len(feasible) == 1 else None


def weighted_wrong_attack(n, edges, owners, k, owner_costs):
    """Theorem: exact min expected penalty of forcing *false certification*.

    Enumerate attacking owner set T and a budget-k decoder-explanation set W,
    requiring a balanced signed graph after removing T union W. For tau>2k,
    this is the exact weighted min attack cost, not merely a lower bound.
    """
    t, _ = tau(n, edges, owners)
    if t <= 2 * k:
        raise ValueError('requires tau > 2k (truth uniquely certified at baseline)')
    principals = tuple(sorted(set(owners), key=str))
    b = b_mask(edges)
    best = (float('inf'), None, None)
    for T in subsets(principals):
        cost = sum(owner_costs[p] for p in T)
        if cost >= best[0]:
            continue
        remaining = tuple(p for p in principals if p not in T)
        for j in range(min(k, len(remaining)) + 1):
            for W in combinations(remaining, j):
                if consistent(n, edges, owners, T + W, b) is not None:
                    best = (cost, T, W)
                    break
            if cost == best[0]:
                break
    return best


def construct_false_certificate(n, edges, owners, k, T, W):
    """Construct tampered transcript y from actual h=0,s=0 that certifies h=1."""
    b = b_mask(edges)
    s = consistent(n, edges, owners, set(T) | set(W), b)
    assert s is not None
    dx = sum((s[u] ^ s[v]) << j for j, (u, v, _b, _c) in enumerate(edges))
    mismatch = b ^ dx
    eta_true = mismatch & compromised_edges(edges, owners, T)
    assert mismatch & ~compromised_edges(edges, owners, set(T) | set(W)) == 0
    y = eta_true  # true h=0 and true s=0
    assert certificate(n, edges, owners, k, y) == 1
    return y, eta_true


def exhaustive_wrong_attack(n, edges, owners, k, costs):
    """Independent exponential transcript oracle for tiny graphs.

    Assumes honest h=0 and all honest offsets zero; nuisance offsets can be
    translated away because the decoder is invariant under incidence shifts.
    """
    principals = tuple(sorted(set(owners), key=str))
    best = float('inf')
    for y in range(1 << len(edges)):
        if certificate(n, edges, owners, k, y) != 1:
            continue
        for T in subsets(principals):
            if y & ~compromised_edges(edges, owners, T) == 0:
                best = min(best, sum(costs[p] for p in T))
    return best


def independent_triangles(count=3):
    edges = []
    for i in range(count):
        a = 3 * i
        edges.extend([(a, a + 1, 1, 1), (a + 1, a + 2, 0, 1), (a + 2, a, 0, 1)])
    return 3 * count, edges, list(range(3 * count))


def test_three_triangles():
    n, edges, owners = independent_triangles(3)
    k = 1
    t, _ = tau(n, edges, owners)
    assert t == 3
    costs = dict(enumerate([2, 6, 6, 3, 6, 6, 7, 9, 9]))
    val, T, W = weighted_wrong_attack(n, edges, owners, k, costs)
    brute = exhaustive_wrong_attack(n, edges, owners, k, costs)
    assert val == brute == 5, (val, brute, T, W)
    y, error = construct_false_certificate(n, edges, owners, k, T, W)
    assert certificate(n, edges, owners, k, 0) == 0
    print(f'PASS: k=1, tau={t}, heterogeneous exact wrong-certificate cost={val}; '
          f'attacker owners={T}; decoder-explanation owners={W}; forged transcript={y:09b}')

    homogeneous = {p: 1 for p in owners}
    hcost, ht, hw = weighted_wrong_attack(n, edges, owners, k, homogeneous)
    assert hcost == t - k == 2
    print(f'PASS: homogeneous tight threshold tau-k={t-k}, witnessed by attacker owners={ht}')


def test_abstention_different_from_wrong():
    n, edges, owners = independent_triangles(4)
    k = 1
    assert tau(n, edges, owners)[0] == 4
    # A single owner flips the parity of one entire triangle, with all other reports intact.
    # Two compromised owners, one from each of two triangles, create parity 2:2.
    attack_mask = (1 << 0) | (1 << 3)
    assert certificate(n, edges, owners, k, attack_mask) is None
    for i in range(len(owners)):
        inc = compromised_edges(edges, owners, [i])
        sub = inc
        while True:
            assert certificate(n, edges, owners, k, sub) == 0
            if sub == 0:
                break
            sub = (sub - 1) & inc
    assert weighted_wrong_attack(n, edges, owners, k, {p: 1 for p in owners})[0] == 3
    disruption = min_disruption_attack(n, edges, owners, k, {p: 1 for p in owners})
    assert disruption[0] == 2 and disruption[3] is None, disruption
    print('PASS: four owner-independent triangles, k=1: abstention by 2 owners, '
          'false certification requires >=3 owners; distinct strategic security thresholds')


def test_random_exhaustive(seed=20261122, iterations=600):
    r = Random(seed)
    checked = 0
    for _ in range(iterations):
        n = r.randint(3, 5)
        all_edges = list(combinations(range(n), 2))
        r.shuffle(all_edges)
        m = r.randint(2, min(7, len(all_edges)))
        edges = [(u, v, r.randint(0, 1), 1) for u, v in all_edges[:m]]
        owners = [r.randrange(n) for _ in range(n)]
        k = r.randint(0, 1)
        t, _ = tau(n, edges, owners)
        if t <= 2 * k:
            continue
        costs = {p: r.randint(1, 7) for p in set(owners)}
        a, T, W = weighted_wrong_attack(n, edges, owners, k, costs)
        b = exhaustive_wrong_attack(n, edges, owners, k, costs)
        assert a == b, (n, edges, owners, k, costs, a, b)
        y, e = construct_false_certificate(n, edges, owners, k, T, W)
        assert certificate(n, edges, owners, k, y) == 1
        checked += 1
    assert checked >= 10
    print(f'PASS: {checked} eligible random owner-labelled graph instances, '
          'exact weighted theorem = independent exhaustive transcript search')


def test_deterrence_certificate():
    n, edges, owners = independent_triangles(3)
    k, benefit, bond = 1, 4.0, 5.0
    q = 0.5
    expected_penalty = {p: q * bond for p in owners}
    mu, _, _ = weighted_wrong_attack(n, edges, owners, k, expected_penalty)
    assert abs(mu - 5.0) < 1e-10 and mu > benefit
    print(f'PASS: conditional wrong-decision deterrence: min expected slashing={mu:.1f} '
          f'> maximum transferable wrong-outcome gain={benefit:.1f}. '
          'Assumes independent audit attribution and enforceable bonds.')





def min_disruption_attack(n, edges, owners, k, costs):
    """Exact min cost to change outcome from true h=0, including abstention.

    Caution: exponentially expensive; for binary signed-edge transcripts only.
    """
    principals = tuple(sorted(set(owners), key=str))
    candidates = sorted(subsets(principals),
                        key=lambda T: (sum(costs[p] for p in T), len(T)))
    for T in candidates:
        inc = compromised_edges(edges, owners, T)
        eta = inc
        while True:
            outcome = certificate(n, edges, owners, k, eta)
            if outcome != 0:
                return (sum(costs[p] for p in T), T, eta, outcome)
            if eta == 0:
                break
            eta = (eta - 1) & inc
    return (float('inf'), None, None, None)


def minimal_attack_coalitions(n, edges, owners, k):
    """Inclusion-minimal attacking owner sets allowing a false k-certificate.

    This is an exponential exact separation baseline. It is NOT scalable.
    """
    principals = tuple(sorted(set(owners), key=str))
    b = b_mask(edges)
    eligible = []
    for T in subsets(principals):
        remaining = tuple(p for p in principals if p not in T)
        found = False
        for j in range(min(k, len(remaining)) + 1):
            for W in combinations(remaining, j):
                if consistent(n, edges, owners, T + W, b) is not None:
                    found = True
                    break
            if found:
                break
        if found and not any(set(R).issubset(T) for R in eligible):
            eligible.append(T)
    return eligible


def min_audit_policy_lp(n, edges, owners, k, benefit, bond_by_owner,
                        audit_cost_by_owner, margin=0.1):
    """Solve the fixed-topology audit frequency covering LP for tiny models.

    For any attack set T that can force a false certificate, require
        sum_{p in T} (audit_probability[p] * bond[p]) >= benefit + margin.
    Audit audit attribution, affordability, and unforgeable raw logs are ASSUMED.
    Even a feasible LP does NOT establish general all-equilibria truthfulness.
    """
    from scipy.optimize import linprog
    principals = tuple(sorted(set(owners), key=str))
    witnesses = minimal_attack_coalitions(n, edges, owners, k)
    assert witnesses
    A_ub = [[-bond_by_owner[p] if p in T else 0.0 for p in principals]
            for T in witnesses]
    b_ub = [-(benefit + margin)] * len(witnesses)
    result = linprog([audit_cost_by_owner[p] for p in principals],
                     A_ub=A_ub, b_ub=b_ub,
                     bounds=[(0.0, 1.0)] * len(principals), method='highs')
    if not result.success:
        return None, len(witnesses)
    q = dict(zip(principals, map(float, result.x)))
    pen = {p: q[p] * bond_by_owner[p] for p in principals}
    mu, _, _ = weighted_wrong_attack(n, edges, owners, k, pen)
    assert mu + 1e-7 >= benefit + margin, (mu, benefit, margin)
    return (q, float(result.fun), float(mu)), len(witnesses)


def test_audit_synthesis_lp():
    n, edges, owners = independent_triangles(3)
    k, benefit = 1, 4.0
    bond = {p: 5.0 for p in owners}
    audit_cost = {p: 1.0 for p in owners}
    optimum, constraints = min_audit_policy_lp(n, edges, owners, k,
                                                benefit, bond, audit_cost, 0.1)
    assert optimum is not None
    q, obj, mu = optimum
    assert constraints == 27, constraints
    # Symmetry gives q_p=(benefit+margin)/(2*bond) = 0.41 for all 9 owners.
    assert abs(obj - 9 * 4.1 / 10) < 1e-6, (obj, q)
    assert abs(mu - 4.1) < 1e-6, (mu, q)
    nu = min_disruption_attack(n, edges, owners, k, {p: q[p] * bond[p] for p in owners})
    assert abs(nu[0] - mu) < 1e-6, (nu, mu)
    print(f'PASS: fixed-topology audit LP, {constraints} minimal attacking coalitions; '
          f'optimal sum audit probabilities={obj:.3f}; min expected attack penalty={mu:.3f}; '
          f'all probabilities within [0,1]')


def main():
    test_three_triangles()
    test_abstention_different_from_wrong()
    test_random_exhaustive()
    test_deterrence_certificate()
    test_audit_synthesis_lp()
    print('All REFLEX-7 *restricted-model* checks passed; no peer-reviewed novelty claim.')


if __name__ == '__main__':
    main()