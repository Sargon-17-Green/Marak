# A15 — Anti-Imitation Audit

Status: PASS for the proposal surface.

| Need | A15 construction | Conventional feature deliberately not imported | Why the surface is source-driven |
|---|---|---|---|
| calendar labels | finite `משפחת שמות` + counted visible label metadata | string / enum / interned identifier | Megillah outputs closed named cutlet/month families |
| years across an origin | `שנת אין`, `N שנים לפני/אחרי שנת אין` | signed Integer | source itself describes an origin and years before it |
| finite ordered runtime data | typed immutable `ספר` | mutable list / array / vector | Megillah repeatedly constructs, traverses and orders books |
| ordinal selection | `מספרו בסדר הספר` | `a[i]`, zero-based index | source speaks in first/next/last ordered-book relations |
| numeric comparison | `A רב מן B` | symbolic `>` / Boolean | direct Biblical comparative frame and Megillah need |
| large constants | productive Biblical magnitude phrases | decimal machine literal | source already writes Biblical numerals |
| exact recurrence | `N פעמים A`; `פעמים כמספר VALUE A` | `for` loop / loop variable | source repeatedly uses `פעמים` counts |
| external values | `דבר` belonging to `המלאכה הזאת` | argv/stdin/function parameters | source explicitly defines two named inputs to the whole work |

## Additional checks

Symbol labels are not secretly Text because no runtime operation receives the word sequence; it is presentation metadata on an atomic member. The word count exists only to make the declaration recoverable under the Charter.

Collection append is a pure Value description. Any later state replacement remains explicit; no list mutation semantics are inferred from `ספר`.

Declared Symbol order is a static relation over semantic member identities, not a comparator callback. Natural ordering is the admitted B13 strict relation, not host numeric ordering by implementation convention.

Program Input Roles reuse the independently justified A13 identity-addressed role idiom but do not turn the whole program into a conventional function. `המלאכה הזאת` has no callable identity and no positional parameter list.

No A15 family relies on punctuation, indentation, Unicode formatting, quoted literal boundaries, or host-language operator precedence.
