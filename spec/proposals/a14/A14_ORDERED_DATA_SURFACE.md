# A14 — Ordered Finite Data Surface

Status: **PREFERRED_SURFACE_CANDIDATE / AWAITING_B_SEMANTICS**

## Need

The Megillah builds and compares finite runtime structures whose order is semantically observable:
candidate years, books of month lengths, books of month names, permutations and weavings.

The need is not "an array". It is:

> a finite group of runtime items with an explicit order, for which source computations can identify
> members and order-relative items such as the first, successor and last.

## Existing source vocabulary

The month-name algorithm already says:

- `ספר שמות חודשים`;
- `השם אשר בראש`;
- `השם אשר אחריו`;
- `החודש האחרון`;
- `ערוך את כל הספרים`.

The word `ספר` is therefore a strong candidate for an explicitly ordered data object rather than
treating every plural noun as a collection.

Biblical Hebrew independently supports the membership relation `כתוב בספר`.

## Preferred relational surface family

The exact mutation/construction verbs await B, but A recommends the following semantic heads:

- collection identity: `הספר אשר שמו NAME`;
- membership: `הדבר אשר כתוב בספר ...`;
- first: `הדבר אשר בראש הספר ...`;
- successor: `הדבר אשר אחריו בספר ...`;
- last: `הדבר האחרון אשר בספר ...`.

The phrases must identify the element type where needed; bare `דבר` above is schematic.

## Operations that are NOT requested merely by analogy

A14 does not request:
- numeric indexing;
- zero-based or one-based indexing;
- random access;
- slicing;
- capacity;
- machine-contiguous storage;
- map/dictionary keys;
- implicit iteration protocol.

A count of members may be added only where an actual algorithmic use requires it.

## Creation / addition

A cannot freeze `כתוב בספר ...` as a mutating append operation until B decides whether:
- a book is persistent or changeable;
- adding an item creates a new book or changes the current one;
- duplicates are legal;
- empty books exist;
- construction is incremental or declarative.

Any eventual source must say the order relation explicitly. Textual order of declarations is not
automatically collection order.

## Selection

`בחר אחת מן ...` is source evidence for selection from a finite candidate relation, but B must define
what value/referent is selected and how the choice operation receives its candidate set.

A14 does not turn `בחר` into a generic library API prematurely.

## B dependencies

Required semantic answers:
1. collection identity/value model;
2. finite order model;
3. mutability/persistence;
4. duplicate-element behavior;
5. empty/singleton behavior;
6. element-type/domain rules;
7. whether first/successor/last are partial queries and how absence fails;
8. whether selection consumes a collection Value or another candidate relation.


## B13 reconciliation

B13 selects an immutable finite ordered homogeneous Collection value, recursively nestable, with
positive positions 1..count, pure append, first/next/nth selection, traversal and ordering by an
admitted strict total relation.

This validates `ספר` as the leading A14 surface family but changes an important detail: source wording
must not imply in-place mutation of a book. Any eventual `כתוב בספר` action must either construct a new
book value or explicitly replace a state-bearing referent containing one. A14 therefore does not freeze
an append verb until the A/B integration wording audit is complete.
