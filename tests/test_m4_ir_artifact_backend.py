from __future__ import annotations
import hashlib
import json
import unittest
from dataclasses import replace

from compiler.api import check, compile_source, run_reference, run_source
from compiler.artifact.format import ArtifactVerificationError, serialize_artifact, verify_artifact, verify_ir
from compiler.ir_lower import lower_validated_hast
from compiler.models import ir as irm
from compiler.optimize import optimize
from compiler.runtime.observables import backend_observable, reference_observable
from compiler.version import ARTIFACT_FORMAT_VERSION, IR_VERSION, LANGUAGE_EDITION
from tests.m4_support import a13_json, tiny_source, ZERO, role_sum_program


def _canon(x):
    return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(",",":"),allow_nan=False).encode("utf-8")


def _retagged(data: bytes, mutate) -> bytes:
    obj=json.loads(data.decode("utf-8"))
    mutate(obj)
    obj["payload_sha256"]=hashlib.sha256(_canon(obj["program"])).hexdigest()
    return _canon(obj)+b"\n"


def _walk(obj):
    if isinstance(obj,dict):
        yield obj
        for v in obj.values(): yield from _walk(v)
    elif isinstance(obj,list):
        for v in obj: yield from _walk(v)


class M4IRContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=tiny_source()
        cls.check=check(cls.source)
        assert cls.check.valid
        cls.ir=lower_validated_hast(cls.check.hast)

    def test_ir_has_assigned_version_and_no_language_halt_node(self):
        self.assertEqual(self.ir.ir_version,IR_VERSION)
        self.assertNotEqual(IR_VERSION,"unassigned")
        names={type(x).__name__ for x in self._nodes(self.ir)}
        self.assertNotIn("IRHalt",names)
        self.assertNotIn("IRReturn",names)
        self.assertNotIn("IRWhile",names)

    def _nodes(self,node):
        import dataclasses
        yield node
        if dataclasses.is_dataclass(node):
            for f in dataclasses.fields(node):
                v=getattr(node,f.name)
                if isinstance(v,tuple):
                    for x in v:
                        if dataclasses.is_dataclass(x): yield from self._nodes(x)
                elif dataclasses.is_dataclass(v) and type(v).__name__!="OriginalSpan":
                    yield from self._nodes(v)

    def test_initial_fact_is_distinct_from_replacement(self):
        names={type(x).__name__ for x in self._nodes(self.ir)}
        self.assertIn("IRInitialFact",names)
        self.assertIn("IRReplaceCurrentFact",names)

    def test_subtraction_is_checked_not_signed_result(self):
        subs=[x for x in self._nodes(self.ir) if isinstance(x,irm.IRCheckedSubtractNatural)]
        self.assertTrue(subs)
        self.assertTrue(all(x.error_code=="ARITHMETIC_DOMAIN_ERROR" for x in subs))

    def test_role_correspondence_survives_as_identity(self):
        role_check=check(role_sum_program())
        self.assertTrue(role_check.valid)
        role_ir=lower_validated_hast(role_check.hast)
        performs=[x for x in self._nodes(role_ir) if isinstance(x,irm.IRPerformAct) and x.associations]
        self.assertTrue(performs)
        for p in performs:
            self.assertTrue(all(type(a.role) is int for a in p.associations))
            self.assertEqual([a.role for a in p.associations],sorted(a.role for a in p.associations))

    def test_optimizer_is_explicit_identity_preserving_pass(self):
        out,report=optimize(self.ir)
        self.assertIs(out,self.ir)
        self.assertEqual(report.passes,("identity-preserve-observables",))


