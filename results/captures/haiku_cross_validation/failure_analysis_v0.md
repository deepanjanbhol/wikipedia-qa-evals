# Failure Analysis

## Failure Counts

| failure_category | count |
|---|---:|
| No Failure | 4 |
| Generation Failure | 1 |
| Multi-Hop Failure | 1 |

## Failure Counts By Slice

### multi_hop

| failure_category | count |
|---|---:|
| No Failure | 3 |
| Multi-Hop Failure | 1 |

### simple_factoid

| failure_category | count |
|---|---:|
| Generation Failure | 1 |
| No Failure | 1 |

## Failure Counts By Version

### v0

| failure_category | count |
|---|---:|
| No Failure | 4 |
| Generation Failure | 1 |
| Multi-Hop Failure | 1 |

## Example Failures

| id | slice | failure_category | explanation | suggested_fix |
|---|---|---|---|---|
| sf_01 | simple_factoid | Generation Failure | Retrieved evidence appears adequate but generated answer quality is low. | Tighten answer prompt for directness and verify output format plus relevance constraints. |
| mh_01 | multi_hop | Multi-Hop Failure | Multi-hop linkage appears incomplete or incorrectly composed. | Force explicit sub-question decomposition and step-wise evidence chaining before synthesis. |
