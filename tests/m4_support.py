from __future__ import annotations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
A13_FIXTURES = ROOT / "tests" / "fixtures" / "a13"


def a13_json(name: str):
    return json.loads((A13_FIXTURES / name).read_text(encoding="utf-8"))


def tiny_source() -> str:
    return (A13_FIXTURES / "a13_tiny_machine.he.txt").read_text(encoding="utf-8")

ZERO = "המספר הנחשב בגרע את המספר אשר הוא אחד מן המספר אשר הוא אחד"

def role_sum_program(*, reverse: bool = False) -> str:
    decl1=("יהי במעשה אשר שמו ראובן דבר ושמו שמעון ובעשות את המעשה אשר שמו ראובן "
           "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון")
    decl2=("יהי במעשה אשר שמו ראובן דבר ושמו לוי ובעשות את המעשה אשר שמו ראובן "
           "יעמד מספר תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי")
    role1="המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
    role2="המספר אשר במעשה הזה עומד תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי"
    body=("זה דבר המעשה אשר שמו ראובן הוצא מן המעשה הזה את המספר הנחשב בהוסיף את "
          +role1+" על "+role2+" עד הנה דבר המעשה אשר שמו ראובן")
    a1="בהיות המספר אשר הוא שלשה תחת הדבר אשר במעשה אשר שמו ראובן שמו שמעון"
    a2="בהיות המספר אשר הוא ארבעה תחת הדבר אשר במעשה אשר שמו ראובן שמו לוי"
    associations=(a2+" "+a1.replace("בהיות","ובהיות",1)) if reverse else (a1+" "+a2.replace("בהיות","ובהיות",1))
    return "יהי מעשה ושמו ראובן "+decl1+" "+decl2+" "+body+" ועתה עשה את המעשה אשר שמו ראובן "+associations
