# Canonical HAST Contract

Version: `core-hast-0.1-candidate-1`.

The HAST contains only semantic distinctions justified by A13/B12. It intentionally does not define a generic Statement/Expression/Function/Parameter/Return/While ontology.

Core categories include:

- `HastCoreProgram(preparation, principal)`;
- preparatory `HastPlaceIntroduction`, `HastActIntroduction`, `HastRoleDeclaration`, `HastActBody`;
- numeric `HastExactNatural`, `HastCurrentFact`, `HastCurrentRoleNumber`, `HastRecentResult`, `HastAddNatural`, `HastSubtractNatural`;
- `HastEqualProposition`;
- executable `HastReplaceCurrentFact`, `HastPerformAct`, `HastProduceResult`, `HastThen`, `HastConditional`, `HastFixedRecurrence`, `HastPostActionRecurrence`;
- `HastRoleAssociation` preserving RoleId correspondence.

All nodes retain original source spans. After resolution, semantic references use typed IDs rather than spelling. Historical M3 fragment nodes remain only for regression/constituent tooling and do not define the current whole-program model.
