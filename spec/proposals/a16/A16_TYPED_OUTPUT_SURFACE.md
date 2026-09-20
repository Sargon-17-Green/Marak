# A16 — Typed Act Output and Immediate Result
Status: proposal delta for B15 review; A13 numeric output remains unchanged.

## Output action
The existing action is retained: `הוצא מן המעשה הזה את TYPED_VALUE`.
`TYPED_VALUE` may now independently be Symbol(D), BidirectionalIndex, or admitted Collection<D>, in addition to Natural.
`הוצא` establishes a product of the current occurrence and does not terminate the act.

## Output-domain discipline
A16 adds no return-type declaration. The resolved body must make every source `הוצא` site of one act denote the same exact semantic domain D.
Mutually exclusive paths do not license different domains. Zero output sites mean no result domain; zero output on a runtime path remains possible under the existing zero/one rule.
A second output in one occurrence is invalid exactly as before.

## Immediate result
Symbol(D): `השם אשר במשפחת השמות אשר שמה DOMAIN ואשר יצא עתה מן המעשה אשר שמו ACT`.
Index: `מספר השנה אשר יצא עתה מן המעשה אשר שמו ACT`.
Collection<D>: `הספר אשר יצא עתה מן המעשה אשר שמו ACT`.
For Collection, D comes from the act's uniquely resolved output domain; for Symbol the domain is explicit in the phrase.

The reference denotes the exact just-completed performance only in the inherited immediate structural position.
Any intervening executable caller action makes it stale. There is no global last-result register and no implicit result dereference.
Observable Symbol label, Index before/zero/after magnitude, and recursively ordered Collection observation remain B13 behavior; transport is not specified.
