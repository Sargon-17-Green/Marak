# B16 Observable Behavior

Observable behavior remains B12+B13+B15:

- exact semantic `BidirectionalIndex` Value: BeforeZero(n), ZeroIndex, or AfterZero(n);
- proposition satisfaction through consequent control effects;
- state/replacement behavior;
- named-role association behavior;
- act output and immediate-result provenance;
- InvalidProgram / InvalidInvocation / RuntimeError / Divergence outcomes already defined.

Not observable:
- whether the source Value originated in year or general profile;
- any runtime profile tag;
- parser/HAST node class;
- source spelling after semantic lowering;
- Python/C class;
- host sign/magnitude representation;
- memory/object identity;
- stack frame;
- result register.

A source-preserving formatter may observe stored source provenance as a tooling concern. That does not
make profile provenance observable to a running Marak program.
