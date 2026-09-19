# A_REFERENCE_AND_SCOPE.md

Status: A12 FROZEN CORE

## 1. Reference principle

A legal referring description has one source-determined referent.

No reference is rescued by:
- nearest antecedent;
- runtime call-chain search;
- type compatibility;
- intended algorithm.

## 2. Place identity versus current content

    המקום אשר שמו X

denotes the state-bearing place.

    המספר אשר במקום אשר שמו X

denotes its current numeric content.

No implicit dereference exists.

## 3. Named act

    המעשה אשר שמו X

denotes the reusable described act.

## 4. Act body region

    זה דבר המעשה אשר שמו X
    ...
    עד הנה דבר המעשה אשר שמו X

The repeated explicit name establishes the body boundary.

A mismatched closer is illegal.

Core act definitions do not nest.

## 5. Role identity

    הדבר אשר במעשה אשר שמו ACT שמו ROLE

denotes the named role belonging to the reusable act.

## 6. Current performance occurrence

Inside a currently executed body:

    המעשה הזה

denotes the particular performance occurrence currently being carried out.

This is event/deed deixis, not a stack-frame object.

In recursive performance, the inner execution has its own current `המעשה הזה`; after it completes,
the outer performance resumes.

This rule does not grant caller-local name lookup.

## 7. Result provenance

Immediately after a completed single-result performance:

    המספר אשר יצא עתה מן המעשה אשר שמו ACT

denotes that performance's one numeric result.

`עתה` and adjacency are essential.
No historical/free last-result reference is created.

## 8. Same spelling in different source domains

Core forbids unresolved same-name ambiguity.

A future richer scope system may introduce explicit qualification.
No conventional shadowing rule is part of v0.1.

# A13 discourse visibility and lifetime

## Program discourse
Frozen Core has one top-level program discourse: preparatory introductions/definitions followed by a
single `ועתה` principal execution.

## Introduction-before-use
A referent may be used only after its complete introduction has ended. Core has no whole-document
hoisting and no implicit forward declarations.

### Places
A place becomes available after its complete initialized introduction and remains available through
program completion. It cannot refer to itself in its own initializer because the introduction is not
yet complete.

### Acts
An act identity becomes available after `יהי מעשה ושמו X`. Its body is defined later exactly once,
before `ועתה`. Direct self-reference in its body is legal because X has already been introduced.

### Mutual recursion
Mutual recursion needs no forward-reference rule: introduce all participating act identities first,
then define bodies that refer to those already introduced identities.

### Roles
The owner act must already be introduced. Role declarations occur before the owner's body definition.
Role identity remains available thereafter, but the numeric association exists only for the duration
of one performance occurrence.

## Collision policy
Duplicate place names and duplicate act names are invalid in one Core program. Duplicate role names
are invalid within one owner act. The same spelling across explicitly typed kinds is not automatically
ambiguous, e.g. place X and act X have different complete Hebrew references.

## No nested introduction scope in Core
Frozen body units do not introduce places, acts or roles. A13 therefore does not import a generic
brace/block lexical-scope model.
