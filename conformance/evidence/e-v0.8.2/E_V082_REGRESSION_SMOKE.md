# E v0.8.2 Regression Smoke

E reused the already-independent v0.8.1 checks against C M4.2 rather than reopening the full v0.8 research program.

- E-FIND-021: source-semantic public observation remains invariant under internal place/act/role/occurrence renumbering; same spelling across semantic kinds remains distinct.
- E-FIND-022: `ועתה` in explicit name slots without a true principal transition yields missing-root diagnostics; two actual top-level transitions yield multiple-root diagnostics.
- E-FIND-024: all eight malformed artifact/IR reproducers remain rejected pre-execution by the semantic verifier; valid compiler artifacts remain accepted.
- E-FIND-025: caller-role→callee-role value transfer returns 5; association order remains non-positional; same-spelling cross-owner roles, A→B→C role context and recursive role context pass.
- Anti-imitation smokes remain PASS: output≠return, proposition≠Boolean value, post-action recurrence≠while, no hoisting, roles≠positional args, no HALT primitive, natural underflow≠signed promotion.

Focused reused regression total: **23/23 PASS**.
