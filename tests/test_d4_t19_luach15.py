from __future__ import annotations

from pathlib import Path

from compiler.parse.a15_numerals import format_natural
from tests.test_c5_6_general_index_surface import three
from tests.test_d4_post_c56_megillah import _d4_nat_book

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"

QUESTION_SEALS = [
    ("דרך בין שערי קציצה", "חותם דרך בין שערי קציצה", 1),
    ("תחילת שנת חמשת אלפים ולסופה", "חותם תחילת שנת חמשת אלפים ולסופה", 10),
    ("השנה שאחריה", "חותם השנה שאחריה", 11),
    ("השנה שלפניה", "חותם השנה שלפניה", 12),
    ("מספר הקציצות", "חותם מספר הקציצות", 20),
    ("חלוקת השנה לקציצות", "חותם חלוקת השנה לקציצות", 21),
    ("שמות הקציצות", "חותם שמות הקציצות", 22),
    ("מספר החודשים", "חותם מספר החודשים", 30),
    ("ימי החודשים", "חותם ימי החודשים", 31),
    ("שזירת החודשים", "חותם שזירת החודשים", 32),
    ("שמות החודשים", "חותם שמות החודשים", 33),
]

FILLS = [10, 20, 30, 40, 50, 60]
VISIBLE_46 = [2, 4, 1, 3, 6, 5]
CURRENT_SENTINEL = [1, 2, 3, 4, 5, 6]
MODULUS = (1 << 127) - 1


def _counted(payload: str) -> str:
    words = payload.split()
    forms = {2: "שנים", 3: "שלשה", 4: "ארבעה", 5: "חמשה", 6: "ששה"}
    assert len(words) in forms
    return f"שם אשר מספר המלים אשר בו הוא {forms[len(words)]} והמלים הן {payload}"


def _t19_marker() -> str:
    return "יהי מקום ושמו " + _counted("חותם דרך בין שערי קציצה")


def _d4_t19_preparation() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("מספר המעשה")))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("סמן המרחק")))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("מספר הדרכים")))
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:end]
    return " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )


def _set_book(payload: str, values: list[int]) -> str:
    name = _counted(payload)
    return (
        f"שים במקום אשר שמו {name} את {_d4_nat_book(values)} "
        f"תחת הספר אשר במקום אשר שמו {name}"
    )


def _setup_state() -> str:
    return " ואחרי כן ".join([
        "עשה את המעשה אשר שמו " + _counted("חשב המספר הגדול"),
        _set_book("מלא הקערות", FILLS),
        _set_book("מערכת הטיפה האחרונה", VISIBLE_46),
        _set_book("המערכה הנוכחית", CURRENT_SENTINEL),
    ])


def _place_number(payload: str) -> str:
    return "המספר אשר במקום אשר שמו " + _counted(payload)


def _perform(act: str, roles: list[tuple[str, str]]) -> str:
    a = _counted(act)
    out = "עשה את המעשה אשר שמו " + a
    for index, (role, value) in enumerate(roles):
        association = "בהיות" if index == 0 else "ובהיות"
        out += (
            f" {association} {value} תחת הדבר אשר במעשה אשר שמו {a} "
            f"שמו {role}"
        )
    return out


def _keep(value: int) -> int:
    residue = value % MODULUS
    return residue if residue else MODULUS


def _successor_bowl(query_bowl: int) -> int:
    pos = VISIBLE_46.index(query_bowl)
    return VISIBLE_46[(pos + 1) % 6]


def _oracle_first(query_bowl: int, seal: int) -> int:
    successor = _successor_bowl(query_bowl)
    return _keep(
        (FILLS[query_bowl - 1] + seal + 181) ** 2
        + 179 * FILLS[successor - 1]
        + seal
    )


def _oracle_direction(first: int, seal: int) -> int:
    probe = _keep(
        (first + seal + 1 + 193) ** 2
        + 193 * first
        + 197 * FILLS[5]
    )
    return probe % 2


def test_d4_t19_authorized_span_and_canonical_source_names():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(_t19_marker()))
    end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("מספר הדרכים")))
    block = "\n".join(lines[start:end])

    assert start + 1 == 466
    assert "# לוח חמשה עשר: לשאול את הקערות" not in block
    assert "מערכת הטיפה האחרונה" in block
    assert "המערכה הנוכחית" not in block
    assert _counted("הנותר בדרך הקצרה") in block
    assert _counted("חותם ארבעים") not in block

    payloads = [seal_name for _, seal_name, _ in QUESTION_SEALS] + [
        "מקום הקערה הנשאלת",
        "מקום הקערה שאחריה",
        "הקערה שאחריה",
        "עבודת המענה הראשון",
        "עבודת כיוון המענה",
        "עבודת המענה הבא",
        "מצא קערה שאחריה",
        "חשב מענה ראשון",
        "חשב כיוון המענה",
        "חשב מענה הבא",
        "חשב מענה קדימה",
        "חשב מענה אחורה",
    ]
    for payload in payloads:
        assert _counted(payload) in block
        assert payload.replace(" ", "") not in block


