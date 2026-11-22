"""REFLEX-6: principal-aware audit robustness, exact small-instance verifier.

Research status: a restricted structural model, not peer-reviewed novelty.
Dependency-free Python 3.9+; tests and small numerical results are reproducible.

For graph edges (u,v,b,cost), a principal-label array owner[v], and
hypothesis h in GF(2), reports follow y_e = s_u ^ s_v ^ (b_e & h) ^ eta_e.
Up to k PRINCIPALS (rather than k edges or k delegate vertices) may corrupt
all edge reports incident to ANY delegate belonging to those principals.
"""
from itertools import combinations
from random import Random


def incident_mask(edges, owner, compromised):
    bad = set(compromised)
    return sum(1 << i for i, (u, v, _b, _c) in enumerate(edges)
               if owner[u] in bad or owner[v] in bad)


def has_b_odd_cycle(n, edges, selected=None, deleted_principals=(), owner=None):
    """BFS signed-balance consistency: True iff some b-odd cycle survives."""
    deleted = set(deleted_principals)
    if selected is None:
        selected = (1 << len(edges)) - 1
    graph = [[] for _ in range(n)]
    for j, (u, v, b, _cost) in enumerate(edges):
        if not (selected >> j) & 1:
            continue
        if owner is not None and (owner[u] in deleted or owner[v] in deleted):
            continue
        graph[u].append((v, b))
        graph[v].append((u, b))
    style = [None] * n
    for r in range(n):
        if style[r] is not None:
            continue
        style[r] = 0
        stack = [r]
        while stack:
            u = stack.pop()
            for v, b in graph[u]:
                candidate = style[u] ^ b
                if style[v] is None:
                    style[v] = candidate
                    stack.append(v)
                elif style[v] != candidate:
                    return True
    return False


def owner_transversal(n, edges, owner, selected=None):
    """Exact minimum number of distinct principals to remove to destroy every b-odd cycle."""
    labels = tuple(sorted(set(owner), key=str))
    for j in range(len(labels) + 1):
        for S in combinations(labels, j):
            if not has_b_odd_cycle(n, edges, selected, S, owner):
                return j, S
    raise AssertionError('Deleting all owners must make the graph balanced')


def certified_for_k(n, edges, owner, k, selected=None):
    tau, witness = owner_transversal(n, edges, owner, selected)
    return (tau > 2 * k), tau, witness


def report(n, edges, h, style_bits, error_bits=0):
    obs = 0
    for i, (u, v, b, _c) in enumerate(edges):
        bit = ((style_bits >> u) & 1) ^ ((style_bits >> v) & 1) ^ (b & h) ^ ((error_bits >> i) & 1)
        obs |= bit << i
    return obs


def consistent_on_intact_edges(n, edges, owner, h, observed, bad_owners, selected=None):
    """Checks existence of node offsets on the edges not controlled by bad owners."""
    if selected is None:
        selected = (1 << len(edges)) - 1
    remaining = []
    disabled = incident_mask(edges, owner, bad_owners)
    for i, (u, v, b, cost) in enumerate(edges):
        if ((selected >> i) & 1) and not ((disabled >> i) & 1):
            remaining.append((u, v, ((observed >> i) & 1) ^ (b & h), cost))
    # consistency <=> no odd cycle in resulting residual signed graph
    return not has_b_odd_cycle(n, remaining)


def plausible_hypotheses(n, edges, owner, k, observed, selected=None):
    labels = tuple(sorted(set(owner), key=str))
    plausible = []
    for h in (0, 1):
        fits = False
        for j in range(min(k, len(labels)) + 1):
            for S in combinations(labels, j):
                if consistent_on_intact_edges(n, edges, owner, h, observed, S, selected):
                    fits = True
                    break
            if fits:
                break
        if fits:
            plausible.append(h)
    return plausible


def feasible_transcripts(n, edges, owner, k):
    """Exhaustive test oracle, feasible only on tiny graphs."""
    labels = tuple(sorted(set(owner), key=str))
    transcripts = [set(), set()]
    for h in (0, 1):
        for ss in range(1 << n):
            baseline = report(n, edges, h, ss)
            for j in range(min(k, len(labels)) + 1):
                for bad in combinations(labels, j):
                    inc = incident_mask(edges, owner, bad)
                    sub = inc
                    while True:
                        transcripts[h].add(baseline ^ sub)
                        if sub == 0:
                            break
                        sub = (sub - 1) & inc
    return transcripts


def edge_frustration(n, edges):
    return min(report(n, edges, 1, ss).bit_count() for ss in range(1 << n))


