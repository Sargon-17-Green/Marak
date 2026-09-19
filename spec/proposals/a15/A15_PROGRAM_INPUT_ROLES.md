# A15 — Program Input Roles

Status: **INTEGRATED_SURFACE_READY** for D-LANGUAGE-REQUEST-007.

## 1. Whole-program owner

A15 keeps `המלאכה הזאת` as the deictic head for the complete Marak work/program **only in top-level preparatory input-role constructions**.

The phrase is used by the Megillah itself for the whole calendar work and is ordinary Biblical wording for a bounded work (`נעשתה המלאכה הזאת`, Nehemiah 6:16). It is distinct from A13 `המעשה הזה`, which denotes the current performance occurrence of a named act.

A15 therefore does not introduce `main`, a synthetic principal act, or a callable program object.

## 2. Exact declaration

A required Program Input Role is declared as one preparatory unit:

    יהי למלאכה הזאת דבר ושמו ROLE
    ובטרם תחל המלאכה הזאת
    יעמד DOMAIN_HEAD
    תחת הדבר אשר למלאכה הזאת שמו ROLE

Line breaks carry no syntax.

This construction is structural/declarative. It extends the already frozen A13 `יהי ... דבר ... יעמד ... תחת הדבר` role idiom and explicitly locates the association before the work begins. It is not an execution instruction that supplies a value at that point in the program.

A14's candidate `למלאכה הזאת ינתן ...` is therefore **not** canonical A15 wording: `ינתן` can too easily be read as the work performing a giving event now, whereas B13 requires a pre-invocation immutable association.

## 3. Domain heads

A15 does not add generic modern type syntax. The semantic domain is distinguished by an ordinary typed Hebrew head:

- Natural: `מספר`;
- Symbol(D): `שם ממשפחת השמות אשר שמה DOMAIN`;
- year-profile BidirectionalIndex: `מספר שנה`;
- Collection: an admitted `ספר ...` kind, such as `ספר מספרים`, `ספר מספרי שנים`, or `ספר שמות ממשפחת השמות אשר שמה DOMAIN`.

This framework is domain-aware now; adding another semantic domain later requires a new independently audited Hebrew head, not angle brackets or a type annotation operator.

## 4. References

Natural:

    המספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

Symbol:

    השם אשר במשפחת השמות אשר שמה DOMAIN
    עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

Year-profile index:

    מספר השנה אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

Collection:

    הספר אשר עומד תחת הדבר אשר למלאכה הזאת שמו ROLE

The role declaration fixes the collection element domain, so the last reference cannot be reinterpreted as a different book kind by context.

## 5. Binding semantics

Host association is by resolved Program Input Role identity. Declaration order has no binding meaning. Two same-domain roles remain distinct. Every required role has exactly one association before Preparation; extra, missing, duplicate, or domain-mismatched associations fail invocation before any preparatory effect.

The association is immutable. It is not a `מקום`, cannot be replaced, and has no storage address. If execution needs mutable working state, it must explicitly establish state from the input Value using whatever integrated state-bearing surface B14 accepts.

Transport is not language semantics. A15 says nothing about stdin, argv, HTTP, files, environment variables, or GUI fields.

## 6. Evidence and controlled deviation

The Megillah begins the reusable algorithm with two explicitly distinguished days and warns not to exchange the first and second. A15 keeps the semantic distinction but removes ordinal binding: source identity, not `first/second`, binds the host Value. This follows B13's accepted Program Input Role model and A13's existing non-positional role discipline.

## 7. Rejection

Reject positional association, declaration-order binding, source-spelling-only host lookup, a mutable-input wording, unbound principal execution, a hidden default input, or any transport convention inferred from the declaration.
