import unittest

from compiler.reference_models.b4_candidate import (
    REFERENCE_MODEL_STATUS,
    REF_UNIT,
    RefBoolean,
    RefFailed,
    RefInteger,
    ReferenceActionDef,
    ReferenceCoreError,
    ReferenceFrame,
    ReferenceRuntime,
    ReferenceState,
    ref_add,
    ref_assign,
    ref_bind_local,
    ref_call,
    ref_eq,
    ref_fail,
    ref_if,
    ref_lit,
    ref_mul,
    ref_read,
    ref_return,
    ref_sequence,
    ref_sub,
)


def empty():
    return ReferenceState({}), ReferenceFrame({})


class B4ReferenceCandidateTests(unittest.TestCase):
    def test_status_is_explicitly_non_normative(self):
        self.assertEqual(REFERENCE_MODEL_STATUS, "REFERENCE_ONLY_AFTER_B6_ANTI_IMITATION_AUDIT")

    def test_parameter_assignment_does_not_touch_caller_in_candidate_model(self):
        rt = ReferenceRuntime()
        rt.actions["inc"] = ReferenceActionDef(
            ("p",), ref_sequence(ref_assign("p", ref_add(ref_read("p"), ref_lit(RefInteger(1)))), ref_return(ref_read("p")))
        )
        state, frame = empty()
        loc, state = rt.fresh(state, RefInteger(10))
        frame.env["x"] = loc
        value, state2 = rt.call(state, frame, "inc", (ref_read("x"),))
        self.assertEqual(value, RefInteger(11))
        self.assertEqual(rt.read(state2, frame, "x"), RefInteger(10))

    def test_candidate_argument_order(self):
        rt = ReferenceRuntime()
        rt.actions["first"] = ReferenceActionDef(("a", "b"), ref_return(ref_read("a")))
        state, frame = empty()
        loc, state = rt.fresh(state, RefInteger(0))
        frame.env["counter"] = loc

        def arg(delta, result):
            def expr(runtime, st, fr):
                cur = runtime.read(st, fr, "counter")
                st2 = runtime.assign(st, fr, "counter", RefInteger(cur.value * 10 + delta))
                return RefInteger(result), st2
            return expr

        value, state2 = rt.call(state, frame, "first", (arg(1, 7), arg(2, 8)))
        self.assertEqual(value, RefInteger(7))
        self.assertEqual(rt.read(state2, frame, "counter"), RefInteger(12))

    def test_argument_error_preserves_successor_state_when_reported(self):
        rt = ReferenceRuntime()
        rt.actions["f"] = ReferenceActionDef(("a", "b"), ref_fail("BODY_RAN"))
        state, frame = empty()
        loc, state = rt.fresh(state, RefInteger(0))
        frame.env["counter"] = loc

        def bad(runtime, st, fr):
            st2 = runtime.assign(st, fr, "counter", RefInteger(1))
            raise ReferenceCoreError("ARG_ERROR", st2)

        def later(runtime, st, fr):
            st2 = runtime.assign(st, fr, "counter", RefInteger(99))
            return RefInteger(0), st2

        with self.assertRaises(ReferenceCoreError) as cm:
            rt.call(state, frame, "f", (bad, later))
        self.assertEqual(cm.exception.code, "ARG_ERROR")
        self.assertEqual(rt.read(cm.exception.state, frame, "counter"), RefInteger(1))

    def test_fallthrough_returns_reference_unit_and_global_effect_persists(self):
        rt = ReferenceRuntime()
        state, frame = empty()
        state = rt.bind_global(state, "g", RefInteger(0))
        rt.actions["touch"] = ReferenceActionDef((), ref_assign("g", ref_add(ref_read("g"), ref_lit(RefInteger(1)))))
        value, state2 = rt.call(state, frame, "touch", ())
        self.assertEqual(value, REF_UNIT)
        self.assertEqual(state2.store[rt.global_env["g"]], RefInteger(1))

    def test_early_reference_return_skips_later_command(self):
        rt = ReferenceRuntime()
        state, frame = empty()
        state = rt.bind_global(state, "g", RefInteger(0))
        rt.actions["f"] = ReferenceActionDef(
            (), ref_sequence(ref_return(ref_lit(RefInteger(7))), ref_assign("g", ref_lit(RefInteger(99))))
        )
        value, state2 = rt.call(state, frame, "f", ())
        self.assertEqual(value, RefInteger(7))
        self.assertEqual(state2.store[rt.global_env["g"]], RefInteger(0))

    def test_nearest_reference_return_boundary(self):
        rt = ReferenceRuntime()
        rt.actions["inner"] = ReferenceActionDef((), ref_return(ref_lit(RefInteger(7))))
        rt.actions["outer"] = ReferenceActionDef(
            (), ref_sequence(ref_bind_local("x", ref_call("inner", ())), ref_return(ref_lit(RefInteger(9))))
        )
        state, frame = empty()
        value, _ = rt.call(state, frame, "outer", ())
        self.assertEqual(value, RefInteger(9))

    def test_direct_recursion_factorial_in_candidate_model(self):
        rt = ReferenceRuntime()
        rt.actions["fact"] = ReferenceActionDef(
            ("n",),
            ref_if(
                ref_eq(ref_read("n"), ref_lit(RefInteger(0))),
                ref_return(ref_lit(RefInteger(1))),
                ref_return(ref_mul(ref_read("n"), ref_call("fact", (ref_sub(ref_read("n"), ref_lit(RefInteger(1))),)))),
            ),
        )
        state, frame = empty()
        value, _ = rt.call(state, frame, "fact", (ref_lit(RefInteger(8)),))
        self.assertEqual(value, RefInteger(40320))

    def test_mutual_recursion_in_candidate_model(self):
        rt = ReferenceRuntime()
        rt.actions["even"] = ReferenceActionDef(
            ("n",),
            ref_if(
                ref_eq(ref_read("n"), ref_lit(RefInteger(0))),
                ref_return(ref_lit(RefBoolean(True))),
                ref_return(ref_call("odd", (ref_sub(ref_read("n"), ref_lit(RefInteger(1))),))),
            ),
        )
        rt.actions["odd"] = ReferenceActionDef(
            ("n",),
            ref_if(
                ref_eq(ref_read("n"), ref_lit(RefInteger(0))),
                ref_return(ref_lit(RefBoolean(False))),
                ref_return(ref_call("even", (ref_sub(ref_read("n"), ref_lit(RefInteger(1))),))),
            ),
        )
        state, frame = empty()
        self.assertEqual(rt.call(state, frame, "even", (ref_lit(RefInteger(20)),))[0], RefBoolean(True))
        self.assertEqual(rt.call(state, frame, "odd", (ref_lit(RefInteger(20)),))[0], RefBoolean(False))

    def test_callee_does_not_inherit_caller_local_in_candidate_model(self):
        rt = ReferenceRuntime()
        rt.actions["callee"] = ReferenceActionDef((), ref_return(ref_lit(RefInteger(5))))
        rt.actions["caller"] = ReferenceActionDef(
            (), ref_sequence(ref_bind_local("secret", ref_lit(RefInteger(99))), ref_return(ref_call("callee", ())))
        )
        state, frame = empty()
        value, _ = rt.call(state, frame, "caller", ())
        self.assertEqual(value, RefInteger(5))

    def test_recursive_parameter_cells_are_independent_in_candidate_model(self):
        rt = ReferenceRuntime()
        rt.actions["sumdown"] = ReferenceActionDef(
            ("n",),
            ref_if(
                ref_eq(ref_read("n"), ref_lit(RefInteger(0))),
                ref_return(ref_lit(RefInteger(0))),
                ref_return(ref_add(ref_read("n"), ref_call("sumdown", (ref_sub(ref_read("n"), ref_lit(RefInteger(1))),)))),
            ),
        )
        state, frame = empty()
        value, _ = rt.call(state, frame, "sumdown", (ref_lit(RefInteger(10)),))
        self.assertEqual(value, RefInteger(55))

    def test_global_write_then_error_is_not_rolled_back_in_candidate_model(self):
        rt = ReferenceRuntime()
        state, frame = empty()
        state = rt.bind_global(state, "g", RefInteger(0))
        out = ref_sequence(ref_assign("g", ref_lit(RefInteger(4))), ref_fail("BOOM"))(rt, state, ReferenceFrame({}))
        self.assertIsInstance(out, RefFailed)
        self.assertEqual(out.state.store[rt.global_env["g"]], RefInteger(4))


if __name__ == "__main__":
    unittest.main()
