# Source-map model

Source mapping is created during normalization and survives every later representation by provenance references.

## Coordinates

`OriginalPoint` stores file, Unicode-code-point character offset, UTF-8 byte offset, 1-based line, and 1-based code-point column.  Spans are half-open `[start,end)`.

CRLF is counted as one line break.  Columns are code-point columns, not display-cell or grapheme columns; an LSP adapter can convert to UTF-16 positions later without changing language semantics.

## Mapping units

There is exactly one `MapUnit` per normalized code point.  A preserved Hebrew letter maps to its original one-code-point span.  A collapsed normalized space maps to the complete original whitespace/gap region, including transparent decorations between whitespace characters.

Non-empty normalized spans begin at the first participating unit and end at the last participating unit, so trailing Markdown decoration is not falsely highlighted.  A zero-width point at normalized EOF maps to physical source EOF so an EOF diagnostic is located correctly even after a transparent suffix.

## Deletions

Transparent ranges not absorbed into a whitespace provenance span are retained as `DiscardedSpan` records for explain/debug tooling.  Deleted characters never become grammar.
