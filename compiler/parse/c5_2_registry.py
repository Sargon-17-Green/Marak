from __future__ import annotations

from compiler.parse.a13_b12_registry import A13_B12_REGISTRY
from compiler.parse.a15_numerals import (
    A15_DIRECT_NUMERAL_LEXICON_ID, A15_FEMININE_COUNT_LEXICON_ID,
)
from compiler.parse.grammar import (
    ConstructionDeclaration, ConstructionKind, ConstructionRegistry,
    CountedLabelTerminal, NameTerminal, Nonterminal, NumeralTerminal,
    Production, SpecStatus, WordTerminal,
)

LANGUAGE_EDITION = A13_B12_REGISTRY.language_edition
REGISTRY_VERSION = "c5.2-a15-a16.1"

def W(text:str)->WordTerminal: return WordTerminal(text)
def N(role:str)->NameTerminal: return NameTerminal(role)

_DECLS=A13_B12_REGISTRY.declarations+(
    ConstructionDeclaration("C52.PRODUCTIVE_NATURALS",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_PRODUCTIVE_NUMERALS",),"A15 direct Naturals 1..99,999,999 with exact canonical magnitude grammar."),
    ConstructionDeclaration("C52.SYMBOL_DECLARATIONS",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_SYMBOL_SURFACE",),"Finite Symbol domain/member declarations with counted canonical visible-label metadata."),
    ConstructionDeclaration("C52.SYMBOL_VALUE",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_SYMBOL_SURFACE","A16_TYPED_STATE_SURFACE","A16_TYPED_ROLE_SURFACE","A16_TYPED_OUTPUT_SURFACE"),"Exact domain-qualified Symbol values and typed carrier references."),
    ConstructionDeclaration("C52.SYMBOL_ORDER",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_SYMBOL_SURFACE",),"Explicit adjacent Symbol-order metadata."),
    ConstructionDeclaration("C52.INDEX_VALUE",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_BIDIRECTIONAL_INDEX_SURFACE","A16_INDEX_SUCCESSOR_PREDECESSOR"),"Year-profile BidirectionalIndex literals and total successor/predecessor."),
    ConstructionDeclaration("C52.TYPED_PLACE",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_TYPED_STATE_SURFACE",),"Symbol/Index place initialization, current content and replacement."),
    ConstructionDeclaration("C52.TYPED_ROLE",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_TYPED_ROLE_SURFACE",),"Symbol/Index named-role declarations and current occurrence values."),
    ConstructionDeclaration("C52.TYPED_ASSOCIATION",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_TYPED_ROLE_SURFACE",),"Named performance associations over independently typed values."),
    ConstructionDeclaration("C52.TYPED_OUTPUT",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_TYPED_OUTPUT_SURFACE",),"Symbol/Index output production and typed immediate-result references."),
    ConstructionDeclaration("C52.SYMBOL_EQUALITY",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A16_SYMBOL_EQUALITY",),"Same-domain Symbol identity proposition."),
    ConstructionDeclaration("C52.NATURAL_GT",ConstructionKind.POSITIVE,SpecStatus.NORMATIVE,("A15_NUMERIC_ORDERING",),"Strict Natural greater-than proposition."),
)

_FILTER={
    "A12.NUMBER.LITERAL",
    "A11.ROLE.ASSOCIATIONS.ONE","A11.ROLE.ASSOCIATIONS.MORE",
    "A11.ACT.PERFORM.WITH.ROLES",
}
_BASE=tuple(p for p in A13_B12_REGISTRY.productions if p.production_id not in _FILTER)

_PRODS=_BASE+(
    Production("C52.NUMBER.LITERAL","C52.PRODUCTIVE_NATURALS","NumberValue",(W("המספר"),W("אשר"),W("הוא"),NumeralTerminal(A15_DIRECT_NUMERAL_LEXICON_ID)),"C52.NATURAL_LITERAL"),

    Production("C52.SYMBOL.DOMAIN","C52.SYMBOL_DECLARATIONS","SymbolDomainDeclaration",(W("תהי"),W("משפחת"),W("שמות"),W("ושמה"),N("SymbolDomainName")),"C52.SYMBOL_DOMAIN"),
    Production("C52.PREP.SYMBOL.DOMAIN","C52.SYMBOL_DECLARATIONS","PreparatoryUnit",(Nonterminal("SymbolDomainDeclaration"),),"C52.PREP_SYMBOL_DOMAIN"),
    Production("C52.SYMBOL.MEMBER","C52.SYMBOL_DECLARATIONS","SymbolMemberDeclaration",(
        W("יהי"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),
        W("שם"),W("ושמו"),N("SymbolMemberName"),W("ולשם"),W("אשר"),W("במשפחת"),W("השמות"),
        W("אשר"),W("שמה"),N("SymbolDomainName"),W("שמו"),N("SymbolMemberName"),
        W("מספר"),W("המלים"),W("אשר"),W("בשמו"),W("הנראה"),W("יהיה"),
        CountedLabelTerminal(A15_DIRECT_NUMERAL_LEXICON_ID),
    ),"C52.SYMBOL_MEMBER"),
    Production("C52.PREP.SYMBOL.MEMBER","C52.SYMBOL_DECLARATIONS","PreparatoryUnit",(Nonterminal("SymbolMemberDeclaration"),),"C52.PREP_SYMBOL_MEMBER"),

    Production("C52.SYMBOL.REF","C52.SYMBOL_VALUE","SymbolValue",(
        W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("שמו"),N("SymbolMemberName")
    ),"C52.SYMBOL_REFERENCE"),
    Production("C52.SYMBOL.CURRENT.PLACE","C52.TYPED_PLACE","SymbolValue",(
        W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),
        W("ואשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")
    ),"C52.SYMBOL_CURRENT_PLACE"),
    Production("C52.SYMBOL.CURRENT.ROLE","C52.TYPED_ROLE","SymbolValue",(
        W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),
        W("ואשר"),W("במעשה"),W("הזה"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),
        W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("AssociatedRoleName")
    ),"C52.SYMBOL_CURRENT_ROLE"),
    Production("C52.SYMBOL.IMMEDIATE","C52.TYPED_OUTPUT","SymbolValue",(
        W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),
        W("ואשר"),W("יצא"),W("עתה"),W("מן"),W("המעשה"),W("אשר"),W("שמו"),N("ResultActionName")
    ),"C52.SYMBOL_IMMEDIATE"),

    Production("C52.INDEX.ZERO","C52.INDEX_VALUE","IndexValue",(W("שנת"),W("אין")),"C52.INDEX_ZERO"),
    Production("C52.INDEX.BEFORE.ONE","C52.INDEX_VALUE","IndexValue",(W("שנה"),W("אחת"),W("לפני"),W("שנת"),W("אין")),"C52.INDEX_BEFORE_ONE"),
    Production("C52.INDEX.AFTER.ONE","C52.INDEX_VALUE","IndexValue",(W("שנה"),W("אחת"),W("אחרי"),W("שנת"),W("אין")),"C52.INDEX_AFTER_ONE"),
    Production("C52.INDEX.BEFORE.TWO","C52.INDEX_VALUE","IndexValue",(W("שתי"),W("שנים"),W("לפני"),W("שנת"),W("אין")),"C52.INDEX_BEFORE_TWO"),
    Production("C52.INDEX.AFTER.TWO","C52.INDEX_VALUE","IndexValue",(W("שתי"),W("שנים"),W("אחרי"),W("שנת"),W("אין")),"C52.INDEX_AFTER_TWO"),
    Production("C52.INDEX.BEFORE.MANY","C52.INDEX_VALUE","IndexValue",(NumeralTerminal(A15_FEMININE_COUNT_LEXICON_ID),W("שנים"),W("לפני"),W("שנת"),W("אין")),"C52.INDEX_BEFORE_MANY"),
    Production("C52.INDEX.AFTER.MANY","C52.INDEX_VALUE","IndexValue",(NumeralTerminal(A15_FEMININE_COUNT_LEXICON_ID),W("שנים"),W("אחרי"),W("שנת"),W("אין")),"C52.INDEX_AFTER_MANY"),
    Production("C52.INDEX.CURRENT.PLACE","C52.TYPED_PLACE","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")),"C52.INDEX_CURRENT_PLACE"),
    Production("C52.INDEX.CURRENT.ROLE","C52.TYPED_ROLE","IndexValue",(
        W("מספר"),W("השנה"),W("אשר"),W("במעשה"),W("הזה"),W("עומד"),W("תחת"),W("הדבר"),W("אשר"),
        W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("AssociatedRoleName")
    ),"C52.INDEX_CURRENT_ROLE"),
    Production("C52.INDEX.IMMEDIATE","C52.TYPED_OUTPUT","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("יצא"),W("עתה"),W("מן"),W("המעשה"),W("אשר"),W("שמו"),N("ResultActionName")),"C52.INDEX_IMMEDIATE"),
    Production("C52.INDEX.SUCC","C52.INDEX_VALUE","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("אחר"),Nonterminal("IndexValue")),"C52.INDEX_SUCCESSOR"),
    Production("C52.INDEX.PRED","C52.INDEX_VALUE","IndexValue",(W("מספר"),W("השנה"),W("אשר"),W("לפני"),Nonterminal("IndexValue")),"C52.INDEX_PREDECESSOR"),

    Production("C52.PREP.PLACE.SYMBOL","C52.TYPED_PLACE","PreparatoryUnit",(
        W("יהי"),W("מקום"),W("ושמו"),N("PlaceName"),W("ובמקום"),W("אשר"),W("שמו"),N("PlaceName"),W("יהי"),Nonterminal("SymbolValue"),W("לבדו")
    ),"C52.PREP_PLACE_SYMBOL"),
    Production("C52.PREP.PLACE.INDEX","C52.TYPED_PLACE","PreparatoryUnit",(
        W("יהי"),W("מקום"),W("ושמו"),N("PlaceName"),W("ובמקום"),W("אשר"),W("שמו"),N("PlaceName"),W("יהי"),Nonterminal("IndexValue"),W("לבדו")
    ),"C52.PREP_PLACE_INDEX"),

    Production("C52.PLACE.REPLACE.SYMBOL","C52.TYPED_PLACE","AtomicAction",(
        W("שים"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName"),W("את"),Nonterminal("SymbolValue"),W("תחת"),
        W("השם"),W("אשר"),W("במשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("ואשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")
    ),"C52.REPLACE_SYMBOL"),
    Production("C52.PLACE.REPLACE.INDEX","C52.TYPED_PLACE","AtomicAction",(
        W("שים"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName"),W("את"),Nonterminal("IndexValue"),W("תחת"),
        W("מספר"),W("השנה"),W("אשר"),W("במקום"),W("אשר"),W("שמו"),N("PlaceName")
    ),"C52.REPLACE_INDEX"),

    Production("C52.ROLE.DECLARE.SYMBOL","C52.TYPED_ROLE","PreparatoryUnit",(
        W("יהי"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("דבר"),W("ושמו"),N("DeclaredRoleName"),
        W("ובעשות"),W("את"),W("המעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("יעמד"),W("שם"),
        W("ממשפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),
        W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("DeclaredRoleName")
    ),"C52.ROLE_SYMBOL"),
    Production("C52.ROLE.DECLARE.INDEX","C52.TYPED_ROLE","PreparatoryUnit",(
        W("יהי"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("דבר"),W("ושמו"),N("DeclaredRoleName"),
        W("ובעשות"),W("את"),W("המעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("יעמד"),W("מספר"),W("שנה"),
        W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("DeclaredRoleName")
    ),"C52.ROLE_INDEX"),

    Production("C52.ASSOC.VALUE.NATURAL","C52.TYPED_ASSOCIATION","AssociationValue",(Nonterminal("NumberValue"),),"C52.ASSOCIATION_VALUE"),
    Production("C52.ASSOC.VALUE.SYMBOL","C52.TYPED_ASSOCIATION","AssociationValue",(Nonterminal("SymbolValue"),),"C52.ASSOCIATION_VALUE"),
    Production("C52.ASSOC.VALUE.INDEX","C52.TYPED_ASSOCIATION","AssociationValue",(Nonterminal("IndexValue"),),"C52.ASSOCIATION_VALUE"),
    Production("C52.ROLE.ASSOC.ONE","C52.TYPED_ASSOCIATION","RoleAssociations",(
        W("בהיות"),Nonterminal("AssociationValue"),W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("AssociatedRoleName")
    ),"C52.ROLE_ASSOCIATION"),
    Production("C52.ROLE.ASSOC.MORE","C52.TYPED_ASSOCIATION","RoleAssociations",(
        Nonterminal("RoleAssociations"),W("ובהיות"),Nonterminal("AssociationValue"),W("תחת"),W("הדבר"),W("אשר"),W("במעשה"),W("אשר"),W("שמו"),N("RoleOwnerActionName"),W("שמו"),N("AssociatedRoleName")
    ),"C52.ROLE_ASSOCIATION"),
    Production("C52.ACT.PERFORM.ROLES","C52.TYPED_ASSOCIATION","AtomicAction",(
        W("עשה"),W("את"),W("המעשה"),W("אשר"),W("שמו"),N("PerformedActionName"),Nonterminal("RoleAssociations")
    ),"C52.ROLE_ASSOCIATION"),

    Production("C52.RESULT.PRODUCE.SYMBOL","C52.TYPED_OUTPUT","BodyAtomicAction",(W("הוצא"),W("מן"),W("המעשה"),W("הזה"),W("את"),Nonterminal("SymbolValue")),"C52.PRODUCE_SYMBOL"),
    Production("C52.RESULT.PRODUCE.INDEX","C52.TYPED_OUTPUT","BodyAtomicAction",(W("הוצא"),W("מן"),W("המעשה"),W("הזה"),W("את"),Nonterminal("IndexValue")),"C52.PRODUCE_INDEX"),

    Production("C52.PROP.SYMBOL.EQ","C52.SYMBOL_EQUALITY","Proposition",(Nonterminal("SymbolValue"),W("הוא"),Nonterminal("SymbolValue")),"C52.SYMBOL_EQUALITY"),
    Production("C52.PROP.NATURAL.GT","C52.NATURAL_GT","Proposition",(Nonterminal("NumberValue"),W("רב"),W("מן"),Nonterminal("NumberValue")),"C52.NATURAL_GT"),

    Production("C52.SYMBOL.ORDER","C52.SYMBOL_ORDER","SymbolOrderDeclaration",(
        W("במשפט"),W("משפחת"),W("השמות"),W("אשר"),W("שמה"),N("SymbolDomainName"),W("יהיה"),
        Nonterminal("SymbolValue"),W("מיד"),W("לפני"),Nonterminal("SymbolValue")
    ),"C52.SYMBOL_ORDER"),
    Production("C52.PREP.SYMBOL.ORDER","C52.SYMBOL_ORDER","PreparatoryUnit",(Nonterminal("SymbolOrderDeclaration"),),"C52.PREP_SYMBOL_ORDER"),
)

C5_2_REGISTRY=ConstructionRegistry(
    language_edition=LANGUAGE_EDITION,
    registry_version=REGISTRY_VERSION,
    source_snapshot="A13+B12+C5.1+A15+A16+B13+B15 integrated implementation candidate",
    declarations=_DECLS,
    productions=_PRODS,
    semantic_gates=A13_B12_REGISTRY.semantic_gates,
)

__all__=["C5_2_REGISTRY","REGISTRY_VERSION","LANGUAGE_EDITION"]
