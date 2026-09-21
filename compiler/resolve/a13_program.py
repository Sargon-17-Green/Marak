from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json

from compiler.models.hast import (
    HastActBody, HastActIntroduction, HastAddNatural, HastConditional,
    HastCoreProgram, HastCurrentFact, HastCurrentRoleNumber, HastEqualProposition,
    HastExactNatural, HastExecutable, HastFixedRecurrence, HastNumber, HastValue,
    HastPerformAct, HastPlaceIntroduction, HastPostActionRecurrence,
    HastProduceResult, HastProposition, HastRecentResult, HastReplaceCurrentFact,
    HastRoleAssociation, HastRoleDeclaration, HastSubtractNatural, HastThen,
    HastPlaceDomain, HastRoleDomain, HastActOutputDomain, HastRepeatExactly,
    HastSymbolValue, HastCurrentValue, HastCurrentRoleValue, HastRecentTypedResult,
    HastIndexValue, HastIndexSuccessor, HastIndexPredecessor,
    HastNaturalGTProposition, HastIndexLTProposition, HastSymbolEqualProposition,
    HastSymbolDomainDeclaration, HastSymbolMemberDeclaration, HastSymbolOrderAdjacent,
    HastCollectionValue, HastCollectionAppend, HastCollectionCount,
    HastCollectionSelectNatural, HastCollectionSelectValue, HastCollectionOrder,
    HastCollectionMembershipProposition, HastProgramInputDomain,
    HastProgramInputNumber, HastProgramInputValue,
)
from compiler.models.domains import NATURAL, BIDIRECTIONAL_INDEX, CollectionDomain, Domain, ProgramInputId, SymbolDomain, SymbolDomainId, SymbolMemberId
from compiler.validate.domains import hast_value_domain
from compiler.models.symbols import ActId, PlaceId, RoleId
from compiler.parse.forest import ParseElement, ParseLeaf, ParseNode
from compiler.parse.c5_6_registry import COUNT_AS_NUMBER_ORIGINS
from compiler.source.source_map import OriginalSpan


@dataclass(frozen=True, slots=True)
class A13ResolutionIssue:
    code: str
    message_en: str
    message_he: str
    source_span: OriginalSpan | None
    metadata: dict[str, object]


class A13ResolutionError(Exception):
    def __init__(self, issue: A13ResolutionIssue):
        super().__init__(f"{issue.code}: {issue.message_en}")
        self.issue = issue


class _Env:
    def __init__(self) -> None:
        self.next_serial = 1
        self.places: dict[str, PlaceId] = {}
        self.acts: dict[str, ActId] = {}
        self.roles: dict[tuple[int, str], RoleId] = {}
        self.bodies: set[int] = set()
        self.place_domains: dict[PlaceId, Domain] = {}
        self.role_domains: dict[RoleId, Domain] = {}
        self.symbol_domains: dict[str, SymbolDomainId] = {}
        self.symbol_members: dict[tuple[int, str], tuple[SymbolMemberId, str]] = {}
        self.output_domains: dict[ActId, Domain | None] = {}
        self.program_inputs: dict[str, ProgramInputId] = {}
        self.program_input_domains: dict[ProgramInputId, Domain] = {}
        self.program_contract: str = "abstract-program-contract"

    def serial(self) -> int:
        value = self.next_serial
        self.next_serial += 1
        return value


class _UnresolvedOutputContract(Exception):
    def __init__(self, act: ActId, where: ParseLeaf | ParseNode):
        super().__init__(act.spelling)
        self.act = act
        self.where = where


def _body_env_snapshot(env: _Env) -> _Env:
    """Freeze source visibility at one body-definition point; share only output contracts."""
    snap = _Env()
    snap.next_serial = env.next_serial
    snap.places = dict(env.places)
    snap.acts = dict(env.acts)
    snap.roles = dict(env.roles)
    snap.bodies = set(env.bodies)
    snap.place_domains = dict(env.place_domains)
    snap.role_domains = dict(env.role_domains)
    snap.symbol_domains = dict(env.symbol_domains)
    snap.symbol_members = dict(env.symbol_members)
    # Output domains are whole-program contracts.  Sharing only this table lets a
    # deferred body learn a later-defined act's independently resolved contract
    # without gaining visibility of later source declarations.
    snap.output_domains = env.output_domains
    snap.program_inputs = dict(env.program_inputs)
    snap.program_input_domains = dict(env.program_input_domains)
    snap.program_contract = env.program_contract
    return snap


def _span(node: ParseNode | ParseLeaf) -> OriginalSpan | None:
    return node.original


