# B16 Distance Algorithm Boundary

**DIRECT INDEX DISTANCE SURFACE — REJECTED / REMAINS ALGORITHMIC**

B13 may define `distance(i,j)` mathematically and use it as a reference theorem/operation. That does
not justify a source primitive.

The Megillah explicitly requires counting the days between positions. A direct distance construction
would remove meaningful source computation in the same way that compiler magic for an operation
defined by the source would erase the source's own algorithm.

## Constructive adequacy proof

Exact distance is writable using only admitted capabilities:

1. classify direction with strict order:
   - if `A לפני B`, choose forward stepping;
   - otherwise perform a named decision act:
     - if `B לפני A`, choose backward stepping;
     - otherwise the values are the same Index.
2. retain a current Index and a Natural count initially zero.
3. forward action: replace current by `succ(current)`, then increase the Natural count by one.
4. backward action: replace current by `pred(current)`, then increase the Natural count by one.
5. repeat the selected named step act using existing post-action recurrence.
6. forward positive stop proposition after each step:
   `TARGET לפני succ(CURRENT)`.
   It is false while CURRENT is still before TARGET and becomes true exactly when CURRENT = TARGET.
7. backward positive stop proposition:
   `pred(CURRENT) לפני TARGET`.
   It is false while CURRENT is still after TARGET and becomes true exactly when CURRENT = TARGET.
8. same-position branch leaves the count at zero.

Thus no Index equality, negation Value, direct distance, implicit conversion, or signed arithmetic is
needed. The algorithm is finite because each step moves exactly one position toward the target.

The reference suite differentially checks this construction against B13 `distance` across a broad
Before/Zero/After grid.
