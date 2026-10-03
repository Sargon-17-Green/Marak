# D4 T19 — Luach Fifteen semantic reconstruction

## Authorized original span

- Luach Fifteen: immutable original lines **895–995**.
- Separator: line 997.
- Luach Sixteen begins at line **999** and is outside T19.

## Question / seal matrix

| Question concept | Seal |
|---|---:|
| דרך בין שערי קציצה | 1 |
| תחילת שנת חמשת אלפים ולסופה | 10 |
| השנה שאחריה | 11 |
| השנה שלפניה | 12 |
| מספר הקציצות | 20 |
| חלוקת השנה לקציצות | 21 |
| שמות הקציצות | 22 |
| מספר החודשים | 30 |
| ימי החודשים | 31 |
| שזירת החודשים | 32 |
| שמות החודשים | 33 |

Seal 40 is explicitly unavailable. Seals are ordinary Natural values; no new type or identity family is required.

## Shared query kernel

Let (M=2^{127}-1), and let `keep(x)` be the already-admitted `שמור` operation.

For queried bowl identity (q), seal (s), post-T18 bowl fills (F_1..F_6), and the preserved visible-drop-46 arrangement (A):

1. Find (q)'s position in (A); the successor bowl (q^+) is the next identity in that same circular arrangement.
2. The first answer number is
   [
   a_1 = keep((F_q+s+181)^2 + 179F_{q^+} + s).
   ]
3. Compute the one-time direction probe
   [
   d = keep((a_1+s+1+193)^2 + 193a_1 + 197F_6).
   ]
4. If (d mod 2 = 1), later answer numbers advance by one with (M\to1). If the remainder is zero, they retreat by one with (1\to M).
5. This cyclic step enumerates every number in 1..M exactly once before returning to (a_1). A later Luach may skip unusable answer numbers by repeatedly taking the next number in this already-defined order.

The modulo-2 operation uses the already accepted source-authorized Luach Six short remainder route. It is not a host shortcut.

## State / provenance audit

The source reads:

- post-T18 bowl fills `מלא הקערות`;
- preserved visible-drop-46 arrangement `מערכת הטיפה האחרונה`;
- fixed bowl identity 6 fill for the direction probe;
- `המספר הגדול`.

It does **not** use the arrangement produced by the twelfth post-drop blend to determine the successor bowl, and it does not authorize changing bowl fills or either arrangement as a result of asking.

The production repair therefore preserves those source-state values. Internal pre-existing arithmetic/search workspaces may be used by admitted helper acts, but no bowl/query source state is advanced.

## Classification

`SOURCE_REPAIR_ONLY / CURRENT_LANGUAGE_ALREADY_SUFFICIENT`.

No parser, grammar, registry, HAST, IR, artifact schema, language specification, semantic type, or identity family change is required.
