"""Finite tests for the REFLEX multi-custodian witness-assembly example."""
import importlib.util
import pathlib
import sys
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "src" / "reflex9_witness_assembly_game.py"
spec = importlib.util.spec_from_file_location("reflex9_witness_assembly_game", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)
WitnessAssemblyGame = mod.WitnessAssemblyGame


class WitnessAssemblyTests(unittest.TestCase):
    def make_game(self, witnesses=None, reward=2.0, completion=False):
        owners = ("a", "b", "c", "d")
        return WitnessAssemblyGame(
            owners=owners,
            witnesses=witnesses or (frozenset(("a", "b")), frozenset(("c", "d"))),
            effort={p: 1.0 for p in owners},
            reward={p: reward for p in owners},
            silence_benefit={p: 0.5 for p in owners},
            pay_only_on_completion=completion,
        )

    def test_two_independent_witnesses_have_owner_cut_two(self):
        self.assertEqual(self.make_game().minimum_owner_cut(), 2)

    def test_completion_only_prize_has_silent_equilibrium_even_when_large(self):
        g = self.make_game(reward=1000.0, completion=True)
        self.assertIn(frozenset(), g.pure_nash_equilibria())
        self.assertFalse(g.is_refuted(frozenset()))

    def test_individual_valid_fragment_rewards_refute_with_one_owner_corrupt(self):
        result = self.make_game(reward=2.0).worst_case_false_finalization(k=1)
        self.assertTrue(result["all_pure_nash_refute_false_claim"])
        self.assertGreater(result["pure_nash_profiles_checked"], 0)

    def test_shared_witness_owner_creates_single_point_of_failure(self):
        g = self.make_game(witnesses=(frozenset(("a", "b")), frozenset(("a", "c"))))
        self.assertEqual(g.minimum_owner_cut(), 1)
        self.assertFalse(g.worst_case_false_finalization(k=1)["all_pure_nash_refute_false_claim"])

    def test_small_reward_leaves_silent_equilibrium(self):
        self.assertIn(frozenset(), self.make_game(reward=0.2).pure_nash_equilibria())

    def test_relabeling_delegates_does_not_make_owner_independent(self):
        g = self.make_game(witnesses=(frozenset(("a", "b")), frozenset(("a", "d"))))
        self.assertEqual(g.minimum_owner_cut(), 1)

    def test_unknown_witness_owner_is_rejected(self):
        with self.assertRaises(ValueError):
            self.make_game(witnesses=(frozenset(("a", "unknown")),))


if __name__ == "__main__":
    unittest.main()
