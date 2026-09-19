import inspect
import unittest

import compiler.models.hast as hast


class AntiImitationGuardTests(unittest.TestCase):
    def test_hast_program_uses_neutral_units(self):
        fields = tuple(hast.HastProgram.__dataclass_fields__)
        self.assertEqual(fields, ("units",))

    def test_canonical_hast_does_not_predeclare_conventional_constructs(self):
        forbidden = {
            "HastStatement", "HastExpression", "HastVariable", "HastAssign",
            "HastIf", "HastWhile", "HastFor", "HastReturn", "HastFunction",
            "HastCall", "HastCallFrame", "HastArray", "HastRecord",
            "HastObject", "HastException", "HastModule", "HastImport",
        }
        exported = {name for name, value in inspect.getmembers(hast, inspect.isclass)}
        self.assertFalse(forbidden & exported)

    def test_post_audit_semantic_core_does_not_reintroduce_cell_boolean_if_ontology(self):
        import compiler.semantic_core.state as state
        import compiler.semantic_core.truth as truth
        names = {name for mod in (state, truth) for name, value in inspect.getmembers(mod, inspect.isclass)}
        forbidden = {
            "Variable", "Cell", "Location", "Frame", "Boolean", "BooleanValue",
            "If", "While", "Return", "Function", "Parameter", "CallFrame",
        }
        self.assertFalse(forbidden & names)


if __name__ == "__main__":
    unittest.main()
