"""Synthetic benchmark: can an auditor find a skipped duty when multi-agent logs go missing?

Each episode has three agent roles (planner, executor, verifier). In a gap episode exactly one role
skipped its required duty. Every role writes three log fields about its duty; each field is right with
probability FIELD_ACCURACY. Fields then go missing in two ways:

* independent omission: each field is lost on its own with probability ``missing_rate``;
* shared outage: with probability ``outage_rate`` the log store shared by the executor and the verifier
  fails, and all six of their fields are lost together (a correlated failure).
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

ROLES: Tuple[str, ...] = ("planner", "executor", "verifier")
SHARED_STORE: Tuple[str, ...] = ("executor", "verifier")
FIELDS_PER_ROLE = 3
GAP_RATE = 0.35
FIELD_ACCURACY = 0.9
COST_FN = 5
COST_FP = 1

# A field is True ("duty done"), False ("duty not done") or None (missing).
Field = Optional[bool]


@dataclass(frozen=True)
class Episode:
    true_gap: int
    skipped_role: Optional[str]
    outage: bool
    logs: Dict[str, Tuple[Field, ...]]

    def missing_fields(self) -> int:
        return sum(v is None for fields in self.logs.values() for v in fields)


def make_episode(seed: int, missing_rate: float, outage_rate: float) -> Episode:
    """One reproducible synthetic episode. Not real agent data."""
    rng = random.Random(seed)
    true_gap = int(rng.random() < GAP_RATE)
    skipped = rng.choice(ROLES) if true_gap else None
    outage = rng.random() < outage_rate
    logs: Dict[str, Tuple[Field, ...]] = {}
    for role in ROLES:
        done = role != skipped
        fields: List[Field] = []
        for _ in range(FIELDS_PER_ROLE):
            reported = done if rng.random() < FIELD_ACCURACY else not done
            lost = rng.random() < missing_rate
            fields.append(None if lost or (outage and role in SHARED_STORE) else reported)
        logs[role] = tuple(fields)
    return Episode(true_gap, skipped, outage, logs)


def gap_probability(ep: Episode) -> float:
    """Chance that some role skipped its duty, given only the fields that were logged.

    Exact under the simulator's own assumptions; a missing field carries no evidence either way.
    """
    prior = GAP_RATE / len(ROLES)
    lr = FIELD_ACCURACY / (1 - FIELD_ACCURACY)
    weights = {}
    for role in ROLES:
        not_done = sum(v is False for v in ep.logs[role])
        done = sum(v is True for v in ep.logs[role])
        weights[role] = prior * lr ** (not_done - done)
    no_gap = 1 - GAP_RATE
    # Fields of a role that did its duty look the same whether or not another role skipped,
    # so the ratio for "role r skipped" against "no gap" is prior * lr^(not_done - done) / no_gap.
    total = sum(weights.values())
    return total / (total + no_gap)


def _majority_not_done(fields: Sequence[Field], missing_as: Optional[bool]) -> Optional[bool]:
    """True if most of the role's fields say "not done"; None if the rule refuses to judge."""
    values = [missing_as if v is None else v for v in fields]
    if any(v is None for v in values):
        return None
    return sum(v is False for v in values) * 2 > len(values)


def predict(ep: Episode, rule: str, threshold: float = 0.5) -> int:
    """1 = report a responsibility gap.

    strict_complete     only judges a role whose three fields are all present
    optimistic_missing  a missing field counts as "duty done"
    pessimistic_missing a missing field counts as "duty not done"
    probability         gap_probability(ep) >= threshold (threshold chosen on training seeds)
    """
    if rule == "probability":
        return int(gap_probability(ep) >= threshold)
    missing_as = {"strict_complete": None, "optimistic_missing": True, "pessimistic_missing": False}
    if rule not in missing_as:
        raise ValueError("unknown rule: %s" % rule)
    verdicts = [_majority_not_done(ep.logs[r], missing_as[rule]) for r in ROLES]
    return int(any(v is True for v in verdicts))


def metrics(labels: Sequence[int], preds: Sequence[int]) -> Dict[str, float]:
    tp = sum(y == 1 and p == 1 for y, p in zip(labels, preds))
    fp = sum(y == 0 and p == 1 for y, p in zip(labels, preds))
    fn = sum(y == 1 and p == 0 for y, p in zip(labels, preds))
    tn = sum(y == 0 and p == 0 for y, p in zip(labels, preds))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1, "fpr": fp / (fp + tn) if fp + tn else 0.0,
            "weighted_cost": COST_FN * fn + COST_FP * fp, "tp": tp, "fp": fp, "fn": fn, "tn": tn}
