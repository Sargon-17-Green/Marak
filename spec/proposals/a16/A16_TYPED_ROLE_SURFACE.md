# A16 — Typed Named-Act Roles
Status: proposal delta for B15 review; A13 numeric roles are unchanged.

## Typed role declaration
Symbol(D): `יהי במעשה אשר שמו ACT דבר ושמו ROLE ובעשות את המעשה אשר שמו ACT יעמד שם ממשפחת השמות אשר שמה DOMAIN תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE`.
Index: replace the domain head by `מספר שנה`.
Collection<D>: replace the domain head by the exact admitted A15 `BOOK_KIND`.
The declaration itself fixes the semantic domain; first use cannot infer it.

## Performance association
Canonical family remains A13: `עשה את המעשה אשר שמו ACT בהיות TYPED_VALUE תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE`.
The supplied Value must match the role's declared domain. Repeated associations are named; source order has no binding meaning.

## Current occurrence reference
Symbol(D): `השם אשר במשפחת השמות אשר שמה DOMAIN ואשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE`.
Index: `מספר השנה אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE`.
Collection<D>: `הספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE`.
For Collection the exact D is recovered from the named role declaration, not from expected context.

`הדבר אשר במעשה אשר שמו ACT שמו ROLE` remains role identity, not its Value.
Associations are immutable for one performance occurrence; `המעשה הזה` remains occurrence deixis, not a stack-frame object.
No parameter cell, caller alias, positional argument, or runtime role-name search is introduced.