class M4ArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.comp=compile_source(tiny_source())
        assert cls.comp.valid and cls.comp.artifact and cls.comp.ir
        cls.data=cls.comp.artifact

    def test_artifact_versions_assigned_and_roundtrip(self):
        self.assertNotEqual(ARTIFACT_FORMAT_VERSION,"unassigned")
        ir=verify_artifact(self.data)
        self.assertEqual(ir,self.comp.ir)

    def test_serialization_is_byte_deterministic(self):
        a=serialize_artifact(self.comp.ir,language_edition=LANGUAGE_EDITION)
        b=serialize_artifact(self.comp.ir,language_edition=LANGUAGE_EDITION)
        self.assertEqual(a,b)
        self.assertEqual(hashlib.sha256(a).hexdigest(),hashlib.sha256(b).hexdigest())

    def test_rejects_unknown_artifact_version(self):
        obj=json.loads(self.data); obj["artifact_version"]="future"
        bad=_canon(obj)+b"\n"
        with self.assertRaises(ArtifactVerificationError): verify_artifact(bad)

    def test_rejects_incompatible_language_edition_even_with_valid_digest(self):
        bad=_retagged(self.data,lambda o:o.__setitem__("language_edition","other-edition"))
        with self.assertRaisesRegex(ArtifactVerificationError,"language edition"): verify_artifact(bad)

    def test_rejects_unknown_opcode(self):
        def mutate(o):
            n=next(x for x in _walk(o["program"]) if x.get("tag")=="IRNatural")
            n["tag"]="IRArbitraryPython"
        with self.assertRaises(ArtifactVerificationError): verify_artifact(_retagged(self.data,mutate))

    def test_rejects_negative_natural_without_leaking_valueerror(self):
        def mutate(o):
            n=next(x for x in _walk(o["program"]) if x.get("tag")=="IRNatural")
            n["value"]=-1
        with self.assertRaises(ArtifactVerificationError): verify_artifact(_retagged(self.data,mutate))

    def test_rejects_unresolved_place_reference(self):
        def mutate(o):
            n=next(x for x in _walk(o["program"]) if x.get("tag")=="IRReadCurrentFact")
            n["place"]=999999
        with self.assertRaisesRegex(ArtifactVerificationError,"place"): verify_artifact(_retagged(self.data,mutate))

    def test_rejects_duplicate_identity_serial(self):
        def mutate(o):
            syms=[x for x in _walk(o["program"]) if x.get("tag")=="IRSymbol"]
            syms[1]["serial"]=syms[0]["serial"]
        with self.assertRaisesRegex(ArtifactVerificationError,"duplicate identity"): verify_artifact(_retagged(self.data,mutate))

    def test_rejects_unchecked_subtraction_error_code(self):
        def mutate(o):
            n=next(x for x in _walk(o["program"]) if x.get("tag")=="IRCheckedSubtractNatural")
            n["error_code"]="NEGATIVE_IS_FINE"
        with self.assertRaisesRegex(ArtifactVerificationError,"subtraction"): verify_artifact(_retagged(self.data,mutate))

    def test_rejects_invalid_role_association_reference(self):
        role_comp=compile_source(role_sum_program())
        self.assertTrue(role_comp.valid)
        def mutate(o):
            association=next(x for x in _walk(o["program"]) if x.get("tag")=="IRRoleAssociation")
            association["role"]=999999
        with self.assertRaisesRegex(ArtifactVerificationError,"role association"):
            verify_artifact(_retagged(role_comp.artifact,mutate))

    def test_no_pickle_or_eval_artifact_path(self):
        from pathlib import Path
        text=Path("compiler/artifact/format.py").read_text(encoding="utf-8")
        self.assertNotIn("pickle",text)
        self.assertNotIn("eval(",text)


class M4DifferentialExecutionTests(unittest.TestCase):
    def assertDifferential(self,source:str,*,fuel:int|None=None):
        c,r=run_reference(source,fuel=fuel)
        self.assertTrue(c.valid,[d.code for d in c.diagnostics])
        vm=run_source(source,fuel=fuel)
        self.assertTrue(vm.compilation.valid)
        self.assertEqual(reference_observable(r),backend_observable(vm.outcome))
        return reference_observable(r)

    def test_tiny_rm_end_to_end(self):
        obs=self.assertDifferential(tiny_source(),fuel=10000)
        self.assertEqual(obs["outcome"],"Normal")
        self.assertEqual(obs["facts"],[["גד",0],["עזר",0]])

    def test_all_terminating_a13_positive_examples_differential(self):
        for x in a13_json("a13_program_conformance.json")["positive"]:
            if "diverges" in x.get("note",""): continue
            with self.subTest(x=x["id"]): self.assertDifferential(x["source"],fuel=10000)

    def test_simple_counted_recurrence(self):
        inc=("שים במקום אשר שמו גד את המספר הנחשב בהוסיף את המספר אשר הוא אחד על "
             "המספר אשר במקום אשר שמו גד תחת המספר אשר במקום אשר שמו גד")
        src="יהי מקום ושמו גד ובמקום אשר שמו גד יהי המספר אשר הוא אחד לבדו ועתה שלש פעמים "+inc
        obs=self.assertDifferential(src); self.assertEqual(obs["facts"],[["גד",4]])

if __name__ == '__main__': unittest.main()
