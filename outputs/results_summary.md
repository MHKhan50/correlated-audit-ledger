# Experiment summary

Synthetic benchmark only; results are not evidence about real systems or LLMs. Test seeds: 44 and 55.

| Missing | Shared outage | Rule | F1 mean | Recall mean | FPR mean | Weighted cost mean |
|---:|---:|---|---:|---:|---:|---:|
| 0.05 | 0.00 | cost_tuned | 0.897 | 0.978 | 0.112 | 28.0 |
| 0.05 | 0.00 | optimistic_missing | 0.919 | 0.927 | 0.050 | 40.5 |
| 0.05 | 0.00 | score_threshold | 0.744 | 0.607 | 0.002 | 174.0 |
| 0.05 | 0.00 | strict_complete | 0.632 | 0.463 | 0.000 | 237.5 |
| 0.05 | 0.10 | cost_tuned | 0.798 | 0.791 | 0.105 | 109.5 |
| 0.05 | 0.10 | optimistic_missing | 0.815 | 0.746 | 0.047 | 120.0 |
| 0.05 | 0.10 | score_threshold | 0.656 | 0.497 | 0.002 | 222.8 |
| 0.05 | 0.10 | strict_complete | 0.561 | 0.390 | 0.000 | 270.0 |
| 0.05 | 0.25 | cost_tuned | 0.699 | 0.634 | 0.096 | 178.0 |
| 0.05 | 0.25 | optimistic_missing | 0.702 | 0.589 | 0.047 | 190.0 |
| 0.05 | 0.25 | score_threshold | 0.548 | 0.385 | 0.002 | 272.8 |
| 0.05 | 0.25 | strict_complete | 0.460 | 0.300 | 0.000 | 310.0 |
| 0.15 | 0.00 | cost_tuned | 0.895 | 0.939 | 0.087 | 41.5 |
| 0.15 | 0.00 | optimistic_missing | 0.895 | 0.865 | 0.037 | 66.0 |
| 0.15 | 0.00 | score_threshold | 0.663 | 0.514 | 0.002 | 215.2 |
| 0.15 | 0.00 | strict_complete | 0.530 | 0.361 | 0.000 | 282.5 |
| 0.15 | 0.10 | cost_tuned | 0.793 | 0.757 | 0.084 | 121.0 |
| 0.15 | 0.10 | optimistic_missing | 0.791 | 0.695 | 0.034 | 140.5 |
| 0.15 | 0.10 | score_threshold | 0.585 | 0.423 | 0.002 | 255.2 |
| 0.15 | 0.10 | strict_complete | 0.474 | 0.311 | 0.000 | 305.0 |
| 0.15 | 0.25 | cost_tuned | 0.691 | 0.628 | 0.102 | 181.5 |
| 0.15 | 0.25 | optimistic_missing | 0.680 | 0.549 | 0.034 | 205.5 |
| 0.15 | 0.25 | score_threshold | 0.482 | 0.325 | 0.002 | 299.0 |
| 0.15 | 0.25 | strict_complete | 0.383 | 0.238 | 0.000 | 337.5 |
| 0.30 | 0.00 | cost_tuned | 0.841 | 0.949 | 0.171 | 50.0 |
| 0.30 | 0.00 | optimistic_missing | 0.848 | 0.769 | 0.025 | 106.5 |
| 0.30 | 0.00 | score_threshold | 0.515 | 0.362 | 0.000 | 282.5 |
| 0.30 | 0.00 | strict_complete | 0.361 | 0.220 | 0.000 | 345.0 |
| 0.30 | 0.10 | cost_tuned | 0.784 | 0.757 | 0.096 | 123.0 |
| 0.30 | 0.10 | optimistic_missing | 0.749 | 0.622 | 0.022 | 171.0 |
| 0.30 | 0.10 | score_threshold | 0.437 | 0.288 | 0.000 | 315.0 |
| 0.30 | 0.10 | strict_complete | 0.306 | 0.181 | 0.000 | 362.5 |
| 0.30 | 0.25 | cost_tuned | 0.679 | 0.594 | 0.084 | 193.5 |
| 0.30 | 0.25 | optimistic_missing | 0.636 | 0.487 | 0.022 | 231.0 |
| 0.30 | 0.25 | score_threshold | 0.361 | 0.227 | 0.000 | 342.5 |
| 0.30 | 0.25 | strict_complete | 0.256 | 0.147 | 0.000 | 377.5 |
