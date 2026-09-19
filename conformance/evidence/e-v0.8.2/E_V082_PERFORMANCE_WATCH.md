# E-FIND-026 Parser Performance Watch

Status remains **INFORMATIONAL / WATCH**.

M4.2 focused 128-action shape:
- 2701 tokens;
- 7607 parser state keys / derivations;
- 771 completed nodes;
- 1 semantic alternative;
- peak 20 state keys at one chart position;
- tracemalloc peak ~11.16 MB;
- two completed E measurements: ~17.77 s and ~17.51 s.

For context, E v0.8 recorded ~18.97 s and E v0.8.1 recorded ~13.39 s for the same shape. Timing variance is substantial; the structural metrics remain stable and there is no ambiguity/state explosion or semantic pruning. No new performance finding is opened.
