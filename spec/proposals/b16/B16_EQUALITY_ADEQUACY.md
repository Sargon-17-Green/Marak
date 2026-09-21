# B16 Equality Adequacy

**Index equality surface: NOT REQUIRED.**

Same-day/same-index discrimination is expressible from strict total order and the existing binary
alternative.

Conceptual source control:
1. test proposition `A לפני B`;
2. if it holds, execute the BEFORE action;
3. otherwise perform a named decision act;
4. inside that act test `B לפני A`;
5. if it holds, execute the AFTER action;
6. otherwise execute the SAME action.

The branch consequents remain legal atomic act performances; no nested-if parsing convention is
required.

Correctness follows from strict-total-order trichotomy. When neither `A<B` nor `B<A` holds, the
semantic Index Values are equal.

No Boolean runtime Value is produced or stored. The host-language booleans in the reference harness
represent proposition satisfaction only.

Therefore A17's decision not to add `INDEX_A הוא INDEX_B` is semantically adequate.
