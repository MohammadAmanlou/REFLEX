"""Finite witness-assembly games for the REFLEX restricted research prototype.

Assumptions: authenticated owners; independently verifiable local fragments;
Byzantine owners only withhold their own evidence; complete witnesses are
conjunctions of owner fragments; the evaluator knows the candidate is false.
This is NOT a general equilibrium oracle, a truth detector, or an LLM evaluation.

Run: python src/reflex9_witness_assembly_game.py
     python -m unittest discover -s tests -v
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Dict, FrozenSet, Iterable, Mapping, Tuple


@dataclass(frozen=True)
class WitnessAssemblyGame:
    owners: Tuple[str, ...]
    witnesses: Tuple[FrozenSet[str], ...]
    effort: Mapping[str, float]
    reward: Mapping[str, float]
    silence_benefit: Mapping[str, float]
    pay_only_on_completion: bool = False

    def __post_init__(self) -> None:
        members = set(self.owners)
        if len(members) != len(self.owners) or not self.owners:
            raise ValueError("Owners must be unique and nonempty")
        if not self.witnesses or any(not w or not w <= members for w in self.witnesses):
            raise ValueError("Witnesses must be nonempty owner subsets")
        for label, values in (("effort", self.effort), ("reward", self.reward),
                              ("silence_benefit", self.silence_benefit)):
            if set(values) != members or any(x < 0 for x in values.values()):
                raise ValueError(label + " needs a nonnegative value per owner")

    def minimum_owner_cut(self) -> int:
        """Smallest set of authentic owners intersecting every witness."""
        for size in range(len(self.owners) + 1):
            for removed in combinations(self.owners, size):
                if all(not w.isdisjoint(removed) for w in self.witnesses):
                    return size
        raise AssertionError("A nonempty witness family has an owner cut")

    def is_refuted(self, submitted: FrozenSet[str]) -> bool:
        return any(w <= submitted for w in self.witnesses)

    def utility(self, owner: str, submitted: FrozenSet[str]) -> float:
        """Toy payoff for a known-false claim; individual valid-fragment rewards."""
        revealed = owner in submitted
        refuted = self.is_refuted(submitted)
        paid = revealed and (refuted or not self.pay_only_on_completion)
        return (self.reward[owner] if paid else 0.0) - (
            self.effort[owner] if revealed else 0.0
        ) + (self.silence_benefit[owner] if not refuted else 0.0)

    def pure_nash_equilibria(self, corrupt: Iterable[str] = ()) -> Tuple[FrozenSet[str], ...]:
        """Exhaustive pure-Nash oracle; Byzantine principals fixed silent."""
        blocked = frozenset(corrupt)
        if not blocked <= set(self.owners):
            raise ValueError("Unknown corrupt owner")
        available = tuple(i for i in self.owners if i not in blocked)
        equilibria = []
        for strategy in product((False, True), repeat=len(available)):
            submitted = frozenset(i for i, act in zip(available, strategy) if act)
            if all(self.utility(i, submitted) >= self.utility(
                    i, submitted ^ frozenset((i,))) - 1e-10 for i in available):
                equilibria.append(submitted)
        return tuple(equilibria)

    def worst_case_false_finalization(self, k: int) -> Dict[str, object]:
        """All corruption sets <= k, all pure Nash profiles, false finalization."""
        if k < 0 or k > len(self.owners):
            raise ValueError("Invalid corruption budget")
        checked = 0
        unsafe_cases = []
        for size in range(k + 1):
            for corrupt in combinations(self.owners, size):
                for eq in self.pure_nash_equilibria(corrupt):
                    checked += 1
                    if not self.is_refuted(eq):
                        unsafe_cases.append((frozenset(corrupt), eq))
        return {
            "witness_cut": self.minimum_owner_cut(),
            "corruption_budget": k,
            "pure_nash_profiles_checked": checked,
            "all_pure_nash_refute_false_claim": not unsafe_cases,
            "unsafe_cases": tuple(unsafe_cases),
        }


def demonstration() -> None:
    owners = ("alice", "bob", "carol", "dave")
    witnesses = (frozenset(("alice", "bob")), frozenset(("carol", "dave")))
    effort = {p: 1.0 for p in owners}
    outside = {p: 0.5 for p in owners}
    reward = {p: 2.0 for p in owners}
    paid_fragments = WitnessAssemblyGame(owners, witnesses, effort, reward, outside)
    completion_prize = WitnessAssemblyGame(owners, witnesses, effort, reward, outside, True)
    print("restricted owner cut:", paid_fragments.minimum_owner_cut())
    print("partial-fragment rewards:", paid_fragments.worst_case_false_finalization(k=1))
    print("completion-only bounty:", completion_prize.worst_case_false_finalization(k=1))


if __name__ == "__main__":
    demonstration()
