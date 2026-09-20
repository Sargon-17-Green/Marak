# B14 Backward Compatibility

Every accepted A13/B12 program that uses no A15/B13 construction must retain identical meaning.

Sensitive-term audit:
- `שם`: Symbol use requires full domain-qualified construction; no bare-name runtime value.
- `ספר`: A15 requires typed book frames; no mutable-list or source-order rule.
- `אין`: no standalone null/zero; only typed year origin and typed empty-book clauses.
- `מספר`: frozen NumberValue remains Natural; `מספר השנה` is a distinct typed head.
- `דבר`: Program Input owner is `המלאכה הזאת`, distinct from named-act role owner.
- `המלאכה הזאת`: whole-program contract only, never implicit main.
- `פעמים`: A15 extends counted morphology/dynamic profile without changing prior admitted forms.

No punctuation/layout/source-order semantics are introduced. No old numeric place, role, or output is
reinterpreted as a generic carrier. B14 finds no backward-semantic regression in the proposal design.
