"""Runs the benchmark and writes outputs/. Python 3.9+, standard library only."""
from __future__ import annotations

import csv
import statistics
from pathlib import Path
from typing import Dict, List

from audit_ledger import FIELDS_PER_ROLE, ROLES, gap_probability, make_episode, metrics, predict

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
MISSING_RATES = [0.05, 0.15, 0.30]
OUTAGE_RATES = [0.0, 0.10, 0.25]
TRAIN_SEEDS = [11, 22, 33]
TEST_SEEDS = [44, 55, 66, 77, 88]
TRAIN_EPISODES = 300
TEST_EPISODES = 400
RULES = ["probability", "strict_complete", "optimistic_missing", "pessimistic_missing"]
CANDIDATES = [round(x / 100, 2) for x in range(5, 96, 5)]


def episodes(seed: int, n: int, mr: float, orate: float):
    return [make_episode(seed * 100000 + i, mr, orate) for i in range(n)]


def tune_threshold(train) -> float:
    """Threshold with the lowest weighted cost on the training seeds (ties: the lower threshold)."""
    labels = [e.true_gap for e in train]
    probs = [gap_probability(e) for e in train]
    return min(CANDIDATES, key=lambda t: (metrics(labels, [int(p >= t) for p in probs])["weighted_cost"], t))


def cell(v):
    return "" if v is None else int(v)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data: List[Dict] = []
    per_seed: List[Dict] = []
    for mr in MISSING_RATES:
        for orate in OUTAGE_RATES:
            train = [e for s in TRAIN_SEEDS for e in episodes(s, TRAIN_EPISODES, mr, orate)]
            threshold = tune_threshold(train)
            for seed in TEST_SEEDS:
                eps = episodes(seed, TEST_EPISODES, mr, orate)
                for i, e in enumerate(eps):
                    row = {"seed": seed, "episode_id": "%d-%d" % (seed, i), "missing_rate": mr,
                           "shared_outage_rate": orate, "true_responsibility_gap": e.true_gap,
                           "skipped_role": e.skipped_role or "", "shared_outage": int(e.outage)}
                    for r in ROLES:
                        for k, v in enumerate(e.logs[r]):
                            row["%s_field%d" % (r, k + 1)] = cell(v)
                    row["gap_probability"] = round(gap_probability(e), 6)
                    data.append(row)
                labels = [e.true_gap for e in eps]
                for rule in RULES:
                    m = metrics(labels, [predict(e, rule, threshold) for e in eps])
                    per_seed.append({"missing_rate": mr, "shared_outage_rate": orate, "seed": seed, "rule": rule,
                                     "threshold": threshold if rule == "probability" else "", **m})

    with (OUT / "synthetic_test_dataset.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)
    with (OUT / "metrics_by_seed.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(per_seed[0].keys()))
        w.writeheader()
        w.writerows(per_seed)

    groups: Dict[tuple, List[Dict]] = {}
    for r in per_seed:
        groups.setdefault((r["missing_rate"], r["shared_outage_rate"], RULES.index(r["rule"])), []).append(r)
    lines = ["# Results", "",
             "Synthetic benchmark only, not evidence about real systems or language models. "
             "Mean over test seeds %s (%d episodes each); range is the lowest and highest seed." % (
                 ", ".join(map(str, TEST_SEEDS)), TEST_EPISODES), "",
             "| Missing | Shared outage | Rule | Threshold | Recall mean (range) | FPR mean (range) | F1 mean | Weighted cost mean |",
             "|---:|---:|---|---:|---:|---:|---:|---:|"]
    for (mr, orate, ri), rs in sorted(groups.items()):
        rec = [x["recall"] for x in rs]
        fpr = [x["fpr"] for x in rs]
        lines.append("| %.2f | %.2f | %s | %s | %.3f (%.3f-%.3f) | %.3f (%.3f-%.3f) | %.3f | %.1f |" % (
            mr, orate, RULES[ri], rs[0]["threshold"] if rs[0]["threshold"] != "" else "-",
            statistics.mean(rec), min(rec), max(rec), statistics.mean(fpr), min(fpr), max(fpr),
            statistics.mean(x["f1"] for x in rs), statistics.mean(x["weighted_cost"] for x in rs)))
    (OUT / "results_summary.md").write_text("\n".join(lines) + "\n")
    (OUT / "dataset_card.md").write_text(
        "# Dataset card\n\n"
        "`synthetic_test_dataset.csv` is written by `run_experiment.py`. One row per simulated test episode: "
        "the true label (was a duty skipped, and by which role), whether a shared outage happened, the nine "
        "logged fields (%d roles x %d fields; 1 = log says done, 0 = log says not done, blank = missing) and "
        "the gap probability an auditor computes from them.\n\n"
        "It is generated from fixed seeds, so it is the same on every run. It is not collected from real "
        "users, deployed systems or language models. Use it for teaching and for testing audit methods, "
        "not for claims about real systems.\n" % (len(ROLES), FIELDS_PER_ROLE))
    print("Wrote %d episodes and %d metric rows to %s" % (len(data), len(per_seed), OUT))


if __name__ == "__main__":
    main()
