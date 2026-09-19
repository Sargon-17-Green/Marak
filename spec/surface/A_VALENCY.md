# A_VALENCY.md

Status: A12 FROZEN CORE

## 1. General rule

Every action/calculation family has explicit grammatical roles.

A preposition inside a subordinate constituent cannot be stolen by an outer predicate.

No "nearest מן", "nearest על", or expected-type role inference exists.

## 2. Arithmetic

Addition:
    המספר הנחשב בהוסיף את ADDEND על AUGEND

Subtraction:
    המספר הנחשב בגרע את AMOUNT מן SOURCE

Role markers remain semantically meaningful even where arithmetic properties such as commutativity
would make some operand swaps numerically equal.

## 3. Place replacement

    שים במקום אשר שמו TARGET
    את NEW_VALUE
    תחת המספר אשר במקום אשר שמו TARGET

Required roles:
- destination;
- new numeric content;
- displaced current numeric content.

## 4. Act performance

    עשה את המעשה אשר שמו ACT

Target act is an explicit typed reference.

## 5. Input association

    בהיות VALUE
    תחת הדבר אשר במעשה אשר שמו ACT שמו ROLE

The role name, not position, determines association.

## 6. Result production

    הוצא מן המעשה הזה את VALUE

Required roles:
- current performance source;
- output numeric Value.

It does not contain a hidden completion role.

# A13 subtraction-domain clarification

The frozen subtraction frame remains:

    המספר הנחשב בגרע את A מן B

`את A` is the amount removed and `מן B` is the source. Within the Core Natural domain a result exists
only when A≤B. A larger A is not a request to extend the language to negative integers. B12 defines
the arithmetic-domain failure behavior if the precondition is not established at runtime.
