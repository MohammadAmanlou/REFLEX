"""REFLEX 8: no-state-oracle refutable certification for principal-labelled graphs.

Research *sanity checks*, NOT a claim of novelty or an LLM experiment.
Python >=3.10, standard library only.

Model: y_e = s_u XOR s_v XOR b_e*h XOR eta_e,
where tampering eta occurs only on edges incident to up to k corrupted owners.
Valid refutation of claim z is a b-odd simple cycle whose authenticated
edge receipts have XOR parity != z.

Two threat models:
  (A) all signed receipts are public;
  (B) only designated authenticated accessors can disclose entire cycles.
All assumptions and restrictions are spelled out in the companion manuscript.
"""
from __future__ import annotations
from itertools import combinations, product
from random import Random
from math import inf


def odd_cycles(n, edges):
    """Exhaustively enumerate b-odd simple cycles (small graphs only)."""
    found = []
    m = len(edges)
    for size in range(3, m + 1):
        for subset in combinations(range(m), size):
            adj = {v: set() for v in range(n)}
            xor_b = 0
            for j in subset:
                u, v, b = edges[j]
                adj[u].add(v)
                adj[v].add(u)
                xor_b ^= b
            vertices = {v for v in range(n) if adj[v]}
            if xor_b != 1 or len(vertices) != size or any(len(adj[v]) != 2 for v in vertices):
                continue
            seen = {next(iter(vertices))}
            todo = list(seen)
            while todo:
                u = todo.pop()
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        todo.append(v)
            if seen == vertices:
                found.append(frozenset(subset))
    return sorted(set(found), key=lambda x: tuple(sorted(x)))


def edge_mask(n, edges, owners, compromised):
    return sum(1 << j for j, (u, v, _) in enumerate(edges)
               if owners[u] in compromised or owners[v] in compromised)


def receipt(n, edges, h, s, eta=0):
    return sum(((s[u] ^ s[v] ^ (b & h) ^ ((eta >> j) & 1)) << j)
               for j, (u, v, b) in enumerate(edges))


def all_transcripts(n, edges, owners, h, k):
    principals = sorted(set(owners))
    output = set()
    for owner_count in range(min(k, len(principals)) + 1):
        for S in combinations(principals, owner_count):
            allowed = [i for i in range(len(edges)) if (edge_mask(n, edges, owners, S) >> i) & 1]
            for flips in product((0, 1), repeat=len(allowed)):
                eta = sum(bit << j for j, bit in zip(allowed, flips))
                for s in product((0, 1), repeat=n):
                    output.add(receipt(n, edges, h, s, eta))
    return output


def principal_transversal(n, edges, owners, cycles=None):
    cycles = odd_cycles(n, edges) if cycles is None else cycles
    cycle_owners = [{owners[v] for j in cyc for v in edges[j][:2]} for cyc in cycles]
    principals = sorted(set(owners))
    for size in range(len(principals) + 1):
        for S in combinations(principals, size):
            if all(set(S) & c_owners for c_owners in cycle_owners):
                return size
    raise AssertionError('empty deletion set should eventually be found')


def public_cycle_certification(y, candidate, cycles):
    """Accept candidate iff all b-odd simple-cycle receipts agree with it."""
    if not cycles:
        return False
    for cyc in cycles:
        parity = sum((y >> j) & 1 for j in cyc) % 2
        if parity != candidate:
            return False
    return True


def cycle_accessibility_frontier(n, edges, owners, accessors):
    """Small-graph exact owner cut for authenticated cycle-proof availability.

    accessors maps each odd cycle (frozenset edge IDs) to a set of owners
    that can individually disclose every receipt on the cycle.
    A cycle remains a trustworthy challenge witness under compromise set S
    iff all its measurement owners are uncorrupted AND some accessor is not in S.
    """
    cs = odd_cycles(n, edges)
    principals = sorted(set(owners))
    def survives(C, S):
        involved = {owners[v] for j in C for v in edges[j][:2]}
        return not involved.intersection(S) and bool(set(accessors.get(C, [])) - S)
    for size in range(len(principals) + 1):
        for subset in combinations(principals, size):
            S = set(subset)
            if not any(survives(C, S) for C in cs):
                return size
    return len(principals)


