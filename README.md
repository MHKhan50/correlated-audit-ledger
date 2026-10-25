# Correlated Audit Ledger v0.1.0

**Research question:** How do independent field omissions and shared whole-agent outages affect responsibility-gap detection in multi-agent AI systems, and can cost-sensitive threshold selection improve held-out performance?

This is a lightweight, standard-library-only synthetic simulation. It does not call an LLM, use external datasets, or claim real-world validation.

## Quick start (Mac)

```bash
cd "$HOME/Downloads" && unzip -oq correlated-audit-ledger-v0.1.0.zip
cd "$HOME/Downloads/correlated-audit-ledger-v0.1.0" && python3 -m unittest discover -s tests -v && python3 run_experiment.py
open "$HOME/Downloads/correlated-audit-ledger-v0.1.0/outputs/results_summary.md"
```

The run creates `outputs/synthetic_test_dataset.csv`, `outputs/metrics_by_seed.csv`, and `outputs/results_summary.md`. Upload the CSV only with its dataset card and synthetic-data disclosure.

## Methods

Three simulated agent roles are abstracted into an episode-level evidence score. The experiment varies independent field missingness (0.05, 0.15, 0.30) and shared outage probability (0, 0.10, 0.25). Train seeds are 11, 22, 33; held-out test seeds are 44 and 55. The weighted loss is 5 per false negative and 1 per false positive. The threshold is selected using training episodes only. Metrics are exploratory, with only two test seeds.

## Limitations

The simulator is intentionally simplified; its generated values are not real agent logs and do not establish that any detector works in deployed systems. Threshold selection can overfit the simulated distribution. Validate with preregistered protocols and appropriately governed real data before drawing deployment conclusions.

## Sources and research context

- University of Southampton, [Responsibility gaps and AI safety in multiagent systems](https://www.southampton.ac.uk/study/postgraduate-research/projects/responsibility-gaps-ai-safety-in-multiagent-systems) (research-interest context; not an endorsement of this project).
- Ulster University, [Agentic AI for Complex Environments](https://www.ulster.ac.uk/doctoralcollege/find-a-phd/11a-computing/1903114) (research-interest context; check the official page for current eligibility and deadlines).
- King's College London, [Cooperative AI Lab](https://coopai.kcl.ac.uk/) (research-group context, not a specific vacancy).

## License
Code: MIT. Synthetic data and figures: CC BY 4.0. See `LICENSE` and `CITATION.cff`.
