# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 5 |
| Generation Failure | 1 |

## Failure Counts By Slice

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 4 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 1 |
| No Failure | 1 |

## Failure Counts By Version

### v1

| failure_category | count |
|---|---:|
| No Failure | 5 |
| Generation Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Generation Failure | No clear deterministic category dominated; defaulting to generation issue. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
