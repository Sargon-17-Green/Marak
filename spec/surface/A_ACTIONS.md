# A_ACTIONS.md

Status: A12 FROZEN CORE

## 1. Reusable computation is `מעשה`

The frozen abstraction is a named described act.

Introduce:
    יהי מעשה ושמו NAME

Reference:
    המעשה אשר שמו NAME

Perform:
    עשה את המעשה אשר שמו NAME

`מצוה` is not the primary reusable-computation noun in Core.

## 2. Body framing — A12 correction

Open:
    זה דבר המעשה אשר שמו NAME

Close:
    עד הנה דבר המעשה אשר שמו NAME

The body contains complete admitted units joined by explicit admitted relations.

This correction replaces A11's:
    אלה דברי המעשה ...
    עד הנה דברי המעשה ...

because the singular `דבר` describes the matter/content of the act rather than metaphorically assigning
"words" to a non-speaking act.

## 3. Numeric input roles

A role is a named `דבר` belonging to an act.

Declaration:
    יהי במעשה אשר שמו ACT דבר ושמו ROLE
    ובעשות את המעשה אשר שמו ACT
    יעמד מספר תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Performance:
    עשה את המעשה אשר שמו ACT
    בהיות VALUE
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

Multiple required roles use repeated complete named associations.

No position carries correspondence semantics.

## 4. Value of a role during the current performance

    המספר אשר במעשה הזה
    עומד תחת
    הדבר אשר במעשה אשר שמו ACT שמו ROLE

The Value is performance-specific but not a mutable parameter cell.

## 5. Core numeric output

Inside the body:

    הוצא מן המעשה הזה את VALUE

Core v0.1 permits zero or one numeric output per performance.

The output action does not terminate the act.

After successful completion of a single-output performance:

    המספר אשר יצא עתה מן המעשה אשר שמו ACT

may be used immediately.

## 6. Completion

When the body runs out of executable units, the performance completes normally.

Result production and completion are separate.

Explicit cessation remains a possible future/limited construction where the Hebrew itself says the
activity ceases, but the Core does not model every result as abrupt return.

## 7. Mutual recursion / forward use

An act must have been explicitly introduced by:

    יהי מעשה ושמו X

before a body refers to it.

Its body may appear later.

This is discourse introduction of a referent, not a mandatory global prototype section.

# A13 program and visibility closure

`יהי מעשה ושמו X` introduces X; it does not perform X. A body definition is legal only after that
introduction and occurs exactly once before `ועתה`. All roles of X are declared after X is introduced
and before its body definition.

Direct self-performance is legal because X is already available when its body is read. Mutual
recursion is legal when all participating identities have been introduced before bodies that refer to
them. A later introduction cannot repair an earlier reference.

At top level an act is performed only if the principal execution explicitly asks for it, for example:

    ועתה עשה את המעשה אשר שמו X

No `main` name is reserved. `הוצא` remains product/result production and is not abrupt return.
