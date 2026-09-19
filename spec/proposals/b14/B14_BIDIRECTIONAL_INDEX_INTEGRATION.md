# B14 BidirectionalIndex Integration

A15 maps `שנת אין` to ZeroIndex, `N שנים לפני שנת אין` to BeforeZero(N), and
`N שנים אחרי שנת אין` to AfterZero(N). This year-specific family is an
ACCEPTABLE_SURFACE_NARROWING of general B13 BidirectionalIndex, not a built-in Year domain.

Natural and Index remain distinct. Natural subtraction underflow never promotes to Index.

B13 defines total successor/predecessor. A15 explicitly states that it adds no source spelling for
those operations. This is a blocking surface gap.

Megillah evidence in `megillah/original/Megilat_HaItim_Yehuda_FINAL_2026-09-18.md`, section
`מספרי השנים` around 1341–1361, requires next-year = one greater, previous-year = one less,
crossing `שנת אין`, and continuing year after year. Literal relative-year constants cannot express
this runtime recurrence.

B13 Natural→Index remains unsurfaced. The evidenced section can seed from an admitted year-profile
literal, so B14 does not make conversion a separate blocker. A16 must not introduce implicit promotion.

Typed Index state, act roles, output, and immediate result are independently missing. The final
calendar result contains the year number, so the output gap is operationally relevant.
