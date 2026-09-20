from __future__ import annotations

import importlib.util
import random
from pathlib import Path

from compiler.api import parse
from compiler.parse.a15_numerals import (
    A15_DIRECT_NUMERAL_LEXICON_ID, format_natural, match_a15_numeral,
)
from compiler.parse.c5_2_registry import C5_2_REGISTRY
from compiler.parse.numeral_lexicons import A12_DIRECT_NUMERALS


ROOT=Path(__file__).resolve().parents[1]


def _reference():
    path=ROOT/"spec"/"proposals"/"a15"/"tools"/"a15_numeral_reference.py"
    spec=importlib.util.spec_from_file_location("a15_independent_numeral_reference",path)
    module=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def full_match(text: str):
    words=tuple(text.split())
    return [x for x in match_a15_numeral(A15_DIRECT_NUMERAL_LEXICON_ID,words,0) if x[0]==len(words)]


def test_all_a13_9999_forms_are_preserved_exactly_and_parse_to_same_value():
    for n in range(1,10_000):
        text=A12_DIRECT_NUMERALS[n]
        assert format_natural(n)==text
        matches=full_match(text)
        assert [(end,value) for end,value,_ in matches]==[(len(text.split()),n)]


def test_a15_reference_parity_boundaries_megillah_and_random_large_sample():
    ref=_reference()
    rng=random.Random(5202026)
    values=[
        10_000,10_001,14_700,999_999,1_000_000,1_000_001,
        14_777_149,99_999_999,
    ]+[rng.randint(10_000,99_999_999) for _ in range(500)]
    for n in values:
        text=ref.format_natural(n)
        assert format_natural(n)==text
        matches=full_match(text)
        assert len(matches)==1 and matches[0][1]==n
    assert format_natural(14_777_149)=="ארבעה עשר אלף אלפים ושבע מאות אלף ושבעים אלף ושבעת אלפים ומאה וארבעים ותשעה"


def test_malformed_large_magnitude_forms_have_no_full_parse():
    malformed=[
        "שבע מאות אלף וארבעה עשר אלף אלפים",
        "עשרת אלפים ועשרת אלפים",
        "מאה אלף אלפים",
        "ארבעה עשר אלף אלפים שבע מאות אלף",
        "אלף אלפים ואלף אלפים",
        "עשרים אלף ושבעת אלפים ושבעים אלף",
    ]
    for text in malformed:
        assert full_match(text)==[]


def test_direct_zero_and_arabic_digits_are_not_admitted_natural_literals():
    for source in ("המספר אשר הוא אפס","המספר אשר הוא 14777149"):
        r=parse(source,registry=C5_2_REGISTRY,start_lhs="NumberValue").parse_result
        assert not r.forest.alternatives


def test_large_numeral_punctuation_is_transparent_but_not_syntax():
    canonical="המספר אשר הוא "+format_natural(14_777_149)
    decorated=canonical.replace(" "," . # ** ")
    a=parse(canonical,registry=C5_2_REGISTRY,start_lhs="NumberValue").parse_result
    b=parse(decorated,registry=C5_2_REGISTRY,start_lhs="NumberValue").parse_result
    assert len(a.forest.alternatives)==len(b.forest.alternatives)==1
