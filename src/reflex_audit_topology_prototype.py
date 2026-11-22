"""REFLEX audit-topology: reproducible, small-scale mathematical sanity checks.

This is not a deployed agent mechanism, new-paper evidence, or a proof of novelty.
Model: y_e = s_u XOR s_v XOR b_e*h XOR adversarial_error_e.
Requires only Python >=3.9 standard library.
"""
from itertools import combinations
from heapq import heappush, heappop
from collections import deque
from random import Random
from math import comb


def edge_observation(n, edges, h, styles, error_mask=0):
    return sum(((styles[u] ^ styles[v] ^ (b & h) ^ ((error_mask >> j) & 1)) << j)
               for j, (u, v, b, cost) in enumerate(edges))


def hamming(x):
    return x.bit_count()


def frustration_index(n, edges):
    """d* = min_s || b + incidence*s ||_0. Exact exponential baseline."""
    best = len(edges) + 1
    for z in range(1 << n):
        style = [(z >> i) & 1 for i in range(n)]
        best = min(best, hamming(edge_observation(n, edges, 1, style)))
    return best


def minimum_unbalanced_cycle(n, edges):
    """Find min-cost odd-b cycle in undirected graph via parity-lifted Dijkstra.

    For positive edge costs, each odd closed walk contains an odd simple cycle
    no more expensive than that walk. Enumerate roots to find global minimum.
    """
    adjacency = [[] for _ in range(n)]
    for i, (u, v, b, cost) in enumerate(edges):
        if cost <= 0: raise ValueError('Positive costs required')
        adjacency[u].append((v, b, cost, i))
        adjacency[v].append((u, b, cost, i))
    best = float('inf')
    best_walk = None
    for root in range(n):
        dist = [[float('inf')]*2 for _ in range(n)]
        parent = {}
        dist[root][0] = 0
        queue = [(0,root,0)]
        while queue:
            d, u, parity = heappop(queue)
            if d != dist[u][parity]:continue
            if u==root and parity==1:break
            for v,b,c,i in adjacency[u]:
                q=parity^b
                if d+c < dist[v][q]:
                    dist[v][q]=d+c
                    parent[(v,q)]=(u,parity,i)
                    heappush(queue,(d+c,v,q))
        if dist[root][1] < best:
            best=dist[root][1]
            edges_on_walk=[]
            cur=(root,1)
            while cur!=(root,0):
                pu, pp, idx=parent[cur]
                edges_on_walk.append(idx)
                cur=(pu,pp)
            best_walk=list(reversed(edges_on_walk))
    return best, best_walk


def brute_min_unbalanced_cycle(n,edges):
    """Exhaustively enumerate single cycles (small graphs only)."""
    m=len(edges)
    best=float('inf')
    for mask in range(1,1<<m):
        ids=[j for j in range(m) if mask>>j&1]
        if len(ids)<3:continue
        if not sum(edges[j][2] for j in ids)%2:continue
        deg=[0]*n
        adj=[[] for _ in range(n)]
        for j in ids:
            u,v,_,_=edges[j]
            deg[u]+=1;deg[v]+=1
            adj[u].append(v);adj[v].append(u)
        if any(d not in (0,2) for d in deg):continue
        active={i for i in range(n) if deg[i]}
        if not active:continue
        seen={next(iter(active))}; stack=list(seen)
        while stack:
            for v in adj[stack.pop()]:
                if v not in seen:seen.add(v);stack.append(v)
        if seen!=active:continue
        cost=sum(edges[j][3] for j in ids)
        best=min(best,cost)
    return best


def robust_decoding_exact(n, edges):
    """Enumerate disjoint Hamming balls of radius t for the two hypothesis cosets."""
    m=len(edges)
    coset=[set(),set()]
    for s_bits in range(1<<n):
        s=[(s_bits>>i)&1 for i in range(n)]
        for h in range(2):coset[h].add(edge_observation(n,edges,h,s))
    min_dist=min(hamming(x^y) for x in coset[0] for y in coset[1])
    assert min_dist == frustration_index(n,edges)
    return min_dist, [len(q) for q in coset]


def greedy_edge_disjoint_odd_cycles(n, edges, number):
    """A sound but incomplete odd-cycle packing certificate."""
    remaining=list(range(len(edges)))
    cycles=[]
    for _ in range(number):
        current=[edges[j] for j in remaining]
        cost, walk=minimum_unbalanced_cycle(n,current)
        if walk is None:return None
        chosen=[remaining[j] for j in walk]
        if len(chosen)!=len(set(chosen)):
            raise AssertionError('Returned minimum-cost walk contains repeated edges')
        assert sum(edges[j][2] for j in chosen)%2 == 1
        cycles.append(chosen)
        removed=set(chosen)
        remaining=[j for j in remaining if j not in removed]
    return cycles