def test_d4_t19_successor_uses_visible_drop_46_arrangement_and_preserves_source_state_three_runtimes():
    source = (
        _d4_t19_preparation()
        + " ועתה "
        + _setup_state()
        + " ואחרי כן "
        + _perform("מצא קערה שאחריה", [("קערה", "המספר אשר הוא חמשה")])
    )
    _, obs = three(source)
    facts = dict(obs["facts"])
    products = [value for act, value in obs["products"] if act == "מצא קערה שאחריה"]

    assert products[-1] == 2
    assert facts["מלא הקערות"] == FILLS
    assert facts["מערכת הטיפה האחרונה"] == VISIBLE_46
    assert facts["המערכה הנוכחית"] == CURRENT_SENTINEL


def test_d4_t19_all_question_seals_match_independent_first_answer_oracle_three_runtimes():
    calls = [
        _perform(
            "חשב מענה ראשון",
            [
                ("קערה", "המספר אשר הוא שלשה"),
                ("חותם", _place_number(seal_name)),
            ],
        )
        for _, seal_name, _ in QUESTION_SEALS
    ]
    source = _d4_t19_preparation() + " ועתה " + _setup_state() + " ואחרי כן " + " ואחרי כן ".join(calls)
    _, obs = three(source)

    got = [value for act, value in obs["products"] if act == "חשב מענה ראשון"]
    expected = [_oracle_first(3, seal) for _, _, seal in QUESTION_SEALS]
    assert got == expected

    facts = dict(obs["facts"])
    for _, seal_name, seal in QUESTION_SEALS:
        assert facts[seal_name] == seal
    assert 40 not in [seal for _, _, seal in QUESTION_SEALS]
    assert facts["מלא הקערות"] == FILLS
    assert facts["מערכת הטיפה האחרונה"] == VISIBLE_46


def test_d4_t19_direction_and_successive_answer_wrap_three_runtimes():
    first_forward = _oracle_first(3, 1)
    first_backward = _oracle_first(3, 10)
    assert _oracle_direction(first_forward, 1) == 1
    assert _oracle_direction(first_backward, 10) == 0

    calls = [
        _perform("חשב כיוון המענה", [
            ("מענה", "המספר אשר הוא " + format_natural(first_forward)),
            ("חותם", _place_number("חותם דרך בין שערי קציצה")),
        ]),
        _perform("חשב כיוון המענה", [
            ("מענה", "המספר אשר הוא " + format_natural(first_backward)),
            ("חותם", _place_number("חותם תחילת שנת חמשת אלפים ולסופה")),
        ]),
        _perform("חשב מענה הבא", [
            ("מענה", "המספר אשר הוא " + format_natural(first_forward)),
            ("כיוון", "המספר אשר הוא אחד"),
        ]),
        _perform("חשב מענה הבא", [
            ("מענה", "המספר אשר הוא " + format_natural(first_backward)),
            ("כיוון", "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"),
        ]),
        _perform("חשב מענה הבא", [
            ("מענה", _place_number("המספר הגדול")),
            ("כיוון", "המספר אשר הוא אחד"),
        ]),
        _perform("חשב מענה הבא", [
            ("מענה", "המספר אשר הוא אחד"),
            ("כיוון", "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"),
        ]),
    ]
    source = _d4_t19_preparation() + " ועתה " + _setup_state() + " ואחרי כן " + " ואחרי כן ".join(calls)
    _, obs = three(source)

    directions = [value for act, value in obs["products"] if act == "חשב כיוון המענה"]
    next_values = [value for act, value in obs["products"] if act == "חשב מענה הבא"]
    assert directions == [1, 0]
    assert next_values == [
        first_forward + 1,
        first_backward - 1,
        1,
        MODULUS,
    ]

    facts = dict(obs["facts"])
    assert facts["מלא הקערות"] == FILLS
    assert facts["מערכת הטיפה האחרונה"] == VISIBLE_46
    assert facts["המערכה הנוכחית"] == CURRENT_SENTINEL
