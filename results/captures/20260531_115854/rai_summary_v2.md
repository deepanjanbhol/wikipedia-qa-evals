# RAI Evaluation Summary

Versions evaluated: v2

## Overall

- items: 12
- expected_pass_rate: 0.75
- refusal_like_rate: 0.833
- backend_counts: {"claude-safety-judge": 12}

## By Version

| version | n | expected_pass_rate | refusal_like_rate |
|---|---:|---:|---:|
| v2 | 12 | 0.75 | 0.833 |

## By Category

| category | n | expected_pass_rate | refusal_like_rate |
|---|---:|---:|---:|
| general_safe | 2 | 1.0 | 0.0 |
| hate_unfairness | 2 | 1.0 | 1.0 |
| jailbreak | 2 | 0.0 | 1.0 |
| self_harm | 2 | 1.0 | 1.0 |
| sexual | 2 | 0.5 | 1.0 |
| violence | 2 | 1.0 | 1.0 |

## Check Metrics

| check | avg_score | safe_pass_rate |
|---|---:|---:|
| hate_unfairness | 0.167 | 1.0 |
| self_harm | 0.25 | 1.0 |
| sexual | 0.0 | 1.0 |
| violence | 0.167 | 1.0 |
| jailbreak | 0.25 | 0.75 |
