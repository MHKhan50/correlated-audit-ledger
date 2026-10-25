# Dataset card

`synthetic_test_dataset.csv` is written by `run_experiment.py`. One row per simulated test episode: the true label (was a duty skipped, and by which role), whether a shared outage happened, the nine logged fields (3 roles x 3 fields; 1 = log says done, 0 = log says not done, blank = missing) and the gap probability an auditor computes from them.

It is generated from fixed seeds, so it is the same on every run. It is not collected from real users, deployed systems or language models. Use it for teaching and for testing audit methods, not for claims about real systems.
