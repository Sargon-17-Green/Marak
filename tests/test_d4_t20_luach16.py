from __future__ import annotations

from pathlib import Path

from compiler.parse.a15_numerals import format_natural
from tests.test_c5_6_general_index_surface import three
from tests.test_d4_post_c56_megillah import _d4_nat_book

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "megillah" / "candidates" / "Megilat_HaItim_Marak_Candidate.md"

SOURCE_NAMES = [
    "מספר הדרכים",
    "האחרון אשר ילקח",
    "מספר המקומות",
    "מספר כל היוצאים",
    "המספר הרחב האחד",
    "האחרון הרחב אשר ילקח",
]
FILLS = [10, 20, 30, 40, 50, 60]
VISIBLE_46 = [2, 4, 1, 3, 6, 5]
CURRENT_SENTINEL = [1, 2, 3, 4, 5, 6]


def _counted(payload: str) -> str:
    words = payload.split()
    forms = {2: "שנים", 3: "שלשה", 4: "ארבעה", 5: "חמשה", 6: "ששה"}
    assert len(words) in forms
    return f"שם אשר מספר המלים אשר בו הוא {forms[len(words)]} והמלים הן {payload}"


def _nat(n: int) -> str:
    if n == 0:
        return "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"
    return "המספר אשר הוא " + format_natural(n)


def _place(payload: str) -> str:
    name = _counted(payload) if " " in payload else payload
    return f"המספר אשר במקום אשר שמו {name}"


def _set_number(payload: str, n: int) -> str:
    name = _counted(payload) if " " in payload else payload
    return f"שים במקום אשר שמו {name} את {_nat(n)} תחת המספר אשר במקום אשר שמו {name}"


def _set_book(payload: str, values: list[int]) -> str:
    name = _counted(payload)
    return f"שים במקום אשר שמו {name} את {_d4_nat_book(values)} תחת הספר אשר במקום אשר שמו {name}"


def _call_choice(n: int, answer: int, direction: int) -> str:
    return (
        "עשה את המעשה אשר שמו בחירה "
        f"בהיות {_nat(n)} תחת הדבר אשר במעשה אשר שמו בחירה שמו {_counted('מספר הדרכים')} "
        f"ובהיות {_nat(answer)} תחת הדבר אשר במעשה אשר שמו בחירה שמו מענה "
        f"ובהיות {_nat(direction)} תחת הדבר אשר במעשה אשר שמו בחירה שמו כיוון"
    )




def _call_choice_expr(n_expr: str, answer_expr: str, direction_expr: str) -> str:
    return (
        "עשה את המעשה אשר שמו בחירה "
        f"בהיות {n_expr} תחת הדבר אשר במעשה אשר שמו בחירה שמו {_counted('מספר הדרכים')} "
        f"ובהיות {answer_expr} תחת הדבר אשר במעשה אשר שמו בחירה שמו מענה "
        f"ובהיות {direction_expr} תחת הדבר אשר במעשה אשר שמו בחירה שמו כיוון"
    )

def _t20_bounds(lines: list[str]) -> tuple[int, int]:
    start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("מספר הדרכים")))
    end = next(i for i, line in enumerate(lines) if line.startswith("# לוח שבעה עשר: שערי הקציצה"))
    return start, end


def _t20_block() -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start, end = _t20_bounds(lines)
    return "\n".join(lines[start:end])


def _preparation(extra_declarations: str = "") -> str:
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    counters_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("מספר המעשה")))
    counters_end = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו " + _counted("סמן המרחק")))
    core_start = next(i for i, line in enumerate(lines) if line.startswith("יהי מקום ושמו מכפלה"))
    _, end = _t20_bounds(lines)
    selected = lines[0:6] + lines[counters_start:counters_end] + lines[core_start:end]
    prep = " ".join(
        line for line in selected
        if line.strip() and line.strip() != "---" and not line.lstrip().startswith("#")
    )
    return prep + ((" " + extra_declarations) if extra_declarations else "")


def _setup(m: int) -> str:
    return " ואחרי כן ".join([
        _set_number("המספר הגדול", m),
        _set_book("מלא הקערות", FILLS),
        _set_book("מערכת הטיפה האחרונה", VISIBLE_46),
        _set_book("המערכה הנוכחית", CURRENT_SENTINEL),
    ])


