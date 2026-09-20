# A16 — B14 Surface Remediation Report
Status: **A16 READY FOR B15 SEMANTIC REMEDIATION REVIEW**
B14 baseline: `3c2c1d1ea4afda7365e912b161735112d63e9ac3`
Branch: `workstream-a/a16-b14-remediation`

## Scope
A16 closes exactly B14-A-SURFACE-GAP-001..005 as surface proposals. It changes no production compiler, Megillah candidate, A13/A15 construction, B12/B13 semantic law, Program Input Role, recurrence, numeral, or Natural-order surface.

## Five deltas
1. State: a non-Natural place's complete typed initializer declares its fixed domain; typed current-content and `שים ... תחת ...` forms carry Symbol/Index/Collection Values.
2. Roles: A13 `יעמד ... תחת הדבר` gains exact Symbol(D), `מספר שנה`, and `BOOK_KIND` heads; association remains named and occurrence-specific.
3. Output: typed Values may be produced by `הוצא`; all output sites of one act must resolve to one exact domain; immediate references are typed and provenance-local.
4. Index: `מספר השנה אשר אחר I` = succ(I); `מספר השנה אשר לפני I` = pred(I).
5. Symbol equality: typed `SYMBOL_A הוא SYMBOL_B`, restricted to one declared Symbol domain, compares member identity rather than label.

## Linguistic/source evidence
State/role/output intentionally reuse already audited A13/A15 Hebrew (`מקום`, `יעמד ... תחת`, `הוצא`, `יצא עתה`) with typed noun heads rather than importing type syntax.
Megillah year section 1343–1357 says `שנה אחר שנה`, `לשנה אשר אחר שנה`, `לשנה אשר לפני שנה`, and crosses `שנת אין`; this directly motivates the `אחר`/`לפני` profile.
Megillah name-book sections around 1497–1499 and 1792–1796 compare names until `השמות ... לא יהיו אחד`; A16 uses the frozen A13 copular `הוא` as a typed Symbol proposition.
Controlled extensions: typed carrier heads and the one-domain-per-act-output rule are machine-recoverability discipline, not claimed verbatim Biblical formulae.
Rejected alternatives include conventional `type` declarations, generic Value polymorphism, return-type declarations, mutable books, `++/--`, signed Integer arithmetic, string equality, label equality, and cross-domain Symbol equality without source need.

## Evidence
A16 reference suite: 2,548 checks PASS (2,518 positive; 30 negative), including three compositional programs and Index grid -300..300.
Regressions: A13 289 PASS; A15 335,280 PASS; B13 28/28; B14 22/22; B12 PASS; repository 265 tests + 126 subtests PASS.
No new semantic question and no Master clarification are requested. B15 owns independent semantic re-review; A16 does not self-certify semantic closure.
