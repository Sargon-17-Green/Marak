# D4 T20 — Luach Sixteen semantic reconstruction

## Authorized source boundary

- Luach Sixteen heading: original line 999.
- Semantic content: original lines 1001–1161, excluding seven organizational headings.
- Separator: original line 1163, documentary only.
- Luach Seventeen begins at original line 1165 and is a hard stop.
- Live T20 executable replacement: candidate lines 507–555.

Organizational headings at original lines 999, 1011, 1051, 1081, 1107, 1119, and 1151 are externalized as documentation.

## Purpose and invariants

Luach Sixteen is a general, bias-free selector for choosing exactly one דרך from N = מספר הדרכים. It must not be specialized to one future caller and must not replace the six-bowl arrangement mechanism.

The central invariant is rejection before one-based remainder mapping: only a prefix whose size is exactly divisible by N may participate in selection.

## Branch A — N <= M

Let M = המספר הגדול.

1. Compute האחרון אשר ילקח = M - (M mod N) using the already admitted source-authorized הנותר בדרך הקצרה.
2. Start from מספר המענה האחד.
3. While the current answer is greater than the threshold, advance using the fixed Luach Fifteen direction and cyclic answer rule.
4. Map the first accepted answer to ((a-1) mod N)+1.

The focused oracle proves equal bucket size L/N, exact divisor handling, N=1, boundary mapping, and forward/backward rejected-tail traversal.

## Branch B — N > M

1. Starting from k=1, W=M, multiply by M until W>=N. This yields the smallest positive מספר המקומות = k and exact מספר כל היוצאים = M^k.
2. Take exactly k successive Luach Fifteen answer numbers in the fixed direction.
3. Subtract one from each answer to obtain digits in 0..M-1.
4. Form המספר הרחב האחד = 1 + sum(d_i*M^(i-1)).
5. Later wide numbers move by one in the same direction, wrapping W→1 forward and 1→W backward.
6. Compute האחרון הרחב אשר ילקח = W - (W mod N).
7. Reject wide values above that threshold, then map the first accepted value to ((w-1) mod N)+1.

The implementation uses exact Natural arithmetic. No floating-point logarithm, host integer cap, or שמור truncation is used for N, M^k, capacities, or wide thresholds.

## Canonical source names

The six source-declared multi-word identities are represented with counted SourceName:

- מספר הדרכים
- האחרון אשר ילקח
- מספר המקומות
- מספר כל היוצאים
- המספר הרחב האחד
- האחרון הרחב אשר ילקח

No welded aliases are introduced.

## Relation to T19 and bowl state

T20 reuses חשב מענה הבא from T19 and does not redefine answer direction. Focused three-runtime tests preserve מלא הקערות, מערכת הטיפה האחרונה, and המערכה הנוכחית.

The generic T20 block contains no bowl-state or six-bowl arrangement machinery. The original exclusion at lines 1159–1161 is retained as a structural invariant: six-bowl arrangements remain governed by Luach Eleven and Luach Fourteen.

## Verification receipt

Accepted executable/evidence head: 86ebc611a56cd96d85a27ff0078bde27bddaed5e.

GitHub Actions:
- push run 37171652776 (#568): SUCCESS;
- PR run 37171656172 (#569): SUCCESS;
- focused T20: 4 passed on Ubuntu and 4 passed on Windows;
- focused T19 regression: 4 passed on Ubuntu and 4 passed on Windows;
- combined D3+D4: 96 passed on Ubuntu and 96 passed on Windows;
- core: 630 passed, 126 subtests passed;
- A13 selftest: 289 checks PASS;
- C5.7 multi-word SourceName job: PASS on both OS;
- post-M2 proposal/semantics regressions: PASS.

Final executable candidate measurement:
- candidate SHA-256: 4aebd9cdac116fa1c1c931d51bf4fe56ae15ac5a998e09a752dcbb06049e340a;
- original SHA-256: 7b834f4a444e021bb65164282b851af960a6dbc0be3d458c2412181773b9db7b;
- normalized tokens: 68,973;
- syntactic frontier: 65,148;
- candidate line: 559;
- mapped original line: 1165;
- diagnostic: PARSE0002;
- next source boundary: Luach Seventeen / שערי הקציצה.

## Classification

SOURCE_REPAIR_ONLY / CURRENT_LANGUAGE_ALREADY_SUFFICIENT.

No parser, grammar, registry, HAST, IR, artifact schema, semantic type, identity family, or compiler change is required.

T21 / Luach Seventeen was not started.