def majority_cycle_witness(edges, cycle_indices, report_bits):
    scores=[sum((report_bits>>j)&1 for j in cycle)%2 for cycle in cycle_indices]
    return 1 if sum(scores)>len(scores)//2 else 0


def test_packing_certificate():
    edges=[]
    for block in range(3):
        a=3*block
        edges.extend([(a,a+1,1,1),(a+1,a+2,0,1),(a+2,a,0,1)])
    cycles=greedy_edge_disjoint_odd_cycles(9,edges,3)
    assert cycles is not None and len(cycles)==3
    assert len(set(j for c in cycles for j in c))==9
    for h in range(2):
        for ss in range(1<<9):
            styles=[(ss>>i)&1 for i in range(9)]
            for error in [0]+[1<<i for i in range(len(edges))]:
                report=edge_observation(9,edges,h,styles,error)
                assert majority_cycle_witness(edges,cycles,report)==h
    print('PASS: 3 edge-disjoint unbalanced cycles recover h for all 5120 style/error combinations per hypothesis')


def exact_bsc_decision_statistics(n, edges, p):
    """Unconditional mass over all bit-flip patterns, nearest-coset with abstention on ties.

    Uniform over agent styles is not needed: an unknown style merely permutes
    each hypothesis coset, leaving distance-to-coset decisions invariant.
    """
    if not 0 <= p <= .5:raise ValueError('p must be in [0,.5]')
    m=len(edges)
    codewords=[set(),set()]
    for styles_bits in range(1<<n):
        styles=[(styles_bits>>j)&1 for j in range(n)]
        for h in range(2):codewords[h].add(edge_observation(n,edges,h,styles))
    outcomes=[]
    for h in range(2):
        actual=edge_observation(n,edges,h,[0]*n)
        correct=abstain=wrong=0.0
        for noise in range(1<<m):
            observed=actual^noise
            d0=min(hamming(observed^x) for x in codewords[0])
            d1=min(hamming(observed^x) for x in codewords[1])
            prob=(p**hamming(noise))*((1-p)**(m-hamming(noise)))
            if d0==d1:abstain+=prob
            elif (d1<d0)==bool(h):correct+=prob
            else:wrong+=prob
        assert abs(correct+abstain+wrong-1)<1e-10
        outcomes.append((correct,abstain,wrong))
    return outcomes


def test_random():
    rng=Random(20261122)
    for attempt in range(100):
        n=rng.randint(3,6)
        all_pairs=list(combinations(range(n),2));rng.shuffle(all_pairs)
        m=rng.randint(2,min(10,len(all_pairs)))
        edges=[(u,v,rng.randint(0,1),rng.randint(1,9)) for u,v in all_pairs[:m]]
        exact=brute_min_unbalanced_cycle(n,edges)
        result, _=minimum_unbalanced_cycle(n,edges)
        assert exact==result,(attempt,edges,exact,result)
        exact_d, _ = robust_decoding_exact(n,edges)
        assert exact_d == frustration_index(n,edges)
    print('PASS: 100 randomized small graphs, exhaustive cycle search and coset distance cross-check')


def main():
    test_random()
    test_packing_certificate()
    path=[(0,1,1,1),(1,2,0,1)]
    triangle=path+[(2,0,0,1)]
    k5=[(u,v,1,1) for u,v in combinations(range(5),2)]
    for name,n,edges in [('path',3,path),('triangle',3,triangle),('K5-all-negative',5,k5)]:
        d, sizes=robust_decoding_exact(n,edges)
        cost,walk=minimum_unbalanced_cycle(n,edges)
        t_max=(d-1)//2 if d>0 else -1
        print('%s: vertices=%d edges=%d, min-coset-distance=%d, t_max=%d, least-odd-cycle-cost=%s, coset-sizes=%s' %
              (name,n,len(edges),d,t_max,str(cost),str(sizes)))
        if walk is not None:
            assert sum(edges[j][2] for j in walk)%2==1
    # Probability that independent bit flips stay within the exact adversarial guarantee on K5
    p=.05;m=len(k5);t=1
    safe=sum(comb(m,j)*p**j*(1-p)**(m-j) for j in range(t+1))
    print('K5, p=0.05: Pr(number of corrupt reports <=1)=%.6f (certified correct under this event)'%safe)
    decisions=exact_bsc_decision_statistics(5,k5,.05)
    print('K5 BSC exact nearest-coset (correct, abstain, error):', tuple(round(x,6) for x in decisions[0]))
    assert all(abs(a-b)<1e-10 for a,b in zip(*decisions))
    print('PASS: all tests. This validates the restricted model, not literature novelty or LLM performance.')

if __name__=='__main__':main()
