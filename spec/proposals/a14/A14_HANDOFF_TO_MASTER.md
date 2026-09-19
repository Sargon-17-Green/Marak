# A14 — Handoff to Master

Status: **A14 READY FOR A/B INTEGRATION REVIEW**

## Baseline

A14 was prepared from canonical `main` after D2 integration.

A13 frozen documents were not modified in place. All proposal work is under:

    spec/proposals/a14/

## Disposition

### SURFACE_READY
- D-LANGUAGE-REQUEST-004 — strict numeric ordering:
      A רב מן B
- D-LANGUAGE-REQUEST-005 — productive direct Naturals through 99,999,999.

### PARTIALLY SURFACE_READY / AWAITING_B
- D-LANGUAGE-REQUEST-006:
  - written exact count `REPEAT_COUNT פעמים ATOMIC_ACTION`: surface-ready and preserves A3 direction;
  - runtime-derived count wording: awaiting B semantics before syntax freeze.

### AWAITING_B integration acceptance
B13 semantic research exists and was reviewed; these remain proposal-level until joint A/B acceptance:
- 001 runtime symbolic names;
- 002 year-number relation across zero;
- 003 ordered finite runtime data;
- 007 external input binding.

## Preferred semantic direction sent to B

- closed Name/Symbol Value before general Text;
- year-relative domain before general Integer;
- ordered `ספר` relations before array/list API;
- counted recurrence observes one Natural count once;
- external bindings established by explicit source identity during preparation.

These are recommendations, not semantic decisions by A.

## No Master clarification currently requested

A found no binary language-policy question that must be decided before B can analyze the remaining
semantic dependencies.

## Numeral coverage

A14's proposal covers direct positive Naturals 1..99,999,999 and therefore the Megillah's fixed
14,777,149 value.

The historical `רבבה` spelling family is not added as an alias; controlled canonicalization uses one
`אלף`/`אלף אלפים` grammar.

## Safety against feature creep

A14 does not add:
- general strings;
- generic signed integers;
- arrays or indexing;
- Boolean Values;
- symbolic comparison operators;
- a `for` primitive or loop index;
- stdin/argv;
- positional arguments.

## Next action

Master should review A14 together with the existing B13 proposal. The semantic research pass is already
complete on both sides; the next step is A/B integration acceptance and final wording for the dependent profiles.

Do not merge these proposals as a frozen language edition merely because the A14 branch is green.


## Final integration verification

- canonical main after required rebase: `45ac2aebe391f7aa83792e1e501dcd69da884710`;
- B13 proposal reviewed: `3c47a57debd381c2b4e41d00d12c792ae43debe8`;
- A14 direct surface checks: **302 PASS**;
- negative fixtures: **24**;
- explicit ambiguity-focus fixtures: **4** plus punctuation/attachment negatives;
- numeral collision generation: **300,000** direct + **300,000** repeat-count checks;
- complete Megillah census: **453 numeral-bearing lines**, **96** `פעמים` tokens on **92** lines;
- `פעמים` census classification: **63 literal-count**, **23 runtime-count**, **10 other uses**;
- repository suite after rebase: **262 passed, 2 deselected, 126 subtests passed**.

Both deselections are baseline Windows portability checks unrelated to A14:
1. `dump_current_registry.py` prints a Windows path while one assertion requires a forward-slash suffix;
2. a static audit compares registry snapshot bytes and observes CRLF in the Windows working-tree current
   registry versus LF in the frozen A13/B12 snapshot.

A14 does not modify either tool/test or the construction registries.

## B13 reconciliation

B13's proposed semantics match A14's independently chosen directions for requests 001–006. Request
007 caused one correction: external bindings are Program Input Roles, **not mutable places**. See
`A14_B13_RECONCILIATION.md`.
