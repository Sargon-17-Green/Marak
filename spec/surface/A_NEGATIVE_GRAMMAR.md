# A_NEGATIVE_GRAMMAR.md

Status: A12 FROZEN CORE

# 1. Lexical/layout leakage

Reject any distinction created only by punctuation, Markdown, line breaks or indentation.

# 2. Sequence leakage

Reject adjacent A B as ordered sequence when no admitted temporal relation says so.

Bare waw is not the universal sequence relation.

# 3. Reference leakage

Reject:
- bare names as references/calls;
- nearest antecedent;
- nearest noun;
- implicit dereference;
- caller-chain dynamic lookup;
- free last-result lookup;
- automatic shadowing.

# 4. Body boundaries

Reject:
    זה דבר המעשה אשר שמו ראובן
    BODY
    עד הנה דבר המעשה אשר שמו שמעון

Reject a body ended only by formatting or by the next definition.

Reject a semantically empty generic END.

# 5. Arithmetic

Reject missing `על` in addition or missing `מן` in subtraction.

Reject `שוה` as Core exact equality.

Reject `אפס` as Core cardinal zero.

# 6. Condition

Reject ambiguous nested:
    אם P אם Q A ואם לא B ואם לא C

No nearest-if rule.

# 7. Recurrence

Reject:
    A עד אשר P
as the frozen recurrence construction.

Reject:
    A וכן עשה עד אשר P
as canonical Core recurrence; the frozen instructional form is `וכן תעשה`.

Reject interpreting `A ואחרי כן B וכן תעשה...` as repetition of both A and B.

# 8. Input roles

Reject:
- two actual Values with no named role associations;
- missing required association;
- two Values for one role;
- undeclared role;
- positional matching;
- hidden parameter cell semantics;
- implicit caller aliasing.

# 9. Current performance

Reject computational `המעשה הזה` outside an executing act body.

Reject exposing stack-frame identity as its meaning.

# 10. Results — A12 correction

Reject implicit last-expression result.

Reject output implying termination.

Reject a second:
    הוצא מן המעשה הזה ...
in the same Core v0.1 performance path.

Core v0.1 has at most one numeric result.

Reject ordinal/positional multi-result access as Core v0.1; A11's first/second-result scheme is
superseded.

Reject result reference after another executable caller action intervened.

# 11. State

Reject using `המקום אשר שמו X` where a numeric Value is required.

Reject `המספר אשר שמו X` as mutable state identity.

Reject latest-write-wins semantics for `כתוב` unless explicitly established by a future language rule.

# 12. Conventional-language leakage

Reject any semantics justified only by:
- variable;
- function;
- parameter;
- return;
- stack;
- while;
- tuple;
- statement;
- expression;
as familiar programming-language defaults rather than Hebrew/source requirements.

# A13 integration negatives

## Program composition
Reject a complete Core document with no top-level `ועתה`, with more than one top-level `ועתה`, or
with an introduction/definition after `ועתה`.

Reject two independent top-level executable actions with no `ואחרי כן`. Newline, punctuation or
source order do not supply execution order.

## Visibility/lifetime
Reject a place/act/role reference before its introduction. Reject duplicate same-kind place or act
introduction and duplicate role within one owner. Reject role declaration before its owner or after
the owner's body definition. Reject performance-relative role value outside the performance.

## Body boundary
A body closes only at `עד הנה דבר המעשה אשר שמו NAME` with the matching name. A following definition,
heading, blank line or punctuation is not a closer.

## HALT leakage
Reject treating non-frozen `חדל מעשות...`, `HALT`, `exit`, or an equivalent phrase as a Core primitive.
Proof-model HALT maps to ordinary language completion.

## Natural subtraction
Reject an alleged negative Core literal such as `המספר אשר הוא מינוס אחד`. When A>B in admitted
`גרע A מן B`, no negative Core Value is created; B12 supplies the defined failure semantics.
