# C5.7 — Baseline Receipt

Workstream: C5.7 — Multi-word Declared Source Names Production Integration

Canonical baseline:
`5679fbe861bc2d30aba479e32fd042bf196295ca`

Baseline verification:
- `main` is exactly the canonical baseline above at workstream creation time.
- This baseline is the Master merge of B17.
- A18 and B17 are already Master-accepted and merged.
- C5.1–C5.6 are historical accepted/merged Workstream C stages and are not reopened.
- No prior C branch is reused.

Normative route:
`D4-LANG-002 → A18 → B17 → C5.7`

Production contract source:
- `spec/proposals/b17/B17_C5_7_IMPLEMENTATION_REQUIREMENTS.md`
- `spec/proposals/b17/B17_HANDOFF_TO_MASTER.md`
- `spec/proposals/a18/A18_MULTIWORD_SOURCE_NAMES.md`
- `spec/proposals/a18/A18_NAME_SITE_INVENTORY.md`

Initial scope:
- implement the accepted two-form SourceName consistently at every A18 name role;
- canonicalize counted payload words to one U+0020-separated spelling before semantic resolution;
- preserve existing namespaces, owners, declaration-before-use and typed resolution behavior;
- keep count/frame out of semantic identity;
- do not introduce runtime names, aliases, longest-match, declaration-known tokenization or expected-type rescue;
- bump compiler/package and construction registry only as required by B17;
- do not edit Megillah.

This receipt is intentionally documentation-only and exists to establish the fresh C5.7 branch and Draft PR before production changes.
