# C M4.1 — Role Association Fix

The legacy A11 compatibility check recursively scanned `RoleOwnerActionName` leaves under an entire association subtree. This incorrectly interpreted names inside the association's NumberValue as declarations of the callee target role owner.

M4.1 separates:

1. target-role descriptor `(callee ActId, target RoleId)`; and
2. NumberValue expression evaluated in the caller occurrence before creation of the callee occurrence.

Ownership checks inspect only the direct target descriptor fields. Caller-role reads inside the value expression therefore remain caller-context reads. No positional correspondence is introduced.

The E reproducer now resolves, validates and produces product `5` from the callee. Recursive same-role isolation also passes.
