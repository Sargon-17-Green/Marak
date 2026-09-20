# C5.1 Domain Validation

Domain resolution is static-first. `hast_value_domain()` and `ir_value_domain()` determine an expression's domain from the resolved expression itself plus already-established identity contracts. Consumer expectations never assign a missing domain.

`validate_hast_domains()` runs before IR lowering. `validate_canonical_ir()` independently revalidates decoded IR at the artifact trust boundary. Both reject mismatched place initialization/replacement, role association, output domain, immediate-result typed head, collection element metadata, incomplete contracts, and unresolved expression domains.

A13/B12 Natural nodes remain specialized. Natural arithmetic and equality reject non-Natural operands; there is no promotion to BidirectionalIndex or Symbol. Runtime backends consume only validated IR and use host type checks solely as unreachable invariant guards, not as domain inference.

Stable domain diagnostics are reserved as `DOM0001` through `DOM0012`; structured validation issues also retain precise semantic invariant codes such as `IR_DOMAIN_ROLE_ASSOCIATION` and `IR_DOMAIN_RESULT_HEAD` for artifact diagnostics. Program invocation uses the distinct B13/B15 codes `MISSING_INPUT_BINDING`, `EXTRA_INPUT_BINDING`, `DUPLICATE_INPUT_BINDING`, and `INPUT_DOMAIN_MISMATCH`.

No runtime name lookup was introduced. Place/Act/Role operations use resolved identities; source spellings are retained only for diagnostics/observable labels.