def brute_min_cost_robust_design(n, edges, owner, k):
    """Exact combinatorial optimum for ≤ 15 candidate edges; exponential by design."""
    opt_cost = float('inf')
    opt_mask = None
    tests = 0
    for mask in range(1 << len(edges)):
        cost = sum(e[3] for j, e in enumerate(edges) if (mask >> j) & 1)
        if cost >= opt_cost:
            continue
        tests += 1
        if certified_for_k(n, edges, owner, k, mask)[0]:
            opt_cost, opt_mask = cost, mask
    return opt_cost, opt_mask, tests


def independent_triangles(count=3, triangle_costs=None):
    if triangle_costs is None:
        triangle_costs = [3] * count
    edges = []
    for block in range(count):
        u = 3 * block
        total = triangle_costs[block]
        assert total >= 3
        edges += [(u, u + 1, 1, 1), (u + 1, u + 2, 0, 1), (u + 2, u, 0, total - 2)]
    return 3 * count, edges


def shared_hub_triangles(count=3):
    edges = []
    for block in range(count):
        v = 2 * block + 1
        edges += [(0, v, 1, 1), (v, v + 1, 0, 1), (v + 1, 0, 0, 1)]
    return 1 + 2 * count, edges


def test_boundary_exhaustive(rng):
    # Exhaustively test both hypothesis transcript sets against theorem on tiny random graphs.
    for iteration in range(120):
        n = rng.randint(3, 5)
        candidate = list(combinations(range(n), 2))
        rng.shuffle(candidate)
        edges = [(u, v, rng.randrange(2), 1) for u, v in candidate[:rng.randint(2, min(7, len(candidate)))]]
        owner = [rng.randrange(1, n + 1) for _ in range(n)]
        k = rng.randrange(2)
        expected, tau, _ = certified_for_k(n, edges, owner, k)
        c0, c1 = feasible_transcripts(n, edges, owner, k)
        observed = not bool(c0 & c1)
        assert expected == observed, (iteration, n, edges, owner, k, tau, c0 & c1)
    print('PASS: 120 random owner-labeled graphs: complete transcript enumeration agrees with tau > 2k')


def test_decoder(rng):
    n, edges = independent_triangles(3)
    owner = list(range(n))
    assert certified_for_k(n, edges, owner, 1)[1] == 3
    # 3 disjoint cycles form an owner-disjoint certificate.
    for _ in range(2000):
        h = rng.randrange(2)
        ss = rng.randrange(1 << n)
        bad = rng.randrange(n)
        possibilities = incident_mask(edges, owner, {bad})
        error = rng.randrange(1 << len(edges)) & possibilities
        y = report(n, edges, h, ss, error)
        assert plausible_hypotheses(n, edges, owner, 1, y) == [h]
    print('PASS: 2000 random node-offset + Byzantine-principal trials, unique correct hypothesis')


def main():
    rng = Random(20261122)
    test_boundary_exhaustive(rng)
    test_decoder(rng)

    n, hub = shared_hub_triangles(3)
    h_owner = list(range(n))
    robust_hub, tau_hub, witness_hub = certified_for_k(n, hub, h_owner, 1)
    d_hub = edge_frustration(n, hub)
    assert d_hub == 3 and tau_hub == 1 and not robust_hub
    print(f'SHARED-HUB: d_edge={d_hub}; principal_tau={tau_hub}; k=1 robust={robust_hub}; destructive owner set={witness_hub}')

    n, triangles = independent_triangles(3)
    unique_owner = list(range(n))
    robust_dis, tau_dis, _ = certified_for_k(n, triangles, unique_owner, 1)
    assert robust_dis and tau_dis == 3
    # 9 delegate vertices but just one ultimate principal: no false Sybil resilience.
    one_owner = ['P'] * n
    robust_sybil, tau_sybil, _ = certified_for_k(n, triangles, one_owner, 1)
    assert not robust_sybil and tau_sybil == 1
    print(f'3 INDEPENDENT TRIANGLES: 9 authenticated owners tau={tau_dis}, one real owner and 9 delegates tau={tau_sybil}')

    n, four = independent_triangles(4, [4, 7, 10, 15])
    owners = list(range(n))
    cost, mask, tested = brute_min_cost_robust_design(n, four, owners, 1)
    assert cost == 21
    chosen = [i for i in range(len(four)) if (mask >> i) & 1]
    assert len(chosen) == 9
    print(f'EXACT AUDIT DESIGN: candidate_edges={len(four)}; k=1; minimum cost={cost}; selected_edges={chosen}; candidates_evaluated={tested}')
    print('All restricted-model checks passed. No theorem is claimed new in the literature.')


if __name__ == '__main__':
    main()
