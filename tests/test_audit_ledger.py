from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audit_ledger import Episode, gap_probability, make_episode, metrics, predict  # noqa: E402

DONE = (True, True, True)
NOT_DONE = (False, False, False)
LOST = (None, None, None)


def ep(planner, executor, verifier, gap=1):
    return Episode(gap, None, False, {"planner": planner, "executor": executor, "verifier": verifier})


class SimulatorTests(unittest.TestCase):
    def test_same_seed_same_episode(self):
        self.assertEqual(make_episode(12, 0.1, 0.1), make_episode(12, 0.1, 0.1))

    def test_shared_outage_removes_executor_and_verifier_together(self):
        e = make_episode(3, 0.0, 1.0)
        self.assertTrue(e.outage)
        self.assertEqual(e.logs["executor"], LOST)
        self.assertEqual(e.logs["verifier"], LOST)
        self.assertNotIn(None, e.logs["planner"])

    def test_no_missing_fields_without_omission_or_outage(self):
        self.assertEqual(make_episode(5, 0.0, 0.0).missing_fields(), 0)


class RuleTests(unittest.TestCase):
    def test_strict_does_not_judge_incomplete_logs(self):
        self.assertEqual(predict(ep(DONE, (False, False, None), DONE), "strict_complete"), 0)
        self.assertEqual(predict(ep(DONE, NOT_DONE, DONE), "strict_complete"), 1)

    def test_optimistic_counts_missing_as_done(self):
        self.assertEqual(predict(ep(DONE, (False, None, None), DONE), "optimistic_missing"), 0)
        self.assertEqual(predict(ep(DONE, (False, False, None), DONE), "optimistic_missing"), 1)

    def test_pessimistic_counts_missing_as_not_done(self):
        self.assertEqual(predict(ep(DONE, LOST, LOST, gap=0), "pessimistic_missing"), 1)

    def test_probability_ignores_missing_fields(self):
        clean = gap_probability(ep(DONE, DONE, DONE))
        outage = gap_probability(ep(DONE, LOST, LOST))
        self.assertLess(clean, 0.01)
        self.assertGreater(outage, clean)
        self.assertAlmostEqual(gap_probability(ep(LOST, LOST, LOST)), 0.35)

    def test_unknown_rule(self):
        with self.assertRaises(ValueError):
            predict(ep(DONE, DONE, DONE), "nope")


class MetricTests(unittest.TestCase):
    def test_perfect(self):
        self.assertEqual(metrics([0, 1], [0, 1])["f1"], 1)

    def test_missed_gap_costs_five_false_alarm_one(self):
        self.assertEqual(metrics([1], [0])["weighted_cost"], 5)
        self.assertEqual(metrics([0], [1])["weighted_cost"], 1)


if __name__ == "__main__":
    unittest.main()
