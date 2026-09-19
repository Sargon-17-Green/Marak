"""Executable adapter for the historical B4 action calculus.

STATUS: REFERENCE_ONLY_AFTER_B6_ANTI_IMITATION_AUDIT.

This deliberately preserves the old B4 conventional encoding (cells, frames,
strict ordered calls, Return/Unit) as an executable oracle.  B6 explicitly
reopened those ontological choices.  Therefore this module MUST NOT be imported
by canonical source, HAST, validation, IR, optimization, backend, or public API
modules.  Python object/layout behavior is not normative.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Union

REFERENCE_MODEL_STATUS = "REFERENCE_ONLY_AFTER_B6_ANTI_IMITATION_AUDIT"
REFERENCE_MODEL_SOURCE = "B4 candidate calculus, demoted by B6"


class ReferenceCoreError(Exception):
    def __init__(self, code: str, state: "ReferenceState | None" = None):
        super().__init__(code)
        self.code = code
        self.state = state


@dataclass(frozen=True, slots=True)
class RefInteger:
    value: int


@dataclass(frozen=True, slots=True)
class RefBoolean:
    value: bool


@dataclass(frozen=True, slots=True)
class RefUnit:
    pass


REF_UNIT = RefUnit()
RefValue = Union[RefInteger, RefBoolean, RefUnit]


@dataclass(frozen=True, slots=True)
class ReferenceState:
    store: dict[int, RefValue]
    next_loc: int = 0


@dataclass(frozen=True, slots=True)
class ReferenceFrame:
    env: dict[str, int]


@dataclass(frozen=True, slots=True)
class RefNormal:
    state: ReferenceState
    frame: ReferenceFrame


@dataclass(frozen=True, slots=True)
class RefReturned:
    value: RefValue
    state: ReferenceState
    frame: ReferenceFrame


@dataclass(frozen=True, slots=True)
class RefFailed:
    code: str
    state: ReferenceState
    frame: ReferenceFrame


RefCompletion = RefNormal | RefReturned | RefFailed
RefExpr = Callable[["ReferenceRuntime", ReferenceState, ReferenceFrame], tuple[RefValue, ReferenceState]]
RefCmd = Callable[["ReferenceRuntime", ReferenceState, ReferenceFrame], RefCompletion]


@dataclass(frozen=True, slots=True)
class ReferenceActionDef:
    params: tuple[str, ...]
    body: RefCmd
    lexical_globals: tuple[str, ...] = ()


class ReferenceRuntime:
    """B4 reference runtime, intentionally isolated from canonical compiler models."""

    def __init__(self) -> None:
        self.actions: dict[str, ReferenceActionDef] = {}
        self.global_env: dict[str, int] = {}

    def fresh(self, state: ReferenceState, value: RefValue) -> tuple[int, ReferenceState]:
        loc = state.next_loc
        new_store = dict(state.store)
        new_store[loc] = value
        return loc, ReferenceState(new_store, loc + 1)

    def bind_global(self, state: ReferenceState, name: str, value: RefValue) -> ReferenceState:
        loc, state2 = self.fresh(state, value)
        self.global_env[name] = loc
        return state2

    def lookup(self, frame: ReferenceFrame, name: str) -> int:
        if name in frame.env:
            return frame.env[name]
        if name in self.global_env:
            return self.global_env[name]
        raise ReferenceCoreError("UNRESOLVED_SYMBOL_REFERENCE_MODEL")

    def read(self, state: ReferenceState, frame: ReferenceFrame, name: str) -> RefValue:
        return state.store[self.lookup(frame, name)]

    def assign(self, state: ReferenceState, frame: ReferenceFrame, name: str, value: RefValue) -> ReferenceState:
        loc = self.lookup(frame, name)
        new_store = dict(state.store)
        new_store[loc] = value
        return ReferenceState(new_store, state.next_loc)

    def call(
        self,
        state: ReferenceState,
        caller: ReferenceFrame,
        action_id: str,
        arg_exprs: tuple[RefExpr, ...],
    ) -> tuple[RefValue, ReferenceState]:
        if action_id not in self.actions:
            raise ReferenceCoreError("INVALID_ACTION_CALL_REFERENCE_MODEL", state)
        action = self.actions[action_id]
        if len(arg_exprs) != len(action.params):
            raise ReferenceCoreError("INVALID_ARITY_REFERENCE_MODEL", state)

        values: list[RefValue] = []
        current = state
        for expr in arg_exprs:
            try:
                value, current = expr(self, current, caller)
            except ReferenceCoreError as exc:
                # Preserve the successor state when the expression supplied it.
                if exc.state is None:
                    exc.state = current
                raise
            values.append(value)

        callee_env: dict[str, int] = {}
        for param, value in zip(action.params, values):
            loc, current = self.fresh(current, value)
            callee_env[param] = loc

        callee = ReferenceFrame(callee_env)
        out = action.body(self, current, callee)
        if isinstance(out, RefReturned):
            return out.value, out.state
        if isinstance(out, RefNormal):
            return REF_UNIT, out.state
        if isinstance(out, RefFailed):
            raise ReferenceCoreError(out.code, out.state)
        raise AssertionError("unknown reference completion")


def ref_lit(value: RefValue) -> RefExpr:
    return lambda rt, state, frame: (value, state)


def ref_read(name: str) -> RefExpr:
    return lambda rt, state, frame: (rt.read(state, frame, name), state)


def ref_call(action_id: str, args: tuple[RefExpr, ...]) -> RefExpr:
    return lambda rt, state, frame: rt.call(state, frame, action_id, args)


def _integer_binary(a: RefExpr, b: RefExpr, op: Callable[[int, int], int]) -> RefExpr:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame):
        av, state1 = a(rt, state, frame)
        bv, state2 = b(rt, state1, frame)
        if type(av) is not RefInteger or type(bv) is not RefInteger:
            raise ReferenceCoreError("TYPE_DOMAIN_ERROR", state2)
        return RefInteger(op(av.value, bv.value)), state2
    return run


def ref_add(a: RefExpr, b: RefExpr) -> RefExpr:
    return _integer_binary(a, b, lambda x, y: x + y)


def ref_sub(a: RefExpr, b: RefExpr) -> RefExpr:
    return _integer_binary(a, b, lambda x, y: x - y)


def ref_mul(a: RefExpr, b: RefExpr) -> RefExpr:
    return _integer_binary(a, b, lambda x, y: x * y)


def ref_eq(a: RefExpr, b: RefExpr) -> RefExpr:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame):
        av, state1 = a(rt, state, frame)
        bv, state2 = b(rt, state1, frame)
        return RefBoolean(av == bv), state2
    return run


def ref_assign(name: str, expr: RefExpr) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        try:
            value, state1 = expr(rt, state, frame)
            return RefNormal(rt.assign(state1, frame, name, value), frame)
        except ReferenceCoreError as exc:
            return RefFailed(exc.code, exc.state or state, frame)
    return run


def ref_bind_local(name: str, expr: RefExpr) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        try:
            value, state1 = expr(rt, state, frame)
            loc, state2 = rt.fresh(state1, value)
            env = dict(frame.env)
            env[name] = loc
            return RefNormal(state2, ReferenceFrame(env))
        except ReferenceCoreError as exc:
            return RefFailed(exc.code, exc.state or state, frame)
    return run


def ref_return(expr: RefExpr) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        try:
            value, state1 = expr(rt, state, frame)
            return RefReturned(value, state1, frame)
        except ReferenceCoreError as exc:
            return RefFailed(exc.code, exc.state or state, frame)
    return run


def ref_sequence(*cmds: RefCmd) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        current_state, current_frame = state, frame
        for cmd in cmds:
            out = cmd(rt, current_state, current_frame)
            if isinstance(out, RefNormal):
                current_state, current_frame = out.state, out.frame
                continue
            return out
        return RefNormal(current_state, current_frame)
    return run


def ref_if(cond: RefExpr, yes: RefCmd, no: RefCmd) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        try:
            value, state1 = cond(rt, state, frame)
        except ReferenceCoreError as exc:
            return RefFailed(exc.code, exc.state or state, frame)
        if type(value) is not RefBoolean:
            return RefFailed("TYPE_DOMAIN_ERROR", state1, frame)
        return yes(rt, state1, frame) if value.value else no(rt, state1, frame)
    return run


def ref_do(expr: RefExpr) -> RefCmd:
    def run(rt: ReferenceRuntime, state: ReferenceState, frame: ReferenceFrame) -> RefCompletion:
        try:
            _, state1 = expr(rt, state, frame)
            return RefNormal(state1, frame)
        except ReferenceCoreError as exc:
            return RefFailed(exc.code, exc.state or state, frame)
    return run


def ref_fail(code: str) -> RefCmd:
    return lambda rt, state, frame: RefFailed(code, state, frame)


__all__ = [
    "REFERENCE_MODEL_STATUS", "REFERENCE_MODEL_SOURCE", "ReferenceCoreError",
    "RefInteger", "RefBoolean", "RefUnit", "REF_UNIT", "RefValue",
    "ReferenceState", "ReferenceFrame", "RefNormal", "RefReturned", "RefFailed",
    "RefCompletion", "RefExpr", "RefCmd", "ReferenceActionDef", "ReferenceRuntime",
    "ref_lit", "ref_read", "ref_call", "ref_add", "ref_sub", "ref_mul", "ref_eq",
    "ref_assign", "ref_bind_local", "ref_return", "ref_sequence", "ref_if", "ref_do", "ref_fail",
]