def _program_contract_id(root: ParseNode) -> str:
    def obj(element: ParseElement):
        if isinstance(element, ParseLeaf):
            return ["leaf", element.terminal_role, element.text, element.numeric_value]
        return ["node", element.production_id, element.symbol, [obj(c) for c in element.children]]
    payload = json.dumps(obj(root), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "marak-program-sha256:" + hashlib.sha256(payload).hexdigest()


def _issue(code: str, en: str, he: str, where: ParseNode | ParseLeaf | None, **metadata) -> A13ResolutionError:
    return A13ResolutionError(A13ResolutionIssue(code, en, he, None if where is None else _span(where), dict(metadata)))


def _direct_leaves(node: ParseNode, role: str) -> tuple[ParseLeaf, ...]:
    return tuple(c for c in node.children if isinstance(c, ParseLeaf) and c.terminal_role == role)


def _all_leaves(element: ParseElement, role: str) -> tuple[ParseLeaf, ...]:
    if isinstance(element, ParseLeaf):
        return (element,) if element.terminal_role == role else ()
    out: list[ParseLeaf] = []
    for child in element.children:
        out.extend(_all_leaves(child, role))
    return tuple(out)


def _child_nodes(node: ParseNode, symbol: str) -> tuple[ParseNode, ...]:
    return tuple(c for c in node.children if isinstance(c, ParseNode) and c.symbol == symbol)


def _one_child(node: ParseNode, symbol: str) -> ParseNode:
    children = _child_nodes(node, symbol)
    if len(children) != 1:
        raise RuntimeError(f"internal parse contract: {node.production_id} expected one {symbol}, got {len(children)}")
    return children[0]


def _single_parse_child(node: ParseNode) -> ParseNode:
    children = tuple(c for c in node.children if isinstance(c, ParseNode))
    if len(children) != 1:
        raise RuntimeError(f"internal parse wrapper contract: {node.production_id}")
    return children[0]


def _flatten_preparation(node: ParseNode) -> list[ParseNode]:
    if node.production_id == "A13.PREPARATION.ONE":
        return [_one_child(node, "PreparatoryUnit")]
    if node.production_id == "A13.PREPARATION.MORE":
        return _flatten_preparation(_one_child(node, "Preparation")) + [_one_child(node, "PreparatoryUnit")]
    raise RuntimeError(f"not an A13 Preparation node: {node.production_id}")


def _flatten_sequence(node: ParseNode, *, body: bool) -> list[ParseNode]:
    one = "A12.BODY.SEQUENCE.ONE" if body else "A13.EXEC.SEQUENCE.ONE"
    more = "A12.BODY.SEQUENCE.MORE" if body else "A13.EXEC.SEQUENCE.MORE"
    unit_symbol = "BodyUnit" if body else "ExecutableUnit"
    seq_symbol = "BodySequence" if body else "ExecutableSequence"
    if node.production_id == one:
        return [_one_child(node, unit_symbol)]
    if node.production_id == more:
        return _flatten_sequence(_one_child(node, seq_symbol), body=body) + [_one_child(node, unit_symbol)]
    raise RuntimeError(f"not a sequence node: {node.production_id}")


def _resolve_place(name: str, env: _Env, where: ParseLeaf | ParseNode, *, self_name: str | None = None) -> PlaceId:
    if name not in env.places:
        if self_name is not None and name == self_name:
            raise _issue(
                "REF0106",
                "A place is not visible inside its own initializer.",
                "מקום אינו זמין בתוך הביטוי הקובע את תוכנו הראשוני שלו עצמו.",
                where,
                name=name,
            )
        raise _issue(
            "REF0101", "Place reference occurs before its complete introduction.",
            "הפניה למקום מופיעה לפני השלמת הצגתו.", where, kind="place", name=name,
        )
    return env.places[name]


def _resolve_act(name: str, env: _Env, where: ParseLeaf | ParseNode) -> ActId:
    if name not in env.acts:
        raise _issue(
            "REF0101", "Act reference occurs before its introduction.",
            "הפניה למעשה מופיעה לפני הצגתו.", where, kind="act", name=name,
        )
    return env.acts[name]


def _resolve_program_input(name: str, env: _Env, where: ParseLeaf | ParseNode) -> ProgramInputId:
    if name not in env.program_inputs:
        raise _issue(
            "REF0501", "Program Input reference occurs before its declaration.",
            "הפניה לקלט התוכנית מופיעה לפני הצהרתו.", where, kind="program-input", name=name,
        )
    return env.program_inputs[name]


def _resolve_symbol_domain(name: str, env: _Env, where: ParseLeaf | ParseNode) -> SymbolDomainId:
    if name not in env.symbol_domains:
        raise _issue("REF0201", "Symbol domain reference occurs before its declaration.", "הפניה למשפחת שמות מופיעה לפני הצגתה.", where, domain=name)
    return env.symbol_domains[name]


def _resolve_symbol_member(domain: SymbolDomainId, name: str, env: _Env, where: ParseLeaf | ParseNode) -> tuple[SymbolMemberId, str]:
    key=(domain.serial,name)
    if key not in env.symbol_members:
        raise _issue("REF0202", "Symbol member reference occurs before its declaration in the named domain.", "הפניה לשם במשפחה מופיעה לפני הצגתו.", where, domain=domain.spelling, member=name)
    return env.symbol_members[key]


def _resolve_role(owner: ActId, name: str, env: _Env, where: ParseLeaf | ParseNode) -> RoleId:
    key = (owner.serial, name)
    if key not in env.roles:
        raise _issue(
            "REF0101", "Role reference occurs before its declaration.",
            "הפניה לתפקיד מופיעה לפני הצהרתו.", where,
            kind="role", owner=owner.spelling, name=name,
        )
    return env.roles[key]


def _collection_kind_element_domain(node: ParseNode, env: _Env) -> Domain:
    pid=node.production_id
    if pid in {"C53.KIND.NATURAL","C53.EMPTY.NATURAL","C53.APPEND.NATURAL"}:
        return NATURAL
    if pid in {"C53.KIND.INDEX","C53.EMPTY.INDEX","C53.APPEND.INDEX"}:
        return BIDIRECTIONAL_INDEX
    if pid in {"C53.KIND.NESTED.NATURAL","C53.EMPTY.NESTED.NATURAL","C53.APPEND.NESTED.NATURAL"}:
        return CollectionDomain(NATURAL)
    if pid in {"C53.KIND.NESTED.INDEX","C53.EMPTY.NESTED.INDEX","C53.APPEND.NESTED.INDEX"}:
        return CollectionDomain(BIDIRECTIONAL_INDEX)
    if pid in {
        "C53.KIND.SYMBOL","C53.EMPTY.SYMBOL","C53.APPEND.SYMBOL",
        "C53.KIND.NESTED.SYMBOL","C53.EMPTY.NESTED.SYMBOL","C53.APPEND.NESTED.SYMBOL",
    }:
        leaves=_direct_leaves(node,"SymbolDomainName")
        if len(leaves)!=1:
            raise RuntimeError("Collection Symbol book-kind domain-head contract")
        base=SymbolDomain(_resolve_symbol_domain(leaves[0].text,env,leaves[0]))
        if "NESTED" in pid:
            return CollectionDomain(base)
        return base
    raise RuntimeError(f"unsupported Collection book kind {pid}")


def _require_collection_domain(value: HastValue, where: ParseNode | ParseLeaf) -> CollectionDomain:
    domain=hast_value_domain(value)
    if not isinstance(domain,CollectionDomain):
        raise _issue(
            "SEM0401","Collection expression requires an independently resolved Collection domain.",
            "ביטוי ספר דורש תחום Collection שנפתר באופן עצמאי.",where,actual_domain=repr(domain),
        )
    return domain


def _body_output_domains(action: HastExecutable) -> set[Domain]:
    if isinstance(action,HastProduceResult):
        return {hast_value_domain(action.value)}
    if isinstance(action,HastThen):
        out:set[Domain]=set()
        for x in action.actions:
            out.update(_body_output_domains(x))
        return out
    if isinstance(action,HastConditional):
        return _body_output_domains(action.if_holds) | _body_output_domains(action.if_not)
    if isinstance(action,(HastFixedRecurrence,HastRepeatExactly,HastPostActionRecurrence)):
        return _body_output_domains(action.action)
    return set()


def _lower_number(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
    pending_self_place: str | None = None,
) -> HastNumber:
    span = node.original
    if span is None:
        raise RuntimeError("number node lacks source span")
    pid = node.production_id
    if pid in {"A12.NUMBER.LITERAL", "C52.NUMBER.LITERAL"}:
        role = "Numeral:a12-direct-1-9999" if pid == "A12.NUMBER.LITERAL" else "Numeral:a15-direct-1-99999999"
        leaves = tuple(l for l in _all_leaves(node, role) if l.numeric_value is not None)
        if len(leaves) != 1:
            raise RuntimeError("literal numeral leaf contract")
        return HastExactNatural(span, leaves[0].numeric_value)  # type: ignore[arg-type]
    if pid == "C55.INPUT.READ.NATURAL":
        leaf = _direct_leaves(node, "ProgramInputRoleName")[0]
        input_id = _resolve_program_input(leaf.text, env, leaf)
        if env.program_input_domains.get(input_id) != NATURAL:
            raise _issue("REF0503", "Natural Program Input head disagrees with the declared input domain.", "ראש מספרי של קלט התוכנית אינו מתאים לתחום הקלט המוצהר.", leaf, role=leaf.text)
        return HastProgramInputNumber(span, input_id)
    if pid == "A10.PLACE.CURRENT_NUMBER":
        leaf = _direct_leaves(node, "PlaceName")[0]
        return HastCurrentFact(span, _resolve_place(leaf.text, env, leaf, self_name=pending_self_place))
    if pid == "A11.NUMBER.CURRENT.ROLE":
        owner_leaf = _direct_leaves(node, "RoleOwnerActionName")[0]
        role_leaf = _direct_leaves(node, "AssociatedRoleName")[0]
        owner = _resolve_act(owner_leaf.text, env, owner_leaf)
        role = _resolve_role(owner, role_leaf.text, env, role_leaf)
        if current_act != owner:
            raise _issue(
                "REF0110", "A current role number is available only in an occurrence of its owning act.",
                "המספר הנוכחי של תפקיד זמין רק בעת ביצוע המעשה שהוא בעל התפקיד.",
                role_leaf, owner=owner.spelling, role=role.spelling,
            )
        return HastCurrentRoleNumber(span, role)
    if pid == "A12.RESULT.IMMEDIATE.SINGLE":
        leaf = _direct_leaves(node, "ResultActionName")[0]
        act = _resolve_act(leaf.text, env, leaf)
        if recent_act is None:
            raise _issue(
                "REF0112", "Immediate result reference has no structurally immediate preceding performance.",
                "להפניית התוצאה המיידית אין ביצוע קודם הצמוד לה מבחינה מבנית.",
                leaf, act=act.spelling,
            )
        if recent_act != act:
            raise _issue(
                "REF0113", "Immediate result reference names a different act from the directly preceding performance.",
                "הפניית התוצאה המיידית נוקבת במעשה שונה מן הביצוע הקודם הישיר.",
                leaf, expected=recent_act.spelling, actual=act.spelling,
            )
        return HastRecentResult(span, act)
    if pid == "C53.COUNT":
        book=_lower_collection(_one_child(node,"CollectionValue"),env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        _require_collection_domain(book,node)
        return HastCollectionCount(span,book)
    if pid in {"C53.FIRST.NATURAL","C53.LAST.NATURAL","C53.SELECT.NATURAL"}:
        children=_child_nodes(node,"CollectionValue")
        if len(children)!=1:
            raise RuntimeError("Natural Collection selection book contract")
        book=_lower_collection(children[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        domain=_require_collection_domain(book,node)
        if domain.element_domain!=NATURAL:
            raise _issue("SEM0402","Natural element head requires a book of Naturals.","ראש איבר מספרי דורש ספר מספרים.",node,book_domain=repr(domain))
        mode="first" if ".FIRST." in pid else "last" if ".LAST." in pid else "ordinal"
        position=None
        if mode=="ordinal":
            nums=_child_nodes(node,"NumberValue")
            if len(nums)!=1:
                raise RuntimeError("Collection ordinal position contract")
            position=_lower_number(nums[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        return HastCollectionSelectNatural(span,book,position,mode)
    if pid == "A9.NUMBER.ADD":
        nums = _child_nodes(node, "NumberValue")
        if len(nums) != 2:
            raise RuntimeError("addition arity contract")
        return HastAddNatural(
            span,
            _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
            _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
        )
    if pid == "A9.NUMBER.SUBTRACT":
        nums = _child_nodes(node, "NumberValue")
        if len(nums) != 2:
            raise RuntimeError("subtraction arity contract")
        return HastSubtractNatural(
            span,
            _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
            _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act, pending_self_place=pending_self_place),
        )
    raise RuntimeError(f"unsupported admitted NumberValue production {pid}")


def _lower_symbol(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
    pending_self_place: str | None = None,
) -> HastValue:
    if node.original is None:
        raise RuntimeError("SymbolValue node lacks source span")
    pid=node.production_id
    if pid in {"C53.FIRST.SYMBOL","C53.LAST.SYMBOL","C53.SELECT.SYMBOL"}:
        children=_child_nodes(node,"CollectionValue")
        if len(children)!=1:
            raise RuntimeError("Symbol Collection selection book contract")
        book=_lower_collection(children[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        domain=_require_collection_domain(book,node)
        if not isinstance(domain.element_domain,SymbolDomain):
            raise _issue("SEM0403","Symbol element head requires a book from one Symbol domain.","ראש איבר של שם דורש ספר שמות ממשפחת שמות אחת.",node,book_domain=repr(domain))
        mode="first" if ".FIRST." in pid else "last" if ".LAST." in pid else "ordinal"
        position=None
        if mode=="ordinal":
            nums=_child_nodes(node,"NumberValue")
            if len(nums)!=1:
                raise RuntimeError("Collection ordinal position contract")
            position=_lower_number(nums[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        return HastCollectionSelectValue(node.original,book,domain.element_domain,position,mode)
    domains=_direct_leaves(node,"SymbolDomainName")
    if not domains:
        raise RuntimeError(f"SymbolValue lacks explicit domain head: {pid}")
    domain=_resolve_symbol_domain(domains[0].text,env,domains[0])
    expected=SymbolDomain(domain)
    if pid=="C55.INPUT.READ.SYMBOL":
        role_leaf=_direct_leaves(node,"ProgramInputRoleName")[0]
        input_id=_resolve_program_input(role_leaf.text,env,role_leaf)
        if env.program_input_domains.get(input_id)!=expected:
            raise _issue("REF0503","Symbol Program Input head names a domain different from the declared input domain.","ראש משפחת השמות של קלט התוכנית מציין תחום שונה מתחום הקלט המוצהר.",domains[0],role=role_leaf.text,domain=domain.spelling)
        return HastProgramInputValue(node.original,input_id,expected)
    if pid=="C52.SYMBOL.REF":
        member_leaf=_direct_leaves(node,"SymbolMemberName")[0]
        member,label=_resolve_symbol_member(domain,member_leaf.text,env,member_leaf)
        return HastSymbolValue(node.original,domain,member,label)
    if pid=="C52.SYMBOL.CURRENT.PLACE":
        place_leaf=_direct_leaves(node,"PlaceName")[0]
        place=_resolve_place(place_leaf.text,env,place_leaf,self_name=pending_self_place)
        if env.place_domains.get(place)!=expected:
            raise _issue("REF0203","Symbol current-place head names a domain different from the place's static domain.","ראש משפחת השמות של הערך הנוכחי במקום מציין תחום שונה מן התחום הסטטי של המקום.",domains[0],place=place.spelling,domain=domain.spelling)
        return HastCurrentValue(node.original,place,expected)
    if pid=="C52.SYMBOL.CURRENT.ROLE":
        owner_leaf=_direct_leaves(node,"RoleOwnerActionName")[0]
        role_leaf=_direct_leaves(node,"AssociatedRoleName")[0]
        owner=_resolve_act(owner_leaf.text,env,owner_leaf)
        role=_resolve_role(owner,role_leaf.text,env,role_leaf)
        if current_act!=owner:
            raise _issue("REF0110","A current role value is available only in an occurrence of its owning act.","הערך הנוכחי של תפקיד זמין רק בעת ביצוע המעשה שהוא בעל התפקיד.",role_leaf,owner=owner.spelling,role=role.spelling)
        if env.role_domains.get(role)!=expected:
            raise _issue("REF0204","Symbol current-role head names a domain different from the role's static domain.","ראש משפחת השמות של הערך הנוכחי בתפקיד מציין תחום שונה מן התחום הסטטי של התפקיד.",domains[0],role=role.spelling,domain=domain.spelling)
        return HastCurrentRoleValue(node.original,role,expected)
    if pid=="C52.SYMBOL.IMMEDIATE":
        act_leaf=_direct_leaves(node,"ResultActionName")[0]
        act=_resolve_act(act_leaf.text,env,act_leaf)
        if recent_act is None:
            raise _issue("REF0112","Immediate result reference has no structurally immediate preceding performance.","להפניית התוצאה המיידית אין ביצוע קודם הצמוד לה מבחינה מבנית.",act_leaf,act=act.spelling)
        if recent_act!=act:
            raise _issue("REF0113","Immediate result reference names a different act from the directly preceding performance.","הפניית התוצאה המיידית נוקבת במעשה שונה מן הביצוע הקודם הישיר.",act_leaf,expected=recent_act.spelling,actual=act.spelling)
        return HastRecentTypedResult(node.original,act,expected)
    raise RuntimeError(f"unsupported admitted SymbolValue production {pid}")


def _lower_index(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
    pending_self_place: str | None = None,
) -> HastValue:
    if node.original is None:
        raise RuntimeError("IndexValue node lacks source span")
    pid=node.production_id
    if pid in {"C53.FIRST.INDEX","C53.LAST.INDEX","C53.SELECT.INDEX"}:
        children=_child_nodes(node,"CollectionValue")
        if len(children)!=1:
            raise RuntimeError("Index Collection selection book contract")
        book=_lower_collection(children[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        domain=_require_collection_domain(book,node)
        if domain.element_domain!=BIDIRECTIONAL_INDEX:
            raise _issue("SEM0404","Year-number element head requires a book of BidirectionalIndex values.","ראש איבר של מספר שנה דורש ספר מספרי שנים.",node,book_domain=repr(domain))
        mode="first" if ".FIRST." in pid else "last" if ".LAST." in pid else "ordinal"
        position=None
        if mode=="ordinal":
            nums=_child_nodes(node,"NumberValue")
            if len(nums)!=1:
                raise RuntimeError("Collection ordinal position contract")
            position=_lower_number(nums[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        return HastCollectionSelectValue(node.original,book,BIDIRECTIONAL_INDEX,position,mode)
    if pid in {"C55.INPUT.READ.INDEX","C56.INPUT.READ.INDEX"}:
        leaf=_direct_leaves(node,"ProgramInputRoleName")[0]
        input_id=_resolve_program_input(leaf.text,env,leaf)
        if env.program_input_domains.get(input_id)!=BIDIRECTIONAL_INDEX:
            raise _issue("REF0503","Year-index Program Input head disagrees with the declared input domain.","ראש מספר השנה של קלט התוכנית אינו מתאים לתחום הקלט המוצהר.",leaf,role=leaf.text)
        return HastProgramInputValue(node.original,input_id,BIDIRECTIONAL_INDEX)
    if pid in {"C52.INDEX.ZERO","C56.INDEX.GENERAL.ZERO"}: return HastIndexValue(node.original,"zero",0)
    if pid in {"C52.INDEX.BEFORE.ONE","C56.INDEX.GENERAL.BEFORE.ONE"}: return HastIndexValue(node.original,"before",1)
    if pid in {"C52.INDEX.AFTER.ONE","C56.INDEX.GENERAL.AFTER.ONE"}: return HastIndexValue(node.original,"after",1)
    if pid in {"C52.INDEX.BEFORE.TWO","C56.INDEX.GENERAL.BEFORE.TWO"}: return HastIndexValue(node.original,"before",2)
    if pid in {"C52.INDEX.AFTER.TWO","C56.INDEX.GENERAL.AFTER.TWO"}: return HastIndexValue(node.original,"after",2)
    if pid in {"C52.INDEX.BEFORE.MANY","C52.INDEX.AFTER.MANY","C56.INDEX.GENERAL.BEFORE.MANY","C56.INDEX.GENERAL.AFTER.MANY"}:
        leaves=tuple(x for x in _all_leaves(node,"Numeral:a15-feminine-count-3-99999999") if x.numeric_value is not None)
        if len(leaves)!=1: raise RuntimeError("Index distance numeral contract")
        return HastIndexValue(node.original,"before" if "BEFORE" in pid else "after",leaves[0].numeric_value)
    if pid in {"C52.INDEX.CURRENT.PLACE","C56.INDEX.GENERAL.CURRENT.PLACE"}:
        leaf=_direct_leaves(node,"PlaceName")[0]
        place=_resolve_place(leaf.text,env,leaf,self_name=pending_self_place)
        if env.place_domains.get(place)!=BIDIRECTIONAL_INDEX:
            raise _issue("REF0210","Index current-place reference requires a BidirectionalIndex place.","הפניית אינדקס לערך הנוכחי במקום מחייבת מקום שתחומו BidirectionalIndex.",leaf,place=place.spelling)
        return HastCurrentValue(node.original,place,BIDIRECTIONAL_INDEX)
    if pid in {"C52.INDEX.CURRENT.ROLE","C56.INDEX.GENERAL.CURRENT.ROLE"}:
        owner_leaf=_direct_leaves(node,"RoleOwnerActionName")[0]
        role_leaf=_direct_leaves(node,"AssociatedRoleName")[0]
        owner=_resolve_act(owner_leaf.text,env,owner_leaf); role=_resolve_role(owner,role_leaf.text,env,role_leaf)
        if current_act!=owner:
            raise _issue("REF0110","A current role value is available only in an occurrence of its owning act.","הערך הנוכחי של תפקיד זמין רק בעת ביצוע המעשה שהוא בעל התפקיד.",role_leaf,owner=owner.spelling,role=role.spelling)
        if env.role_domains.get(role)!=BIDIRECTIONAL_INDEX:
            raise _issue("REF0211","Index current-role reference requires a BidirectionalIndex role.","הפניית אינדקס לערך הנוכחי בתפקיד מחייבת תפקיד שתחומו BidirectionalIndex.",role_leaf,role=role.spelling)
        return HastCurrentRoleValue(node.original,role,BIDIRECTIONAL_INDEX)
    if pid in {"C52.INDEX.IMMEDIATE","C56.INDEX.GENERAL.IMMEDIATE"}:
        leaf=_direct_leaves(node,"ResultActionName")[0]; act=_resolve_act(leaf.text,env,leaf)
        if recent_act is None:
            raise _issue("REF0112","Immediate result reference has no structurally immediate preceding performance.","להפניית התוצאה המיידית אין ביצוע קודם הצמוד לה מבחינה מבנית.",leaf,act=act.spelling)
        if recent_act!=act:
            raise _issue("REF0113","Immediate result reference names a different act from the directly preceding performance.","הפניית התוצאה המיידית נוקבת במעשה שונה מן הביצוע הקודם הישיר.",leaf,expected=recent_act.spelling,actual=act.spelling)
        return HastRecentTypedResult(node.original,act,BIDIRECTIONAL_INDEX)
    if pid in {"C52.INDEX.SUCC","C52.INDEX.PRED","C56.INDEX.GENERAL.SUCC","C56.INDEX.GENERAL.PRED"}:
        operand=_lower_index(_one_child(node,"IndexValue"),env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        return HastIndexSuccessor(node.original,operand) if pid.endswith("SUCC") else HastIndexPredecessor(node.original,operand)
    raise RuntimeError(f"unsupported admitted IndexValue production {pid}")


def _lower_collection(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
    pending_self_place: str | None = None,
) -> HastValue:
    if node.original is None:
        raise RuntimeError("CollectionValue node lacks source span")
    pid=node.production_id
    if pid=="C55.INPUT.READ.COLLECTION":
        leaf=_direct_leaves(node,"ProgramInputRoleName")[0]
        input_id=_resolve_program_input(leaf.text,env,leaf)
        domain=env.program_input_domains.get(input_id)
        if not isinstance(domain,CollectionDomain):
            raise _issue("REF0503","Collection Program Input head requires a Collection input contract.","ראש ספר של קלט התוכנית דורש קלט שתחומו Collection.",leaf,role=leaf.text)
        return HastProgramInputValue(node.original,input_id,domain)
    if pid.startswith("C53.EMPTY."):
        element_domain=_collection_kind_element_domain(node,env)
        return HastCollectionValue(node.original,element_domain,())

    if pid.startswith("C53.APPEND."):
        element_domain=_collection_kind_element_domain(node,env)
        books=_child_nodes(node,"CollectionValue")
        if pid in {"C53.APPEND.NESTED.NATURAL","C53.APPEND.NESTED.INDEX","C53.APPEND.NESTED.SYMBOL"}:
            if len(books)!=2:
                raise RuntimeError("nested Collection append arity")
            source=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
            item=_lower_collection(books[1],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        else:
            if len(books)!=1:
                raise RuntimeError("Collection append source arity")
            source=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
            item_symbol="NumberValue" if pid=="C53.APPEND.NATURAL" else "IndexValue" if pid=="C53.APPEND.INDEX" else "SymbolValue"
            item=_lower_value(_one_child(node,item_symbol),env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        source_domain=_require_collection_domain(source,node)
        if source_domain!=CollectionDomain(element_domain):
            raise _issue("SEM0405","Pure append book kind disagrees with the source book domain.","סוג הספר בהוספה הטהורה אינו מתאים לתחום הספר המקורי.",node,expected=repr(CollectionDomain(element_domain)),actual=repr(source_domain))
        if hast_value_domain(item)!=element_domain:
            raise _issue("SEM0406","Pure append item does not belong to the book element domain.","האיבר הנוסף לספר אינו שייך לתחום איברי הספר.",node,expected=repr(element_domain),actual=repr(hast_value_domain(item)))
        return HastCollectionAppend(node.original,source,item,element_domain)

    if pid=="C53.CURRENT.PLACE":
        leaf=_direct_leaves(node,"PlaceName")[0]
        place=_resolve_place(leaf.text,env,leaf,self_name=pending_self_place)
        domain=env.place_domains.get(place)
        if not isinstance(domain,CollectionDomain):
            raise _issue("REF0401","Collection current-place reference requires a Collection-bearing place.","הפניית הספר שבמקום דורשת מקום הנושא Collection.",leaf,place=place.spelling)
        return HastCurrentValue(node.original,place,domain)

    if pid=="C53.CURRENT.ROLE":
        owner_leaf=_direct_leaves(node,"RoleOwnerActionName")[0]
        role_leaf=_direct_leaves(node,"AssociatedRoleName")[0]
        owner=_resolve_act(owner_leaf.text,env,owner_leaf)
        role=_resolve_role(owner,role_leaf.text,env,role_leaf)
        if current_act!=owner:
            raise _issue("REF0110","A current role value is available only in an occurrence of its owning act.","הערך הנוכחי של תפקיד זמין רק בעת ביצוע המעשה שהוא בעל התפקיד.",role_leaf,owner=owner.spelling,role=role.spelling)
        domain=env.role_domains.get(role)
        if not isinstance(domain,CollectionDomain):
            raise _issue("REF0402","Collection current-role reference requires a Collection-bearing role.","הפניית הספר שבתפקיד דורשת תפקיד הנושא Collection.",role_leaf,role=role.spelling)
        return HastCurrentRoleValue(node.original,role,domain)

    if pid=="C53.IMMEDIATE":
        leaf=_direct_leaves(node,"ResultActionName")[0]
        act=_resolve_act(leaf.text,env,leaf)
        if recent_act is None:
            raise _issue("REF0112","Immediate result reference has no structurally immediate preceding performance.","להפניית התוצאה המיידית אין ביצוע קודם הצמוד לה מבחינה מבנית.",leaf,act=act.spelling)
        if recent_act!=act:
            raise _issue("REF0113","Immediate result reference names a different act from the directly preceding performance.","הפניית התוצאה המיידית נוקבת במעשה שונה מן הביצוע הקודם הישיר.",leaf,expected=recent_act.spelling,actual=act.spelling)
        if act not in env.output_domains:
            raise _UnresolvedOutputContract(act,leaf)
        domain=env.output_domains[act]
        if not isinstance(domain,CollectionDomain):
            raise _issue("REF0403","Collection immediate-result head requires a Collection output contract.","ראש תוצאה מיידית של ספר דורש חוזה פלט מסוג Collection.",leaf,act=act.spelling,output_domain=repr(domain))
        return HastRecentTypedResult(node.original,act,domain)

    if pid in {"C53.FIRST.NESTED","C53.LAST.NESTED","C53.SELECT.NESTED"}:
        books=_child_nodes(node,"CollectionValue")
        if len(books)!=1:
            raise RuntimeError("nested Collection selection book contract")
        book=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        domain=_require_collection_domain(book,node)
        if not isinstance(domain.element_domain,CollectionDomain):
            raise _issue("SEM0407","Book element head requires a book of books.","ראש איבר של ספר דורש ספר ספרים.",node,book_domain=repr(domain))
        mode="first" if ".FIRST." in pid else "last" if ".LAST." in pid else "ordinal"
        position=None
        if mode=="ordinal":
            nums=_child_nodes(node,"NumberValue")
            if len(nums)!=1:
                raise RuntimeError("nested Collection ordinal position contract")
            position=_lower_number(nums[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        return HastCollectionSelectValue(node.original,book,domain.element_domain,position,mode)

    if pid in {"C53.ORDER.NATURAL","C53.ORDER.SYMBOL","C53.ORDER.LEX.NATURAL","C53.ORDER.LEX.SYMBOL"}:
        books=_child_nodes(node,"CollectionValue")
        if len(books)!=1:
            raise RuntimeError("Collection order source contract")
        book=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
        actual=_require_collection_domain(book,node)
        symbol_domain_id=None
        if pid=="C53.ORDER.NATURAL":
            element_domain=NATURAL; kind="natural"
        elif pid=="C53.ORDER.LEX.NATURAL":
            element_domain=CollectionDomain(NATURAL); kind="lex-natural"
        else:
            leaf=_direct_leaves(node,"SymbolDomainName")[0]
            symbol_domain_id=_resolve_symbol_domain(leaf.text,env,leaf)
            symbol_domain=SymbolDomain(symbol_domain_id)
            if pid=="C53.ORDER.SYMBOL":
                element_domain=symbol_domain; kind="symbol"
            else:
                element_domain=CollectionDomain(symbol_domain); kind="lex-symbol"
        if actual!=CollectionDomain(element_domain):
            raise _issue("SEM0408","Collection order profile does not apply to the resolved book domain.","פרופיל סדר הספר אינו חל על תחום הספר שנפתר.",node,expected=repr(CollectionDomain(element_domain)),actual=repr(actual))
        return HastCollectionOrder(node.original,book,element_domain,kind,symbol_domain_id)

    raise RuntimeError(f"unsupported admitted CollectionValue production {pid}")


def _lower_value(node: ParseNode, env: _Env, *, current_act: ActId | None, recent_act: ActId | None, pending_self_place: str | None=None) -> HastValue:
    if node.symbol=="AssociationValue":
        return _lower_value(_single_parse_child(node),env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
    if node.symbol=="NumberValue":
        return _lower_number(node,env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
    if node.symbol=="SymbolValue":
        return _lower_symbol(node,env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
    if node.symbol=="IndexValue":
        return _lower_index(node,env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
    if node.symbol=="CollectionValue":
        return _lower_collection(node,env,current_act=current_act,recent_act=recent_act,pending_self_place=pending_self_place)
    raise RuntimeError(f"unsupported Value category {node.symbol}")


def _lower_proposition(node: ParseNode, env: _Env, *, current_act: ActId | None, recent_act: ActId | None) -> HastProposition:
    assert node.original is not None
    if node.production_id == "A9.PROPOSITION.NUMERIC_IDENTITY":
        nums = _child_nodes(node, "NumberValue")
        assert len(nums) == 2
        return HastEqualProposition(
            node.original,
            _lower_number(nums[0], env, current_act=current_act, recent_act=recent_act),
            _lower_number(nums[1], env, current_act=current_act, recent_act=recent_act),
        )
    if node.production_id == "C52.PROP.NATURAL.GT":
        nums=_child_nodes(node,"NumberValue")
        assert len(nums)==2
        return HastNaturalGTProposition(node.original,
            _lower_number(nums[0],env,current_act=current_act,recent_act=recent_act),
            _lower_number(nums[1],env,current_act=current_act,recent_act=recent_act))
    if node.production_id == "C56.PROP.INDEX.LT":
        vals=_child_nodes(node,"IndexValue")
        if len(vals)!=2:
            raise RuntimeError("Index strict-order arity")
        left=_lower_index(vals[0],env,current_act=current_act,recent_act=recent_act)
        right=_lower_index(vals[1],env,current_act=current_act,recent_act=recent_act)
        ld=hast_value_domain(left); rd=hast_value_domain(right)
        if ld!=BIDIRECTIONAL_INDEX or rd!=BIDIRECTIONAL_INDEX:
            raise _issue(
                "SEM0501",
                "Index strict-order operands must independently resolve to BidirectionalIndex.",
                "אופרנדי סדר אינדקס קפדני חייבים להיפתר בנפרד לתחום BidirectionalIndex.",
                node,
                left_domain=repr(ld),
                right_domain=repr(rd),
            )
        return HastIndexLTProposition(node.original,left,right)
    if node.production_id == "C52.PROP.SYMBOL.EQ":
        vals=_child_nodes(node,"SymbolValue")
        assert len(vals)==2
        left=_lower_symbol(vals[0],env,current_act=current_act,recent_act=recent_act)
        right=_lower_symbol(vals[1],env,current_act=current_act,recent_act=recent_act)
        ld=hast_value_domain(left); rd=hast_value_domain(right)
        if ld != rd or not isinstance(ld,SymbolDomain):
            raise _issue("SEM0301","Symbol equality operands must independently resolve to the same declared Symbol domain.","אופרנדי השוויון של Symbol חייבים להיפתר בנפרד לאותו תחום Symbol מוצהר.",node,left_domain=repr(ld),right_domain=repr(rd))
        return HastSymbolEqualProposition(node.original,left,right,ld.identity)
    if node.production_id.startswith("C53.MEMBER."):
        books=_child_nodes(node,"CollectionValue")
        if node.production_id=="C53.MEMBER.NESTED":
            if len(books)!=2:
                raise RuntimeError("nested Collection membership arity")
            item=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act)
            book=_lower_collection(books[1],env,current_act=current_act,recent_act=recent_act)
        else:
            if len(books)!=1:
                raise RuntimeError("Collection membership book arity")
            book=_lower_collection(books[0],env,current_act=current_act,recent_act=recent_act)
            item_symbol="NumberValue" if node.production_id=="C53.MEMBER.NATURAL" else "IndexValue" if node.production_id=="C53.MEMBER.INDEX" else "SymbolValue"
            item=_lower_value(_one_child(node,item_symbol),env,current_act=current_act,recent_act=recent_act)
        domain=_require_collection_domain(book,node)
        item_domain=hast_value_domain(item)
        if item_domain!=domain.element_domain:
            raise _issue("SEM0409","Collection membership item has a different domain from the book elements.","האיבר הנבדק כחבר בספר שייך לתחום שונה מתחום איברי הספר.",node,book_domain=repr(domain),item_domain=repr(item_domain))
        return HastCollectionMembershipProposition(node.original,item,book,domain.element_domain)
    raise RuntimeError(f"unsupported proposition {node.production_id}")


def _flatten_role_associations(node: ParseNode) -> list[ParseNode]:
    if node.production_id in {"A11.ROLE.ASSOCIATIONS.ONE","C52.ROLE.ASSOC.ONE"}:
        return [node]
    if node.production_id in {"A11.ROLE.ASSOCIATIONS.MORE","C52.ROLE.ASSOC.MORE"}:
        prev = _one_child(node, "RoleAssociations")
        return _flatten_role_associations(prev) + [node]
    raise RuntimeError(f"unexpected role association production {node.production_id}")


def _lower_count_as_number(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
) -> HastNumber:
    """Lower the exact NumberValue production from which כמספר was derived."""
    original_id = COUNT_AS_NUMBER_ORIGINS.get(node.production_id)
    if original_id is None:
        raise RuntimeError(f"unexpected CountAsNumber production {node.production_id}")
    number_node = replace(node, production_id=original_id, symbol="NumberValue")
    return _lower_number(number_node, env, current_act=current_act, recent_act=recent_act)


def _repeat_count(node: ParseNode) -> int:
    mapping = {
        "A9.REPEAT.COUNT.3": 3, "A9.REPEAT.COUNT.4": 4, "A9.REPEAT.COUNT.5": 5,
        "A9.REPEAT.COUNT.6": 6, "A9.REPEAT.COUNT.7": 7, "A9.REPEAT.COUNT.8": 8,
        "A9.REPEAT.COUNT.9": 9,
    }
    try:
        return mapping[node.production_id]
    except KeyError as exc:
        raise RuntimeError(f"unexpected repeat count production {node.production_id}") from exc


def _lower_action(
    node: ParseNode,
    env: _Env,
    *,
    current_act: ActId | None,
    recent_act: ActId | None,
) -> HastExecutable:
    # Semantic-category wrappers are transparent; the category itself remains
    # in HAST through the concrete admitted child.
    if node.symbol in {"BodyUnit", "ExecutableUnit"}:
        return _lower_action(_single_parse_child(node), env, current_act=current_act, recent_act=recent_act)
    pid = node.production_id
    span = node.original
    if span is None:
        raise RuntimeError("action node lacks source span")

    if pid == "A10.PLACE.REPLACE":
        names = _direct_leaves(node, "PlaceName")
        if len(names) != 2:
            raise RuntimeError("replace place-name contract")
        if names[0].text != names[1].text:
            raise _issue(
                "REF0001", "Replacement destination descriptions must co-refer explicitly.",
                "תיאורי יעד ההחלפה חייבים להתייחס במפורש לאותו מקום.", names[1],
                expected=names[0].text, actual=names[1].text,
            )
        place = _resolve_place(names[0].text, env, names[0])
        value = _lower_number(_one_child(node, "NumberValue"), env, current_act=current_act, recent_act=recent_act)
        return HastReplaceCurrentFact(span, place, value)

    if pid=="C53.PLACE.REPLACE":
        names=_direct_leaves(node,"PlaceName")
        if len(names)!=2 or names[0].text!=names[1].text:
            raise _issue("REF0001","Typed replacement destination and displaced current-value description must name the same place.","יעד ההחלפה בעל הטיפוס ותיאור הערך הנוכחי המוחלף חייבים לנקוב באותו מקום.",names[-1] if names else node)
        place=_resolve_place(names[0].text,env,names[0])
        expected=env.place_domains.get(place)
        if not isinstance(expected,CollectionDomain):
            raise _issue("REF0401","Collection replacement requires a Collection-bearing place.","החלפת ספר דורשת מקום הנושא Collection.",names[0],place=place.spelling)
        value=_lower_collection(_one_child(node,"CollectionValue"),env,current_act=current_act,recent_act=recent_act)
        actual=hast_value_domain(value)
        if actual!=expected:
            raise _issue("SEM0302","Typed replacement value domain does not equal the place's fixed domain.","תחום ערך ההחלפה בעל הטיפוס אינו שווה לתחום הקבוע של המקום.",node,place=place.spelling,expected=repr(expected),actual=repr(actual))
        return HastReplaceCurrentFact(span,place,value)

    if pid in {"C52.PLACE.REPLACE.SYMBOL","C52.PLACE.REPLACE.INDEX","C56.PLACE.REPLACE.INDEX"}:
        names=_direct_leaves(node,"PlaceName")
        if len(names)!=2 or names[0].text!=names[1].text:
            raise _issue("REF0001","Typed replacement destination and displaced current-value description must name the same place.","יעד ההחלפה בעל הטיפוס ותיאור הערך הנוכחי המוחלף חייבים לנקוב באותו מקום.",names[-1] if names else node)
        place=_resolve_place(names[0].text,env,names[0])
        value_node=_one_child(node,"SymbolValue" if pid.endswith("SYMBOL") else "IndexValue")
        value=_lower_value(value_node,env,current_act=current_act,recent_act=recent_act)
        actual=hast_value_domain(value)
        if env.place_domains.get(place)!=actual:
            raise _issue("SEM0302","Typed replacement value domain does not equal the place's fixed domain.","תחום ערך ההחלפה בעל הטיפוס אינו שווה לתחום הקבוע של המקום.",node,place=place.spelling)
        if pid.endswith("SYMBOL"):
            head=_direct_leaves(node,"SymbolDomainName")[0]
            explicit=SymbolDomain(_resolve_symbol_domain(head.text,env,head))
            if explicit!=env.place_domains.get(place):
                raise _issue("SEM0303","Displaced Symbol-place head names the wrong Symbol domain.","ראש משפחת השמות בתיאור מקום ה־Symbol המוחלף מציין תחום Symbol שגוי.",head,place=place.spelling)
        return HastReplaceCurrentFact(span,place,value)

    if pid in {"A10.ACT.PERFORM", "A11.ACT.PERFORM.WITH.ROLES", "C52.ACT.PERFORM.ROLES"}:
        role_name = "ActionName" if pid == "A10.ACT.PERFORM" else "PerformedActionName"
        act_leaf = _direct_leaves(node, role_name)[0]
        act = _resolve_act(act_leaf.text, env, act_leaf)
        required = {rid.spelling: rid for (owner, _), rid in env.roles.items() if owner == act.serial}
        associations: list[HastRoleAssociation] = []
        seen: set[str] = set()
        role_nodes = _child_nodes(node, "RoleAssociations")
        if pid != "A10.ACT.PERFORM":
            if len(role_nodes) != 1:
                raise RuntimeError("role association wrapper contract")
            for assoc_node in _flatten_role_associations(role_nodes[0]):
                owners = _direct_leaves(assoc_node, "RoleOwnerActionName")
                roles = _direct_leaves(assoc_node, "AssociatedRoleName")
                if len(owners) != 1 or len(roles) != 1:
                    raise RuntimeError("role association direct-shape contract")
                if owners[0].text != act.spelling:
                    raise _issue("REF0111","Role association explicitly names a different owning act.","שיוך התפקיד נוקב במפורש במעשה בעלים שונה.",owners[0],performed=act.spelling,owner=owners[0].text)
                role = _resolve_role(act, roles[0].text, env, roles[0])
                if role.spelling in seen:
                    raise _issue("REF0111","A role is associated more than once in one performance.","תפקיד משויך יותר מפעם אחת בביצוע יחיד.",roles[0],role=role.spelling)
                seen.add(role.spelling)
                if pid == "A11.ACT.PERFORM.WITH.ROLES":
                    value_node=_one_child(assoc_node,"NumberValue")
                else:
                    value_node=_one_child(assoc_node,"AssociationValue")
                value=_lower_value(value_node,env,current_act=current_act,recent_act=recent_act)
                if env.role_domains.get(role)!=hast_value_domain(value):
                    raise _issue("SEM0304","Role association value domain does not equal the role's static domain.","תחום הערך בשיוך תפקיד אינו שווה לתחום הסטטי של התפקיד.",assoc_node,role=role.spelling)
                associations.append(HastRoleAssociation(assoc_node.original or span,role,value))
        if set(seen) != set(required):
            missing = sorted(set(required) - seen)
            extra = sorted(seen - set(required))
            raise _issue("REF0111","Performance role associations must match the described act's required roles exactly.","שיוכי התפקידים בביצוע חייבים להתאים בדיוק לתפקידים הנדרשים של המעשה המתואר.",act_leaf,act=act.spelling,missing=missing,extra=extra)
        return HastPerformAct(span, act, tuple(sorted(associations, key=lambda a: a.role.serial)))

    if pid in {"A12.RESULT.PRODUCE","C52.RESULT.PRODUCE.SYMBOL","C52.RESULT.PRODUCE.INDEX","C53.RESULT.PRODUCE"}:
        if current_act is None:
            raise _issue("REF0114","Result production is licensed only within the current act performance.","הפקת תוצאה מותרת רק בתוך הביצוע הנוכחי של מעשה.",node)
        symbol={"A12.RESULT.PRODUCE":"NumberValue","C52.RESULT.PRODUCE.SYMBOL":"SymbolValue","C52.RESULT.PRODUCE.INDEX":"IndexValue","C53.RESULT.PRODUCE":"CollectionValue"}[pid]
        value=_lower_value(_one_child(node,symbol),env,current_act=current_act,recent_act=recent_act)
        return HastProduceResult(span,value)

    if pid == "A10.CONDITIONAL.PAIRED":
        prop = _lower_proposition(_one_child(node, "Proposition"), env, current_act=current_act, recent_act=recent_act)
        branches = _child_nodes(node, "AtomicAction")
        assert len(branches) == 2
        return HastConditional(
            span, prop,
            _lower_action(branches[0], env, current_act=current_act, recent_act=recent_act),
            _lower_action(branches[1], env, current_act=current_act, recent_act=recent_act),
        )

    if pid == "A10.REPEAT.COUNTED":
        count = _repeat_count(_one_child(node, "RepeatCount"))
        # A recurrence body starts a fresh structural-immediacy boundary.
        # Incoming result provenance belongs to the enclosing sequence, not to
        # iteration 1 (and the runtimes clear it between later iterations).
        action = _lower_action(_one_child(node, "AtomicAction"), env, current_act=current_act, recent_act=None)
        return HastFixedRecurrence(span, count, action)

    if pid in {"C54.REPEAT.ONE", "C54.REPEAT.TWO", "C54.REPEAT.MANY", "C54.REPEAT.DYNAMIC"}:
        if pid == "C54.REPEAT.ONE":
            count: HastNumber = HastExactNatural(span, 1)
        elif pid == "C54.REPEAT.TWO":
            count = HastExactNatural(span, 2)
        elif pid == "C54.REPEAT.MANY":
            leaves = tuple(l for l in _all_leaves(node, "Numeral:a15-feminine-count-3-99999999") if l.numeric_value is not None)
            if len(leaves) != 1:
                raise RuntimeError("C5.4 literal recurrence count contract")
            count = HastExactNatural(span, leaves[0].numeric_value)  # type: ignore[arg-type]
        else:
            count = _lower_count_as_number(
                _one_child(node, "CountAsNumber"), env,
                current_act=current_act, recent_act=recent_act,
            )
        # The count expression observes the incoming provenance exactly at
        # recurrence entry, but the repeated action does not inherit it.
        repeated = _lower_action(
            _one_child(node, "AtomicAction"), env,
            current_act=current_act, recent_act=None,
        )
        return HastRepeatExactly(span, count, repeated)

    if pid == "A10.RECURRENCE.AFTER_UNTIL":
        # The repeated action never inherits provenance from before the
        # recurrence.  Only a Perform completed by this action can create the
        # provenance observed by the post-action proposition.
        action = _lower_action(_one_child(node, "AtomicAction"), env, current_act=current_act, recent_act=None)
        action_recent = action.act if isinstance(action, HastPerformAct) else None
        prop = _lower_proposition(_one_child(node, "Proposition"), env, current_act=current_act, recent_act=action_recent)
        return HastPostActionRecurrence(span, action, prop)

    if node.symbol in {"AtomicAction", "BodyAtomicAction", "ConditionalConsequence", "CountedConsequence", "AfterGatedRecurrence"}:
        return _lower_action(_single_parse_child(node), env, current_act=current_act, recent_act=recent_act)

    raise RuntimeError(f"unsupported admitted action production {pid}")


def _lower_sequence(node: ParseNode, env: _Env, *, current_act: ActId | None, body: bool) -> HastExecutable:
    units = _flatten_sequence(node, body=body)
    actions: list[HastExecutable] = []
    recent: ActId | None = None
    for unit in units:
        action = _lower_action(unit, env, current_act=current_act, recent_act=recent)
        actions.append(action)
        recent = action.act if isinstance(action, HastPerformAct) else None
    if len(actions) == 1:
        return actions[0]
    assert node.original is not None
    return HastThen(node.original, tuple(actions))


def resolve_a13_program(root: ParseNode) -> HastCoreProgram:
    if root.symbol != "CoreProgram":
        raise RuntimeError("A13 resolver requires a CoreProgram parse root")
    if root.original is None:
        raise RuntimeError("CoreProgram lacks source span")
    env = _Env()
    env.program_contract = _program_contract_id(root)
    preparation_hast = []
    pending_bodies: list[dict[str, object]] = []

    def lower_body_with_contract(wrapper: ParseNode, body_node: ParseNode, act: ActId, body_env: _Env) -> HastActBody:
        body = _lower_sequence(_one_child(body_node, "BodySequence"), body_env, current_act=act, body=True)
        domains = _body_output_domains(body)
        if len(domains) > 1:
            raise _issue("SEM0306","One act has result-production sites with different semantic domains.","למעשה אחד יש אתרי הפקת תוצאה בעלי תחומים סמנטיים שונים.",body_node,act=act.spelling,domains=sorted(map(repr,domains)))
        env.output_domains[act] = next(iter(domains)) if domains else None
        return HastActBody(wrapper.original or root.original, act, body)

    prep_nodes: list[ParseNode] = []
    prep_children = _child_nodes(root, "Preparation")
    if prep_children:
        prep_nodes = _flatten_preparation(prep_children[0])

    for wrapper in prep_nodes:
        pid = wrapper.production_id
        unwrap_ids={
            "A13.PREP.ACT.INTRODUCE","A13.PREP.ROLE.DECLARE","A13.PREP.BODY.DEFINE",
            "C52.PREP.SYMBOL.DOMAIN","C52.PREP.SYMBOL.MEMBER","C52.PREP.SYMBOL.ORDER",
        }
        inner = _single_parse_child(wrapper) if pid in unwrap_ids else wrapper

        if pid in {"C55.INPUT.DECLARE.NATURAL","C55.INPUT.DECLARE.SYMBOL","C55.INPUT.DECLARE.INDEX","C55.INPUT.DECLARE.COLLECTION","C56.INPUT.DECLARE.INDEX"}:
            roles=_direct_leaves(wrapper,"ProgramInputRoleName")
            if len(roles)!=2 or roles[0].text!=roles[1].text:
                raise _issue("REF0502","Program Input declaration must explicitly repeat the same role identity.","הצהרת קלט התוכנית חייבת לחזור במפורש על אותו תפקיד.",roles[-1] if roles else wrapper)
            name=roles[0].text
            if name in env.program_inputs:
                raise _issue("REF0502","Duplicate Program Input role declaration.","הצהרה כפולה של תפקיד קלט לתוכנית.",roles[0],role=name)
            if pid.endswith("NATURAL"):
                domain=NATURAL
            elif pid.endswith("INDEX"):
                domain=BIDIRECTIONAL_INDEX
            elif pid.endswith("SYMBOL"):
                dleaf=_direct_leaves(wrapper,"SymbolDomainName")[0]
                domain=SymbolDomain(_resolve_symbol_domain(dleaf.text,env,dleaf))
            else:
                kind=_one_child(wrapper,"CollectionKind")
                domain=CollectionDomain(_collection_kind_element_domain(kind,env))
            input_id=ProgramInputId(env.serial(),name,env.program_contract)
            env.program_inputs[name]=input_id
            env.program_input_domains[input_id]=domain
            continue

        if pid == "C52.PREP.SYMBOL.DOMAIN":
            leaf=_direct_leaves(inner,"SymbolDomainName")[0]
            if leaf.text in env.symbol_domains:
                raise _issue("REF0205","Duplicate Symbol domain name.","שם משפחת שמות כפול.",leaf,domain=leaf.text)
            domain=SymbolDomainId(env.serial(),leaf.text)
            env.symbol_domains[leaf.text]=domain
            preparation_hast.append(HastSymbolDomainDeclaration(wrapper.original or root.original,domain))
            continue

        if pid == "C52.PREP.SYMBOL.MEMBER":
            domains=_direct_leaves(inner,"SymbolDomainName")
            members=_direct_leaves(inner,"SymbolMemberName")
            labels=_direct_leaves(inner,"CountedLabel:a15-direct-1-99999999")
            if len(domains)!=2 or len({x.text for x in domains})!=1 or len(members)!=2 or len({x.text for x in members})!=1 or len(labels)!=1:
                raise _issue("REF0001","Symbol member declaration must explicitly co-refer to one domain/member and one counted label.","הצהרת שם במשפחה חייבת להתייחס במפורש למשפחה אחת, לשם אחד ולתווית מנויה אחת.",inner)
            domain=_resolve_symbol_domain(domains[0].text,env,domains[0])
            key=(domain.serial,members[0].text)
            if key in env.symbol_members:
                raise _issue("REF0206","Duplicate Symbol member source name within one domain.","שם מקור כפול של איבר Symbol בתוך תחום אחד.",members[0],domain=domain.spelling,member=members[0].text)
            member=SymbolMemberId(env.serial(),members[0].text)
            label=labels[0].text
            env.symbol_members[key]=(member,label)
            preparation_hast.append(HastSymbolMemberDeclaration(wrapper.original or root.original,domain,member,label))
            continue

        if pid == "C52.PREP.SYMBOL.ORDER":
            domain_leaf=_direct_leaves(inner,"SymbolDomainName")[0]
            domain=_resolve_symbol_domain(domain_leaf.text,env,domain_leaf)
            vals=_child_nodes(inner,"SymbolValue")
            if len(vals)!=2: raise RuntimeError("Symbol order arity")
            before=_lower_symbol(vals[0],env,current_act=None,recent_act=None)
            after=_lower_symbol(vals[1],env,current_act=None,recent_act=None)
            expected=SymbolDomain(domain)
            if hast_value_domain(before)!=expected or hast_value_domain(after)!=expected:
                raise _issue("SEM0305","Symbol order adjacency operands must belong to the explicitly named domain.","אופרנדי הסמיכות בסדר Symbol חייבים להשתייך לתחום הנקוב במפורש.",inner,domain=domain.spelling)
            assert isinstance(before,HastSymbolValue) and isinstance(after,HastSymbolValue)
            preparation_hast.append(HastSymbolOrderAdjacent(wrapper.original or root.original,domain,before.member_id,after.member_id))
            continue

        if pid=="C53.PREP.PLACE":
            names=_direct_leaves(wrapper,"PlaceName")
            if len(names)!=2 or names[0].text!=names[1].text:
                raise _issue("REF0001","Initialized typed place introduction must repeat the same place name.","הצגת מקום מאותחל בעל טיפוס מפורש חייבת לחזור על אותו שם מקום.",names[-1] if names else wrapper)
            name=names[0].text
            if name in env.places:
                raise _issue("REF0102","Duplicate place name.","שם מקום כפול.",names[0],name=name)
            initial=_lower_collection(_one_child(wrapper,"CollectionValue"),env,current_act=None,recent_act=None,pending_self_place=name)
            domain=_require_collection_domain(initial,wrapper)
            place=PlaceId(env.serial(),name)
            env.places[name]=place
            env.place_domains[place]=domain
            preparation_hast.append(HastPlaceIntroduction(wrapper.original or root.original,place,initial))
            continue

        if pid in {"C52.PREP.PLACE.SYMBOL","C52.PREP.PLACE.INDEX"}:
            names=_direct_leaves(wrapper,"PlaceName")
            if len(names)!=2 or names[0].text!=names[1].text:
                raise _issue("REF0001","Initialized typed place introduction must repeat the same place name.","הצגת מקום מאותחל בעל טיפוס מפורש חייבת לחזור על אותו שם מקום.",names[-1] if names else wrapper)
            name=names[0].text
            if name in env.places:
                raise _issue("REF0102","Duplicate place name.","שם מקום כפול.",names[0],name=name)
            symbol="SymbolValue" if pid.endswith("SYMBOL") else "IndexValue"
            initial=_lower_value(_one_child(wrapper,symbol),env,current_act=None,recent_act=None,pending_self_place=name)
            domain=hast_value_domain(initial)
            place=PlaceId(env.serial(),name); env.places[name]=place; env.place_domains[place]=domain
            preparation_hast.append(HastPlaceIntroduction(wrapper.original or root.original,place,initial))
            continue

        if pid=="C53.ROLE.DECLARE":
            owners=_direct_leaves(wrapper,"RoleOwnerActionName")
            roles=_direct_leaves(wrapper,"DeclaredRoleName")
            if len(owners)!=3 or len({x.text for x in owners})!=1 or len(roles)!=2 or len({x.text for x in roles})!=1:
                raise _issue("REF0001","Typed role declaration repeated descriptions must co-refer explicitly.","התיאורים החוזרים בהצהרת תפקיד חייבים להתייחס במפורש לאותם שמות.",wrapper)
            owner_name,role_name=owners[0].text,roles[0].text
            if owner_name not in env.acts:
                raise _issue("REF0107","Role owner act has not been introduced.","המעשה בעל התפקיד טרם הוצג.",owners[0],owner=owner_name)
            owner=env.acts[owner_name]
            if owner.serial in env.bodies:
                raise _issue("REF0108","Role declaration appears after its owner's body definition.","הצהרת תפקיד מופיעה לאחר הגדרת הגוף של המעשה בעל התפקיד.",roles[0],owner=owner_name,role=role_name)
            key=(owner.serial,role_name)
            if key in env.roles:
                raise _issue("REF0104","Duplicate role name within one act.","שם תפקיד כפול בתוך מעשה אחד.",roles[0],owner=owner_name,role=role_name)
            kind=_one_child(wrapper,"CollectionKind")
            domain=CollectionDomain(_collection_kind_element_domain(kind,env))
            role=RoleId(env.serial(),owner,role_name)
            env.roles[key]=role
            env.role_domains[role]=domain
            preparation_hast.append(HastRoleDeclaration(wrapper.original or root.original,role))
            continue

        if pid in {"C52.ROLE.DECLARE.SYMBOL","C52.ROLE.DECLARE.INDEX","C56.ROLE.DECLARE.INDEX"}:
            owners=_direct_leaves(wrapper,"RoleOwnerActionName"); roles=_direct_leaves(wrapper,"DeclaredRoleName")
            if len(owners)!=3 or len({x.text for x in owners})!=1 or len(roles)!=2 or len({x.text for x in roles})!=1:
                raise _issue("REF0001","Typed role declaration repeated descriptions must co-refer explicitly.","התיאורים החוזרים בהצהרת תפקיד חייבים להתייחס במפורש לאותם שמות.",wrapper)
            owner_name,role_name=owners[0].text,roles[0].text
            if owner_name not in env.acts:
                raise _issue("REF0107","Role owner act has not been introduced.","המעשה בעל התפקיד טרם הוצג.",owners[0],owner=owner_name)
            owner=env.acts[owner_name]
            if owner.serial in env.bodies:
                raise _issue("REF0108","Role declaration appears after its owner's body definition.","הצהרת תפקיד מופיעה לאחר הגדרת הגוף של המעשה בעל התפקיד.",roles[0],owner=owner_name,role=role_name)
            key=(owner.serial,role_name)
            if key in env.roles:
                raise _issue("REF0104","Duplicate role name within one act.","שם תפקיד כפול בתוך מעשה אחד.",roles[0],owner=owner_name,role=role_name)
            domain=BIDIRECTIONAL_INDEX
            if pid.endswith("SYMBOL"):
                dleaf=_direct_leaves(wrapper,"SymbolDomainName")[0]
                domain=SymbolDomain(_resolve_symbol_domain(dleaf.text,env,dleaf))
            role=RoleId(env.serial(),owner,role_name); env.roles[key]=role; env.role_domains[role]=domain
            preparation_hast.append(HastRoleDeclaration(wrapper.original or root.original,role))
            continue

        if pid == "A13.PREP.PLACE.INTRODUCE":
            names = _direct_leaves(wrapper, "PlaceName")
            assert len(names) == 2
            if names[0].text != names[1].text:
                raise _issue(
                    "REF0001", "Initialized place introduction must explicitly repeat the same place name.",
                    "הצגת מקום מאותחל חייבת לחזור במפורש על אותו שם מקום.", names[1],
                    expected=names[0].text, actual=names[1].text,
                )
            name = names[0].text
            if name in env.places:
                raise _issue("REF0102", "Duplicate place name.", "שם מקום כפול.", names[0], name=name)
            value_node = _one_child(wrapper, "NumberValue")
            initial = _lower_number(value_node, env, current_act=None, recent_act=None, pending_self_place=name)
            place = PlaceId(env.serial(), name)
            env.places[name] = place
            env.place_domains[place] = NATURAL
            preparation_hast.append(HastPlaceIntroduction(wrapper.original or root.original, place, initial))
            continue

        if pid == "A13.PREP.ACT.INTRODUCE":
            leaf = _all_leaves(inner, "ActionName")[0]
            name = leaf.text
            if name in env.acts:
                raise _issue("REF0103", "Duplicate act name.", "שם מעשה כפול.", leaf, name=name)
            act = ActId(env.serial(), name)
            env.acts[name] = act
            preparation_hast.append(HastActIntroduction(wrapper.original or root.original, act))
            continue

        if pid == "A13.PREP.ROLE.DECLARE":
            owners = _direct_leaves(inner, "RoleOwnerActionName")
            roles = _direct_leaves(inner, "DeclaredRoleName")
            if not owners or not roles:
                raise RuntimeError("role declaration shape")
            if len({x.text for x in owners}) != 1 or len({x.text for x in roles}) != 1:
                raise _issue(
                    "REF0001", "Role declaration repeated descriptions must co-refer explicitly.",
                    "התיאורים החוזרים בהצהרת תפקיד חייבים להתייחס במפורש לאותם שמות.",
                    owners[-1] if len({x.text for x in owners}) != 1 else roles[-1],
                )
            owner_name, role_name = owners[0].text, roles[0].text
            if owner_name not in env.acts:
                raise _issue("REF0107", "Role owner act has not been introduced.", "המעשה בעל התפקיד טרם הוצג.", owners[0], owner=owner_name)
            owner = env.acts[owner_name]
            if owner.serial in env.bodies:
                raise _issue("REF0108", "Role declaration appears after its owner's body definition.", "הצהרת תפקיד מופיעה לאחר הגדרת גוף המעשה בעליו.", roles[0], owner=owner_name, role=role_name)
            key = (owner.serial, role_name)
            if key in env.roles:
                raise _issue("REF0104", "Duplicate role name within one act.", "שם תפקיד כפול בתוך מעשה אחד.", roles[0], owner=owner_name, role=role_name)
            role = RoleId(env.serial(), owner, role_name)
            env.roles[key] = role
            env.role_domains[role] = NATURAL
            preparation_hast.append(HastRoleDeclaration(wrapper.original or root.original, role))
            continue

        if pid == "A13.PREP.BODY.DEFINE":
            body_node = inner
            names = _direct_leaves(body_node, "BodyActionName")
            assert len(names) == 2
            if names[0].text != names[1].text:
                raise _issue(
                    "REF0021", "Body opener and closer must explicitly name the same act.",
                    "פותח הגוף וסוגר הגוף חייבים לנקוב במפורש באותו מעשה.", names[1],
                    expected=names[0].text, actual=names[1].text,
                )
            name = names[0].text
            if name not in env.acts:
                raise _issue("REF0109", "Body owner act has not been introduced.", "המעשה בעל הגוף טרם הוצג.", names[0], owner=name)
            act = env.acts[name]
            if act.serial in env.bodies:
                raise _issue("REF0105", "Duplicate body definition for one act.", "הגדרת גוף כפולה לאותו מעשה.", names[0], act=name)
            body_env = _body_env_snapshot(env)
            slot = len(preparation_hast)
            try:
                body_hast = lower_body_with_contract(wrapper, body_node, act, body_env)
            except _UnresolvedOutputContract as blocked:
                pending_bodies.append({
                    "slot": slot, "wrapper": wrapper, "body_node": body_node,
                    "act": act, "env": body_env, "blocked": blocked,
                })
                preparation_hast.append(None)
            else:
                preparation_hast.append(body_hast)
            # The body definition has occurred in source even when semantic lowering is deferred.
            # This preserves A13's prohibition on later role declarations for its owner.
            env.bodies.add(act.serial)
            continue

        raise RuntimeError(f"unsupported A13 preparatory production {pid}")

    while pending_bodies:
        progressed = False
        remaining = []
        for pending in pending_bodies:
            try:
                body_hast = lower_body_with_contract(
                    pending["wrapper"], pending["body_node"], pending["act"], pending["env"]
                )
            except _UnresolvedOutputContract as blocked:
                pending["blocked"] = blocked
                remaining.append(pending)
            else:
                preparation_hast[pending["slot"]] = body_hast
                progressed = True
        if not progressed:
            blocked = remaining[0]["blocked"]
            raise _issue(
                "REF0404",
                "Collection immediate-result output contract is cyclic or otherwise unresolved.",
                "חוזה הפלט של תוצאת הספר המיידית מעגלי או שאינו ניתן לפתרון.",
                blocked.where,
                act=blocked.act.spelling,
            )
        pending_bodies = remaining

    missing_bodies = [act for act in env.acts.values() if act.serial not in env.bodies]
    if missing_bodies:
        act = sorted(missing_bodies)[0]
        raise _issue(
            "SEM0203", "Every introduced Core act requires exactly one body before principal execution.",
            "לכל מעשה שהוצג ב־Core נדרש גוף אחד בדיוק לפני הביצוע העיקרי.", root,
            missing=[a.spelling for a in sorted(missing_bodies)],
        )

    principal_node = _one_child(root, "PrincipalExecution")
    seq = _one_child(principal_node, "ExecutableSequence")
    principal = _lower_sequence(seq, env, current_act=None, body=False)

    places = tuple(sorted(env.places.values()))
    acts = tuple(sorted(env.acts.values()))
    roles = tuple(sorted(env.roles.values()))
    body_by_act = {x.act: x.body for x in preparation_hast if isinstance(x, HastActBody)}
    output_contracts=[]
    for act in acts:
        if act not in env.output_domains:
            domains=_body_output_domains(body_by_act[act])
            if len(domains)>1:
                raise _issue("SEM0306","One act has result-production sites with different semantic domains.","למעשה אחד יש אתרי הפקת תוצאה בעלי תחומים סמנטיים שונים.",root,act=act.spelling,domains=sorted(map(repr,domains)))
            env.output_domains[act]=next(iter(domains)) if domains else None
        output_contracts.append(HastActOutputDomain(act,env.output_domains[act]))
    return HastCoreProgram(
        root.original,
        tuple(preparation_hast),
        principal,
        places,
        acts,
        roles,
        tuple(HastPlaceDomain(x, env.place_domains[x]) for x in places),
        tuple(HastRoleDomain(x, env.role_domains[x]) for x in roles),
        tuple(output_contracts),
        tuple(HastProgramInputDomain(x, env.program_input_domains[x]) for x in sorted(env.program_input_domains, key=lambda y: y.serial)),
    )



__all__ = ["A13ResolutionIssue", "A13ResolutionError", "resolve_a13_program"]
