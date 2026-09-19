# A14 — Anti-Imitation Audit

| Request | Need | Candidate construction/model | Familiar analogue | Independent justification | Primary risk |
|---|---|---|---|---|---|
| 001 | calendar label as runtime result | closed runtime `שם` datum, explicit declaration/reference | string / enum | source explicitly computes month/cutlet names; arbitrary text operations are not requested | accidentally turning source identifiers into strings; multiword literal boundaries |
| 002 | years before a zero-year origin | `שנת אין` plus explicit `לפני` relation | signed integer | source itself numbers years relationally around `שנת אין`; generic integer arithmetic is not required | confusing year origin with numeric zero or null |
| 003 | finite observable order among runtime items | explicit `ספר` with membership/head/successor/last relations | list / array | the Megillah itself speaks of books, head, following item, last item and ordered books | importing indexing/mutability API |
| 004 | strict numeric comparison | `A רב מן B` | `A > B` | direct Biblical comparative `רב ... מן`; operand roles are visible in words | treating proposition as Boolean Value; admitting loose aliases |
| 005 | direct large written numbers | descending additive/multiplicative Biblical scale grammar | integer literal | Biblical large-number phrases use `אלף`, hundreds of thousands and `אלף אלפים`; no digits/place notation | overgenerating variants or Modern-Hebrew scale forms |
| 006 | exact finite action count | `REPEAT_COUNT פעמים ATOMIC_ACTION`; dynamic evidence `פעמים כמספר VALUE` | `for` loop | Biblical and Megillah action+`פעמים` wording is direct; no iterator/index variable is implied | hidden repeated-span attachment; runtime count evaluation convention |
| 007 | two externally supplied semantic inputs | preparation-level named external establishment | parameters / stdin / argv | source says two days are given/taken and assigns explicit meanings; transport is irrelevant | positional host binding or synthetic `main` |

## Request 001

The audit rejects "we need strings because programming languages have strings." The actual need is
closed symbolic labels that can appear in results. General strings remain unjustified.

## Request 002

The audit rejects automatic promotion of the A13 Natural universe to Integers. The source's strongest
native model is chronological relation to a zero-year designation.

## Request 003

The audit rejects looking for a Biblical word meaning array. `ספר` is considered because the source
already uses it as the object in ordered-data operations. Indexing is deliberately absent.

## Request 004

Similarity to `>` is convergence. The chosen relation is independently ordinary Biblical comparison.

## Request 005

The grammar is not decimal syntax written in words: its admitted forms are scale phrases with Biblical
morphology, including `אלף אלפים`.

## Request 006

No loop index, iterator object or mutation counter is introduced. The only required meaning is exact
repetition of one linguistically bounded action.

## Request 007

The program interface is not modeled as a function parameter list. It extends preparatory discourse
with explicit externally established identities.

## Final question

For the surface-ready profiles — numeric order, productive numerals and written-count recurrence — a
Biblical-Hebrew reader can recover the computational relation from the words without knowing a modern
programming convention.

For 001/002/003/dynamic-006/007, B13 now proposes a precise semantic object. A14 therefore evaluates those
models as matching its independent directions, but does not freeze final wording until A/B integration acceptance.
