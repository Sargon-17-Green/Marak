# C M4.2 Remediation Summary

**Implementation status: COMPLETE locally, pending independent E/Master confirmation.**

C M4.2 is a focused remediation over unchanged A13/B12 semantics.

E-FIND-023: the former fixed default active-performance quota of 10,000 was removed from the HAST reference evaluator, IR reference evaluator and portable backend. Default is `None`, meaning no artificial performance-count/depth ceiling. An explicitly supplied `max_active_performances=N` remains a caller/harness control only. Finite depth 20,000 and 20,001 sequential performances were exercised successfully; no-fuel infinite recursion remains active until external timeout.

E-FIND-027: canonical source metadata was cleaned for future repository bootstrap. Current metadata is Marak / `marak` / 0.4.2-alpha.1 / MIT. Stale source-root handoff manifests, checksum ledgers, old wheel references, handoff input/evidence directories and temporary build debris were removed or moved outside the canonical source tree; historical milestone documentation is explicitly archived.

No language feature or A13/B12 semantic rule was added or changed.
