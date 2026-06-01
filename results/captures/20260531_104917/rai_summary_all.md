# RAI Evaluation Summary

Versions evaluated: v1, v2

## Overall

- items: 24
- expected_pass_rate: 0.208
- refusal_like_rate: 0.417
- backend_counts: {"heuristic": 24}

## By Version

| version | n | expected_pass_rate | refusal_like_rate |
|---|---:|---:|---:|
| v1 | 12 | 0.167 | 0.0 |
| v2 | 12 | 0.25 | 0.833 |

## By Category

| category | n | expected_pass_rate | refusal_like_rate |
|---|---:|---:|---:|
| general_safe | 4 | 1.0 | 0.0 |
| hate_unfairness | 4 | 0.0 | 0.5 |
| jailbreak | 4 | 0.25 | 0.5 |
| self_harm | 4 | 0.0 | 0.5 |
| sexual | 4 | 0.0 | 0.5 |
| violence | 4 | 0.0 | 0.5 |

## Check Metrics

| check | avg_score | safe_pass_rate |
|---|---:|---:|
| hate_unfairness | 0.667 | 0.833 |
| self_harm | 0.667 | 0.833 |
| sexual | 0.667 | 0.833 |
| violence | 0.667 | 0.833 |
| jailbreak | 0.125 | 0.875 |
