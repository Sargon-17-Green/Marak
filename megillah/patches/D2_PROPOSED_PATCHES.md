# D2 Proposed Source Patches

This file records D2 patch decisions. The historical original is immutable.

## D-PATCH-0001
- Span(s): line 1267
- Original: `אחד ושמונים ושבע מאות וחמשת אלפים`
- Replacement: `חמשת אלפים ושבע מאות ושבעים ושמנה`
- Class: SOURCE_PROGRAMMING_BUG
- Preservation: ALGORITHM_CHANGE
- Approval: MASTER_APPROVED
- Reason: isolated 5781 contradicts derived/repeated 5778 bound

## D-PATCH-0002
- Span(s): line 23, line 147
- Original: `יהי שם מעשה NAME`
- Replacement: `יהי מעשה ושמו NAME`
- Class: SOURCE_AMBIGUITY
- Preservation: DISAMBIGUATION_ONLY
- Approval: SEMANTICALLY_CONFIRMED
- Reason: A13 freezes an unambiguous named-act introduction

## D-PATCH-0003
- Span(s): line 237
- Original: `וכן עשה עד אשר`
- Replacement: `וכן תעשה עד אשר`
- Class: SOURCE_AMBIGUITY
- Preservation: DISAMBIGUATION_ONLY
- Approval: SEMANTICALLY_CONFIRMED
- Reason: A13 negative grammar rejects וכן עשה and freezes וכן תעשה

## D-PATCH-0004
- Span(s): line 173, line 341
- Original: `ואחר כן`
- Replacement: `ואחרי כן`
- Class: SOURCE_NOT_LANGUAGE
- Preservation: SEMANTIC_EQUIVALENT
- Approval: SEMANTICALLY_CONFIRMED
- Reason: A13 freezes only the explicit sequence relation ואחרי כן