def _run_calls(m: int, calls: list[str], extra_declarations: str = ""):
    source = _preparation(extra_declarations) + " ועתה " + _setup(m)
    if calls:
        source += " ואחרי כן " + " ואחרי כן ".join(calls)
    _, obs = three(source)
    return obs


def _next_answer(a: int, direction: int, m: int) -> int:
    if direction == 1:
        return 1 if a == m else a + 1
    return m if a == 1 else a - 1


def _oracle(m: int, n: int, first: int, direction: int) -> dict[str, int]:
    if n <= m:
        limit = (m // n) * n
        a = first
        while a > limit:
            a = _next_answer(a, direction, m)
        return {"way": ((a - 1) % n) + 1, "limit": limit}

    k = 1
    w = m
    while w < n:
        k += 1
        w *= m
    answers = [first]
    for _ in range(1, k):
        answers.append(_next_answer(answers[-1], direction, m))
    wide = 1 + sum((a - 1) * (m ** i) for i, a in enumerate(answers))
    wide_limit = (w // n) * n
    accepted = wide
    while accepted > wide_limit:
        if direction == 1:
            accepted = 1 if accepted == w else accepted + 1
        else:
            accepted = w if accepted == 1 else accepted - 1
    return {
        "way": ((accepted - 1) % n) + 1,
        "k": k,
        "w": w,
        "wide_first": wide,
        "wide_limit": wide_limit,
        "accepted": accepted,
    }


def _probe_act(name: str, place_payload: str) -> str:
    place_expr = _place(place_payload)
    return (
        f"יהי מעשה ושמו {name} "
        f"זה דבר המעשה אשר שמו {name} "
        f"הוצא מן המעשה הזה את {place_expr} "
        f"עד הנה דבר המעשה אשר שמו {name}"
    )


def test_d4_t20_authorized_span_names_fast_remainder_and_bowl_exclusion():
    lines = CANDIDATE.read_text(encoding="utf-8").splitlines()
    start, end = _t20_bounds(lines)
    block = "\n".join(lines[start:end])

    assert start + 1 == 507
    assert end + 1 == 559
    for payload in SOURCE_NAMES:
        assert _counted(payload) in block
        assert payload.replace(" ", "") not in block

    assert _counted("הנותר בדרך הקצרה") in block
    assert "נותרמהר" not in block
    assert "מלא הקערות" not in block
    assert "מערכת הטיפה האחרונה" not in block
    assert "המערכה הנוכחית" not in block
    assert "שבע מאות ועשרים" not in block
    assert "# לוח שבעה עשר" not in block


def test_d4_t20_branch_a_boundaries_rejection_fairness_n1_divisor_three_runtimes():
    m = 12
    cases = [
        (1, 12, 1),  # N=1
        (4, 12, 0),  # exact divisor
        (5, 1, 1),
        (5, 5, 1),
        (5, 6, 1),
        (5, 12, 1),  # rejected tail, forward
        (5, 12, 0),  # rejected tail, backward
    ]
    obs = _run_calls(m, [_call_choice(*c) for c in cases])
    got = [v for act, v in obs["products"] if act == "בחירה"]
    want = [_oracle(m, *c)["way"] for c in cases]
    assert got == want

    limit = (m // 5) * 5
    buckets = {i: 0 for i in range(1, 6)}
    for a in range(1, limit + 1):
        buckets[((a - 1) % 5) + 1] += 1
    assert set(buckets.values()) == {limit // 5}

    facts = dict(obs["facts"])
    assert facts["האחרון אשר ילקח"] == limit
    assert facts["מלא הקערות"] == FILLS
    assert facts["מערכת הטיפה האחרונה"] == VISIBLE_46
    assert facts["המערכה הנוכחית"] == CURRENT_SENTINEL


def test_d4_t20_branch_b_small_models_minimal_places_encoding_wrap_rejection_fairness_three_runtimes():
    m = 5
    k3 = (27, 5, 1)
    k2_forward = (6, 5, 1)
    k2_backward = (6, 1, 0)
    reject_forward = (7, 4, 1)   # wide_first=24, L=21, then 25 -> 1
    reject_backward = (9, 1, 0)  # wide_first=21, L=18, then 20 -> 19 -> 18
    want3 = _oracle(m, *k3)
    want2f = _oracle(m, *k2_forward)
    want2b = _oracle(m, *k2_backward)
    want_rf = _oracle(m, *reject_forward)
    want_rb = _oracle(m, *reject_backward)

    probes = " ".join([
        _probe_act("בחן", "מספר המקומות"),
        _probe_act("מדד", "מספר כל היוצאים"),
        _probe_act("צפה", "המספר הרחב האחד"),
        _probe_act("חתם", "האחרון הרחב אשר ילקח"),
    ])
    calls = [
        _call_choice(*k3),
        "עשה את המעשה אשר שמו בחן",
        "עשה את המעשה אשר שמו מדד",
        "עשה את המעשה אשר שמו צפה",
        "עשה את המעשה אשר שמו חתם",
        _call_choice(*k2_forward),
        _call_choice(*k2_backward),
        _call_choice(*reject_forward),
        _call_choice(*reject_backward),
        "עשה את המעשה אשר שמו בחן",
        "עשה את המעשה אשר שמו מדד",
        "עשה את המעשה אשר שמו צפה",
        "עשה את המעשה אשר שמו חתם",
        _set_number("מספר כל היוצאים", 5),
        _set_number("קלט", 5),
        _set_number("מגמה", 1),
        "עשה את המעשה אשר שמו צעידה",
        _set_number("קלט", 1),
        _set_number("מגמה", 0),
        "עשה את המעשה אשר שמו צעידה",
        _set_number("קלט", 3),
        _set_number("מגמה", 1),
        "עשה את המעשה אשר שמו צעידה",
        _set_number("קלט", 3),
        _set_number("מגמה", 0),
        "עשה את המעשה אשר שמו צעידה",
    ]
    obs = _run_calls(m, calls, probes)

    choices = [v for act, v in obs["products"] if act == "בחירה"]
    assert choices == [want3["way"], want2f["way"], want2b["way"], want_rf["way"], want_rb["way"]]
    assert [v for act, v in obs["products"] if act == "בחן"] == [want3["k"], want_rb["k"]]
    assert [v for act, v in obs["products"] if act == "מדד"] == [want3["w"], want_rb["w"]]
    assert [v for act, v in obs["products"] if act == "צפה"] == [want3["wide_first"], want_rb["wide_first"]]
    assert [v for act, v in obs["products"] if act == "חתם"] == [want3["wide_limit"], want_rb["wide_limit"]]
    assert [v for act, v in obs["products"] if act == "צעידה"] == [25, 1, 20, 19, 18, 1, 5, 4, 2]

    # Independent fairness proofs for both k=2 and k=3 models.
    for n in (6, 27):
        k = min(i for i in range(1, 10) if m**i >= n)
        w = m**k
        limit = (w // n) * n
        buckets = {i: 0 for i in range(1, n + 1)}
        for wide in range(1, limit + 1):
            buckets[((wide - 1) % n) + 1] += 1
        assert set(buckets.values()) == {limit // n}

    facts = dict(obs["facts"])
    assert facts["מלא הקערות"] == FILLS
    assert facts["מערכת הטיפה האחרונה"] == VISIBLE_46
    assert facts["המערכה הנוכחית"] == CURRENT_SENTINEL


def test_d4_t20_real_m_large_cardinality_exact_natural_arithmetic_three_runtimes():
    real_m = (1 << 127) - 1
    n = real_m + 1
    want = _oracle(real_m, n, 1, 1)
    setup = " ואחרי כן ".join([
        "עשה את המעשה אשר שמו " + _counted("חשב המספר הגדול"),
        _set_book("מלא הקערות", FILLS),
        _set_book("מערכת הטיפה האחרונה", VISIBLE_46),
        _set_book("המערכה הנוכחית", CURRENT_SENTINEL),
    ])
    n_expr = f"המספר הנחשב בהוסיף את המספר אשר הוא אחד על {_place('המספר הגדול')}"
    call = _call_choice_expr(n_expr, _nat(1), _nat(1))
    source = _preparation() + " ועתה " + setup + " ואחרי כן " + call
    _, obs = three(source)
    facts = dict(obs["facts"])
    products = [v for act, v in obs["products"] if act == "בחירה"]

    assert facts["מספר המקומות"] == 2
    assert facts["מספר כל היוצאים"] == real_m * real_m
    assert facts["מספר כל היוצאים"] > real_m
    assert facts["המספר הרחב האחד"] == want["wide_first"]
    assert facts["האחרון הרחב אשר ילקח"] == want["wide_limit"]
    assert products[-1] == want["way"]
