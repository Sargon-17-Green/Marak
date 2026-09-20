# A16 — Negative Grammar Delta
Status: proposal delta; A13/A15 negatives remain in force.

Reject an untyped non-Natural place initializer or any rule saying every A13 `מקום` accepts every Value.
Reject place identity `המקום אשר שמו X` where a Value is required; no implicit dereference.
Reject Symbol/Index/Collection replacement whose RHS domain differs from the place's initializer-declared domain.
Reject changing a place from one semantic domain to another after initialization.

Reject role association whose Value domain differs from the role declaration.
Reject using `הדבר אשר במעשה ...` as the associated Value; it is role identity.
Reject positional binding, mutable role content, caller aliasing, or expected-type role inference.

Reject a typed immediate-result head that does not match the act's uniquely resolved output domain.
Reject a stale non-Natural immediate result after any intervening executable caller action.
Reject a second `הוצא` in one occurrence and reject interpreting `הוצא` as termination.
Reject two source output sites of one act whose exact semantic domains differ, even on different branches.
Reject implicit result dereference or a free/global last-result lookup.

Reject Natural subtraction as a way to cross `שנת אין`; reject successor/predecessor on Natural; reject standalone `אין` as a Value.
Reject label-word equality or source-identifier equality as Symbol equality.
Reject cross-domain Symbol equality in A16; reject Text/string operands and generic polymorphic equality.

Reject punctuation, Markdown, indentation, line breaks, or capitalization as distinctions among any A16 construction.
Any phrase ambiguous between place identity/content, member source identity/Symbol Value, Natural/Index, or role identity/current-role Value is InvalidProgram; expected type cannot rescue it.
