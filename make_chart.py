"""Draws outputs/recall_fpr_by_outage.png from outputs/metrics_by_seed.csv. Needs matplotlib (optional)."""
from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent
MISSING = 0.15
RULES = [
    ("probability", "Probability, cost-tuned threshold", "#2b5ce6", "-"),
    ("optimistic_missing", "Missing counts as done", "#35c3ff", "-"),
    ("pessimistic_missing", "Missing counts as not done", "#c62828", "--"),
    ("strict_complete", "Judge complete logs only", "#0f1830", ":"),
]


def main(out: Path) -> None:
    rows = list(csv.DictReader((ROOT / "outputs" / "metrics_by_seed.csv").open()))
    rows = [r for r in rows if abs(float(r["missing_rate"]) - MISSING) < 1e-9]
    outages = sorted({float(r["shared_outage_rate"]) for r in rows})
    fig, axes = plt.subplots(1, 2, figsize=(10.06, 5.2), dpi=100, sharex=True)
    for ax, metric, title in ((axes[0], "recall", "Gaps found (recall)"), (axes[1], "fpr", "False alarms (FPR)")):
        for key, label, colour, style in RULES:
            ys = [statistics.mean(float(r[metric]) for r in rows if r["rule"] == key
                                  and float(r["shared_outage_rate"]) == o) * 100 for o in outages]
            ax.plot([o * 100 for o in outages], ys, style, marker="o", color=colour, lw=2.2, label=label)
        ax.set_title(title, loc="left", fontsize=12, color="#0f1830")
        ax.set_ylim(0, 105)
        ax.set_xticks([o * 100 for o in outages])
        ax.set_xlabel("Shared outage rate (%)", color="#0f1830")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color("#dbe3f0")
        ax.tick_params(colors="#55617c")
    axes[0].set_ylabel("%, mean of 5 test seeds, 15% of fields missing", color="#0f1830")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(out)
    print("Wrote %s" % out)


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "outputs" / "recall_fpr_by_outage.png")