def exact_min_custody(n, edges, owners, grants, k):
    """Enumerate minimum-cost authorised (cycle, custodian, cost) grants.

    The owner-size-k corruption scenarios must each leave at least one
    fully honest b-odd cycle and honest authorised custodian.
    This is a restricted weighted set cover baseline, NOT a scalable advance.
    """
    cs = set(odd_cycles(n, edges))
    for cyc, a, cost in grants:
        assert cyc in cs and a in set(owners) and cost >= 0
    principals = set(owners)
    scenarios = [set(S) for r in range(min(k, len(principals))+1)
                 for S in combinations(sorted(principals), r)]
    best = (inf, [])
    for size in range(len(grants)+1):
        for idxs in combinations(range(len(grants)), size):
            total = sum(grants[i][2] for i in idxs)
            if total >= best[0]-1e-10:
                continue
            viable = True
            for S in scenarios:
                if not any(a not in S and
                           not ({owners[v] for j in cyc for v in edges[j][:2]} & S)
                           for i in idxs for cyc,a,_ in [grants[i]]):
                    viable = False
                    break
            if viable:
                best = (total, [grants[i] for i in idxs])
    return best


def enumerate_equilibrium_challenge_game(witnesses, rational_owner_ids, reward, challenge_cost, false_finalization_value):
    """Enumerate pure Nash equilibria of the post-proposal challenge subgame.

    When an owner has a valid witness they can challenge; a verified challenge
    pays reward whether or not other owners challenge (no free-rider issue).
    An owner with no valid witness can challenge but pays an unrefunded cost.
    Finalized wrong proposal gives each owner at most false_finalization_value
    payoff vs rejection. This is a stylized worst-case bound, not a human model.
    """
    ps = list(rational_owner_ids)
    payoffs = {}
    for actions in product((0, 1), repeat=len(ps)):
        challenged = any(actions[i] and witnesses.get(p, False) for i, p in enumerate(ps))
        pay = []
        for i, p in enumerate(ps):
            a = actions[i]
            valid = witnesses.get(p, False)
            if a and valid:
                pay.append(reward - challenge_cost)
            elif a:
                pay.append(-challenge_cost + (false_finalization_value if not challenged else 0.0))
            else:
                pay.append(false_finalization_value if not challenged else 0.0)
        payoffs[actions] = (pay, challenged)
    equilibria = []
    for actions, (pay, challenged) in payoffs.items():
        if all(pay[i] >= payoffs[actions[:i] + (1-actions[i],) + actions[i+1:]][0][i] - 1e-10
               for i in range(len(ps))):
            equilibria.append((actions, challenged))
    return equilibria


def test_theorem_random(seed=20261122, instances=180):
    rng = Random(seed)
    checks = 0
    regimes = {'impossible': 0, 'safe_only': 0, 'full_recovery': 0}
    for _ in range(instances):
        n = rng.choice([3, 4, 5])
        all_edges = list(combinations(range(n), 2))
        rng.shuffle(all_edges)
        m = rng.randrange(3, min(7, len(all_edges)) + 1)
        edges = [(u, v, rng.randrange(2)) for u, v in all_edges[:m]]
        # Some agents share owners, to check Sybil/clone effects.
        owners = [rng.randrange(max(2, n-1)) for _ in range(n)]
        principals = len(set(owners))
        k = rng.randrange(min(2, principals) + 1)
        cycles = odd_cycles(n, edges)
        tau = principal_transversal(n, edges, owners, cycles)
        Y00 = all_transcripts(n, edges, owners, 0, 0)
        Y10 = all_transcripts(n, edges, owners, 1, 0)
        Y0k = all_transcripts(n, edges, owners, 0, k)
        Y1k = all_transcripts(n, edges, owners, 1, k)
        assert (not bool(Y00 & Y1k)) == (tau > k), ('one-sided indistinguishability', edges, owners, k, tau)
        assert (not bool(Y10 & Y0k)) == (tau > k), ('symmetry', edges, owners, k, tau)
        assert (not bool(Y0k & Y1k)) == (tau > 2*k), ('two-sided indistinguishability', edges, owners, k, tau)
        # Noncorrupt full transcript must be accepted when tau>0.
        if tau:
            assert all(public_cycle_certification(y, 0, cycles) for y in Y00)
            assert all(public_cycle_certification(y, 1, cycles) for y in Y10)
        # With at most k corrupted owners, no wrong acceptance when tau>k.
        if tau > k:
            assert not any(public_cycle_certification(y, 1, cycles) for y in Y0k)
            assert not any(public_cycle_certification(y, 0, cycles) for y in Y1k)
        regime = ('impossible' if tau <= k else 'safe_only' if tau <= 2*k else 'full_recovery')
        regimes[regime] += 1
        checks += 1
    return checks, regimes


