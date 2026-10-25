# Correlated Audit Ledger: Stress-Testing Responsibility-Gap Detection under Missing Multi-Agent Logs

## Abstract
Multi-agent AI systems may distribute tasks and evidence across several components. If logs are incomplete, a post-hoc audit may confuse absence of evidence with evidence that a duty was not performed. This small reproducible study proposes a synthetic benchmark for testing responsibility-gap detectors under independent field omissions and shared agent outages.

## Research question
How do independent field omissions and shared whole-agent outages affect responsibility-gap detection, and can a cost-sensitive threshold selected on training simulations improve held-out performance?

## Method
A standard-library Python simulator generates labelled episodes with varying missingness and outage rates. We compare simple score thresholds and a cost-sensitive threshold selected using separate training seeds. False negatives receive five times the cost of false positives. The held-out split uses two seeds, so results are exploratory.

## Results and interpretation
Run `python3 run_experiment.py` and quote values directly from `outputs/results_summary.md`. Do not generalize these synthetic results to real agents: the data are simulated, the evidence score is deliberately simplified, and only two held-out seeds are used. The benchmark is useful as a transparent starting point for testing missing-log assumptions, not as evidence of production readiness.

## Limitations and next steps
Extend the benchmark with calibrated causal models, richer missingness mechanisms, uncertainty intervals across many seeds, and carefully governed real traces where permission and provenance are clear. Predefine the evaluation protocol before examining final test results.

## Reproducibility
Python standard library only. See the repository README for commands, data card, test suite, and licence details.
