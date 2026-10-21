# D4 T21 — Luach Seventeen semantic reconstruction

## Authorized source boundary

- Luach Seventeen heading: original line **1165**.
- Executable semantic content: original lines **1167–1247**, excluding organizational headings.
- Separator: original line **1249**, documentary only.
- Luach Eighteen begins at original line **1251** and is a hard stop.
- Live T21 executable replacement: candidate lines **559–594**.

Organizational headings at original lines 1165, 1171, 1201, 1237 and the separator at 1249 are externalized as documentation.

## Core recurrence

Foundation is the middle cutlet gate, `השער התיכון`.

For the nth gate **after** Foundation:
1. action day remains Foundation;
2. query day is exactly the nth day after Foundation;
3. the five established counters are rebuilt for that action/query pair, with the source direction for the after stream;
4. the existing hidden drops, 46 visible drops, bowl initialization, drop-to-bowl mixing and twelve post-drop blends are reused;
5. bowl 1 is queried with seal 1 through the accepted T19 first-answer and direction machinery;
6. T20 `בחירה` selects one of exactly 922 ways without bias;
7. 41 is added, producing a gap in 42..963;
8. that gap advances from the **previous gate position**.

The before-Foundation recurrence is the corresponding backward construction with its own nth-day-before query stream. It is not assigned the after stream's query values or gaps.

## Query day is not gate day

T21 maintains distinct workspaces:
- `יום שאלת השער` moves by exactly one day per ordinal query;
- `השער הנוכחי` moves by the selected inter-gate gap;
- `השער התיכון` remains fixed at Foundation.

This directly preserves original lines 1227–1235. The query day determines the bowl result; it is not itself the gate.

## Constructive unboundedness

The source does not give a finite gate table. `בנה שערים אחרי` and `בנה שערים לפני` accept an arbitrary Natural count and repeat the gate-step recurrence exactly that many times.

Because every selected gap is one of 42..963, every next gate is strictly farther in its direction. Thus finite prefixes can be extended without a source-defined terminal gate.

## Oracle receipts

An independent Python oracle implements the already accepted arithmetic formulas without calling the T21 acts.

First four intervals:
- after Foundation: **[377, 740, 885, 200]**;
- before Foundation: **[762, 513, 584, 808]**.

Cumulative gate positions relative to Foundation:
- after: **[377, 1117, 2002, 2202]**;
- before: **[-762, -1275, -1859, -2667]**.

The receipts confirm the 42..963 bound, strict directional monotonicity, and non-symmetry of the two streams.

## Canonical source names

All multi-word identities introduced for T21 use counted SourceName, including:
- `השער התיכון`
- `יום שאלת השער`
- `השער הנוכחי`
- `תוצאת השער`
- `רווח השער`
- `מענה השער`
- `כיוון השער`
- `בחירת השער`
- `מונה השערים`
- `צעד יום אחרי` / `צעד יום לפני`
- `צעד שער אחרי` / `צעד שער לפני`
- `חשב מוני שער`
- `אתחל שערים`
- `אתחל שאלת שער`
- `חשב רווח שער`
- `השער הבא אחרי` / `השער הבא לפני`
- `בנה שערים אחרי` / `בנה שערים לפני`.

No welded multi-word identity is introduced.

## Verification receipt

Final executable/evidence HEAD: `76b895877b81614980c7edf5e4a4885b836d929e`.

GitHub Actions:
- push #578 / `37238924835`: **19/19 SUCCESS**;
- PR #579 / `37238927963`: **19/19 SUCCESS**;
- focused T21: **5/5 PASS** Ubuntu, **5/5 PASS** Windows;
- T19 regression: **4/4 PASS** on both;
- T20 regression: **4/4 PASS** on both;
- D3+D4: **101/101 PASS** on both;
- core: **635 passed, 126 subtests passed**;
- A13: **289 checks PASS**;
- semantics suite and post-M2 regressions: **PASS**.

Final candidate:
- SHA-256: `6fda03c4ca953898b471da666c048d81020f9bea4fcd240b94aab7bb3f091881`;
- normalized tokens: **75,245**;
- frontier: **71,871**;
- candidate line: **598**;
- mapped original line: **1251**;
- next source boundary: **Luach Eighteen / Year Five Thousand**.

The final two descendants before acceptance were test-only fixture remediations: first removing an unnecessarily expensive full-pipeline three-runtime fixture while preserving oracle + production-bridge coverage, then correcting the feminine count surface required before `פעמים`. Neither changed candidate bytes or T21 semantics.

## Classification

`SOURCE_REPAIR_ONLY / CURRENT_LANGUAGE_ALREADY_SUFFICIENT`.

No parser, grammar, registry, HAST, IR, artifact schema, semantic type, identity family, or compiler change is required.

T22 / Luach Eighteen was not started.
