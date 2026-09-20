from __future__ import annotations

from compiler.parse.c5_2_registry import C5_2_REGISTRY
from compiler.parse.grammar import (
    ConstructionDeclaration, ConstructionKind, ConstructionRegistry,
    NameTerminal, Nonterminal, Production, SpecStatus, WordTerminal,
)

LANGUAGE_EDITION = C5_2_REGISTRY.language_edition
REGISTRY_VERSION = "c5.3-a15-a16.1"

def W(text: str) -> WordTerminal: return WordTerminal(text)
def N(role: str) -> NameTerminal: return NameTerminal(role)
def NT(name: str) -> Nonterminal: return Nonterminal(name)

_DECLS=C5_2_REGISTRY.declarations+(
    ConstructionDeclaration("C53.COLLECTION_KIND",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_ORDERED_COLLECTION_SURFACE",),"The six admitted finite ordered book kinds only."),
    ConstructionDeclaration("C53.COLLECTION_VALUE",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_ORDERED_COLLECTION_SURFACE","B13_ORDERED_COLLECTION_MODEL"),"Typed empty books, pure append, selection and deterministic ordering."),
    ConstructionDeclaration("C53.COLLECTION_PROPOSITION",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_ORDERED_COLLECTION_SURFACE","B13_ORDERED_COLLECTION_MODEL"),"Collection membership proposition with domain semantic equality."),
    ConstructionDeclaration("C53.COLLECTION_CARRIER",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_TYPED_STATE_SURFACE","A16_TYPED_ROLE_SURFACE","A16_TYPED_OUTPUT_SURFACE","B15_DOMAIN_FLOW_SEMANTICS"),"Collection places, named roles, output and immediate result."),
)

P=[]

# Exact admitted book-kind heads. These are grammar metadata, not generic type syntax.
P += [
    Production("C53.KIND.NATURAL","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("מספרים")),"C53.KIND_NATURAL"),
    Production("C53.KIND.INDEX","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("מספרי"),W("שנים")),"C53.KIND_INDEX"),
    Production("C53.KIND.SYMBOL","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName")),"C53.KIND_SYMBOL"),
    Production("C53.KIND.NESTED.NATURAL","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("ספרי"),W("מספרים")),"C53.KIND_NESTED_NATURAL"),
    Production("C53.KIND.NESTED.INDEX","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("ספרי"),W("מספרי"),W("שנים")),"C53.KIND_NESTED_INDEX"),
    Production("C53.KIND.NESTED.SYMBOL","C53.COLLECTION_KIND","CollectionKind",(W("ספר"),W("ספרי"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName")),"C53.KIND_NESTED_SYMBOL"),
]

# Typed empty books.
P += [
    Production("C53.EMPTY.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("מספרים"),W("אשר"),W("אין"),W("בו"),W("מספר")),"C53.EMPTY"),
    Production("C53.EMPTY.INDEX","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("מספרי"),W("שנים"),W("אשר"),W("אין"),W("בו"),W("מספר"),W("שנה")),"C53.EMPTY"),
    Production("C53.EMPTY.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("אשר"),W("אין"),W("בו"),W("שם")),"C53.EMPTY"),
    Production("C53.EMPTY.NESTED.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("מספרים"),W("אשר"),W("אין"),W("בו"),W("ספר")),"C53.EMPTY"),
    Production("C53.EMPTY.NESTED.INDEX","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("מספרי"),W("שנים"),W("אשר"),W("אין"),W("בו"),W("ספר")),"C53.EMPTY"),
    Production("C53.EMPTY.NESTED.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("אשר"),W("אין"),W("בו"),W("ספר")),"C53.EMPTY"),
]

# Pure append. BOOK_VALUE and ITEM_VALUE must resolve independently.
P += [
    Production("C53.APPEND.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("מספרים"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("NumberValue")),"C53.APPEND"),
    Production("C53.APPEND.INDEX","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("מספרי"),W("שנים"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("IndexValue")),"C53.APPEND"),
    Production("C53.APPEND.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("SymbolValue")),"C53.APPEND"),
    Production("C53.APPEND.NESTED.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("מספרים"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("CollectionValue")),"C53.APPEND"),
    Production("C53.APPEND.NESTED.INDEX","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("מספרי"),W("שנים"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("CollectionValue")),"C53.APPEND"),
    Production("C53.APPEND.NESTED.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("ספר"),W("ספרי"),W("שמות"),W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("אשר"),W("בו"),W("כל"),W("אשר"),W("ב"),NT("CollectionValue"),W("כסדרו"),W("ואחר"),W("כלם"),NT("CollectionValue")),"C53.APPEND"),
]

# Count, current carriers and selection.
P += [
    Production("C53.COUNT","C53.COLLECTION_VALUE","NumberValue",(W("מספר"),W("הדברים"),W("אשר"),W("בתוך"),NT("CollectionValue")),"C53.COUNT"),
    Production("C53.CURRENT.PLACE","C53.COLLECTION_CARRIER","CollectionValue",(W("הספר"),W("אשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")),"C53.CURRENT_PLACE"),
    Production("C53.CURRENT.ROLE","C53.COLLECTION_CARRIER","CollectionValue",(W("הספר"),W("אשר"),W("במעשה"),W("הזה"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("AssociatedRoleName")),"C53.CURRENT_ROLE"),
    Production("C53.IMMEDIATE","C53.COLLECTION_CARRIER","CollectionValue",(W("הספר"),W("אשר"),W("יצא"),W("עתה"),W("מן"),W("המעשה"),W("אשר"),W("שמו"),N("ResultActionName")),"C53.IMMEDIATE"),
    Production("C53.FIRST.NATURAL","C53.COLLECTION_VALUE","NumberValue",(W("המספר"),W("אשר"),W("בראש"),NT("CollectionValue")),"C53.SELECT_FIRST"),
    Production("C53.LAST.NATURAL","C53.COLLECTION_VALUE","NumberValue",(W("המספר"),W("האחרון"),W("אשר"),W("בתוך"),NT("CollectionValue")),"C53.SELECT_LAST"),
    Production("C53.SELECT.NATURAL","C53.COLLECTION_VALUE","NumberValue",(W("המספר"),W("אשר"),W("מספרו"),W("בסדר"),NT("CollectionValue"),W("הוא"),NT("NumberValue")),"C53.SELECT_ORDINAL"),
    Production("C53.FIRST.INDEX","C53.COLLECTION_VALUE","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("בראש"),NT("CollectionValue")),"C53.SELECT_FIRST"),
    Production("C53.LAST.INDEX","C53.COLLECTION_VALUE","IndexValue",(W("מספר"),W("השנה"),W("האחרון"),W("אשר"),W("בתוך"),NT("CollectionValue")),"C53.SELECT_LAST"),
    Production("C53.SELECT.INDEX","C53.COLLECTION_VALUE","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("מספרו"),W("בסדר"),NT("CollectionValue"),W("הוא"),NT("NumberValue")),"C53.SELECT_ORDINAL"),
    Production("C53.FIRST.SYMBOL","C53.COLLECTION_VALUE","SymbolValue",(W("השם"),W("אשר"),W("בראש"),NT("CollectionValue")),"C53.SELECT_FIRST"),
    Production("C53.LAST.SYMBOL","C53.COLLECTION_VALUE","SymbolValue",(W("השם"),W("האחרון"),W("אשר"),W("בתוך"),NT("CollectionValue")),"C53.SELECT_LAST"),
    Production("C53.SELECT.SYMBOL","C53.COLLECTION_VALUE","SymbolValue",(W("השם"),W("אשר"),W("מספרו"),W("בסדר"),NT("CollectionValue"),W("הוא"),NT("NumberValue")),"C53.SELECT_ORDINAL"),
    Production("C53.FIRST.NESTED","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("אשר"),W("בראש"),NT("CollectionValue")),"C53.SELECT_FIRST"),
    Production("C53.LAST.NESTED","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("האחרון"),W("אשר"),W("בתוך"),NT("CollectionValue")),"C53.SELECT_LAST"),
    Production("C53.SELECT.NESTED","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("אשר"),W("מספרו"),W("בסדר"),NT("CollectionValue"),W("הוא"),NT("NumberValue")),"C53.SELECT_ORDINAL"),
]

# Membership propositions.
P += [
    Production("C53.MEMBER.NATURAL","C53.COLLECTION_PROPOSITION","Proposition",(NT("NumberValue"),W("כתוב"),W("בתוך"),NT("CollectionValue")),"C53.MEMBERSHIP"),
    Production("C53.MEMBER.INDEX","C53.COLLECTION_PROPOSITION","Proposition",(NT("IndexValue"),W("כתוב"),W("בתוך"),NT("CollectionValue")),"C53.MEMBERSHIP"),
    Production("C53.MEMBER.SYMBOL","C53.COLLECTION_PROPOSITION","Proposition",(NT("SymbolValue"),W("כתוב"),W("בתוך"),NT("CollectionValue")),"C53.MEMBERSHIP"),
    Production("C53.MEMBER.NESTED","C53.COLLECTION_PROPOSITION","Proposition",(NT("CollectionValue"),W("כתוב"),W("בתוך"),NT("CollectionValue")),"C53.MEMBERSHIP"),
]

# Deterministic order profiles only.
P += [
    Production("C53.ORDER.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("הערוך"),W("מן"),NT("CollectionValue"),W("מן"),W("המעט"),W("אל"),W("הרב")),"C53.ORDER_NATURAL"),
    Production("C53.ORDER.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("הערוך"),W("מן"),NT("CollectionValue"),W("כמשפט"),W("משפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName")),"C53.ORDER_SYMBOL"),
    Production("C53.ORDER.LEX.NATURAL","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("הערוך"),W("מן"),NT("CollectionValue"),W("מראש"),W("כל"),W("ספר"),W("ועד"),W("אחריתו"),W("מן"),W("המעט"),W("אל"),W("הרב")),"C53.ORDER_LEX_NATURAL"),
    Production("C53.ORDER.LEX.SYMBOL","C53.COLLECTION_VALUE","CollectionValue",(W("הספר"),W("הערוך"),W("מן"),NT("CollectionValue"),W("מראש"),W("כל"),W("ספר"),W("ועד"),W("אחריתו"),W("כמשפט"),W("משפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName")),"C53.ORDER_LEX_SYMBOL"),
]

# Collection-bearing A16 carriers.
P += [
    Production("C53.PREP.PLACE","C53.COLLECTION_CARRIER","PreparatoryUnit",(W("יהי"),W("מקום"),W("ושמו"),N("PlaceName"),W("ובמקום"),W("אשר"),W("שמו"),N("PlaceName"),W("יהי"),NT("CollectionValue"),W("לבדו")),"C53.PREP_PLACE"),
    Production("C53.PLACE.REPLACE","C53.COLLECTION_CARRIER","AtomicAction",(W("שים"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName"),W("את"),NT("CollectionValue"),W("תחת"),W("הספר"),W("אשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")),"C53.REPLACE"),
    Production("C53.ASSOC.VALUE","C53.COLLECTION_CARRIER","AssociationValue",(NT("CollectionValue"),),"C53.ASSOCIATION_VALUE"),
    Production("C53.RESULT.PRODUCE","C53.COLLECTION_CARRIER","BodyAtomicAction",(W("הוצא"),W("מן"),W("המעשה"),W("הזה"),W("את"),NT("CollectionValue")),"C53.PRODUCE"),
]

# Typed role declarations use exactly one admitted CollectionKind.
P += [
    Production("C53.ROLE.DECLARE","C53.COLLECTION_CARRIER","PreparatoryUnit",(
        W("יהי"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("דבר"),W("ושמו"),N("DeclaredRoleName"),
        W("ובעשות"),W("את"),W("המעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("יעמד"),NT("CollectionKind"),
        W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("DeclaredRoleName")
    ),"C53.ROLE_COLLECTION"),
]

C5_3_REGISTRY=ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="C5.2+A15/A16 finite ordered Collection production integration candidate",
    declarations=_DECLS,
    productions=C5_2_REGISTRY.productions+tuple(P),
    semantic_gates=C5_2_REGISTRY.semantic_gates,
)

__all__=["C5_3_REGISTRY","REGISTRY_VERSION","LANGUAGE_EDITION"]