def check_examples():
    # Two completely disjoint owner-independent odd triangles.
    edges = [(0,1,1),(1,2,0),(2,0,0),(3,4,1),(4,5,0),(5,3,0)]
    owners = list(range(6))
    cycles = odd_cycles(6, edges)
    assert len(cycles) == 2
    tau = principal_transversal(6, edges, owners, cycles)
    assert tau == 2
    assert not (tau > 2*1) and tau > 1
    honest_zero = all_transcripts(6, edges, owners, 0, 0)
    honest_one = all_transcripts(6, edges, owners, 1, 0)
    attacked_zero = all_transcripts(6, edges, owners, 0, 1)
    attacked_one = all_transcripts(6, edges, owners, 1, 1)
    assert not (honest_zero & attacked_one) and not (honest_one & attacked_zero)
    assert (attacked_zero & attacked_one), 'two-sided decoding must be impossible in the middle regime'
    assert all(not public_cycle_certification(y, 1, cycles) for y in attacked_zero)
    assert all(not public_cycle_certification(y, 0, cycles) for y in attacked_one)
    # One corrupt owner can falsify one cycle but cannot certify an incorrect h.
    S = {0}
    attacked = [receipt(6, edges, 0, (0,)*6, 1 << 0)]
    assert all(not public_cycle_certification(y, 1, cycles) for y in attacked)
    assert all(not public_cycle_certification(y, 0, cycles) for y in attacked), 'attacker can force abstention'
    # Three owner-disjoint cycles guarantee full unique correction for k=1.
    edges3 = edges + [(6,7,1),(7,8,0),(8,6,0)]
    assert principal_transversal(9, edges3, list(range(9))) == 3
    # An external sole custodian for *both* cycles is a single point of failure.
    # Accessors listed as owners who can disclose all three signed receipts.
    sole = {C: {0} for C in cycles}
    separated = {cycles[0]: {0}, cycles[1]: {3}}
    l1 = cycle_accessibility_frontier(6, edges, owners, sole)
    l2 = cycle_accessibility_frontier(6, edges, owners, separated)
    assert (l1, l2) == (1, 2)
    grants = [(cycles[0],0,1.0),(cycles[1],0,0.2),
              (cycles[1],3,1.2),(cycles[0],1,1.5)]
    custody_opt, chosen = exact_min_custody(6, edges, owners, grants, 1)
    assert abs(custody_opt-2.2)<1e-10
    chosen_accessors = {C:set() for C in cycles}
    for C,a,_ in chosen:
        chosen_accessors[C].add(a)
    assert cycle_accessibility_frontier(6,edges,owners,chosen_accessors)>1
    # Game: an honest watcher with a valid refutation must challenge at ALL Nash equilibria.
    e = enumerate_equilibrium_challenge_game({0: True, 1: False}, [0,1], 3.0, 1.0, 0.5)
    assert e and all(challenged for _, challenged in e), e
    # If challenger's attainable reward is less than lost collusive benefit,
    # no-challenge equilibrium can reappear: a sharp incentive counterexample.
    weak = enumerate_equilibrium_challenge_game({0: True}, [0], 1.1, 1.0, 1.0)
    assert any(not challenged for _, challenged in weak), weak
    return {"two_triangle_tau":tau,"k":1,"three_triangle_tau":3,
            "single_custodian_cut":l1,"independent_custodian_cut":l2,
            "challenge_equilibria":len(e),"weak_bounty_unsafe_equilibria":len(weak),
            "two_triangle_ambiguous_attack_transcripts":len(attacked_zero & attacked_one),
            "least_cost_robust_custody":custody_opt, "chosen_custody_grants":len(chosen)}


if __name__ == '__main__':
    count, regimes = test_theorem_random()
    e = check_examples()
    print('REFLEX-8 reproducibility audit: PASS')
    print(f'Random graph/transcript exhaustive checks: {count}/{count}')
    print(f'Random instances by regime: {regimes}')
    for k,v in e.items():
        print(f'{k}: {v}')
    print('Status: restricted binary model; NO external peer review, NO LLM trial, NO historical priority claim.')
