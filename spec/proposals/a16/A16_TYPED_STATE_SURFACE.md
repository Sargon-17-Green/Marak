# A16 — Typed State-Bearing Referents
Status: proposal delta for B15 review; A13 numeric state is unchanged.

## Domain declaration by initialization
A16 introduces no `type` declaration. For a non-Natural place, the complete typed initializer declares the place domain:
`יהי מקום ושמו PLACE ובמקום אשר שמו PLACE יהי TYPED_VALUE לבדו`.
`TYPED_VALUE` must independently denote exactly one A15/B13 domain: Symbol(D), BidirectionalIndex, or one admitted Collection<D>.
The declared domain is fixed for the lifetime of the place. A later replacement from another domain is invalid.

## Current content
Symbol(D): `השם אשר במשפחת השמות אשר שמה DOMAIN ואשר במקום אשר שמו PLACE`.
BidirectionalIndex year profile: `מספר השנה אשר במקום אשר שמו PLACE`.
Collection<D>: `הספר אשר במקום אשר שמו PLACE`; D is recovered from the place declaration, never from expected use.
`המקום אשר שמו PLACE` remains place identity and never denotes its current Value.

## Replacement
Symbol: `שים במקום אשר שמו PLACE את SYMBOL_VALUE תחת SYMBOL_PLACE_VALUE`.
Index: `שים במקום אשר שמו PLACE את INDEX_VALUE תחת INDEX_PLACE_VALUE`.
Collection: `שים במקום אשר שמו PLACE את COLLECTION_VALUE תחת COLLECTION_PLACE_VALUE`.
The displaced phrase is the exact current-content referent above. RHS completion/error/commit behavior is inherited unchanged from A13/B12.

Collection append remains pure: append(C,x)=C'. Only explicit replacement of a Collection-bearing place changes state.
Wrong-domain initialization, reference, or replacement is InvalidProgram; there is no dynamic place type and no implicit dereference.
