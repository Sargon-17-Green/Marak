# D2 Structural Repair Plan

Purpose: define the next source-conformance path without rewriting the Megillah from scratch.

## 1. Preserve the historical original
- megillah/original remains immutable.
- No Markdown-stripping preprocessor is allowed; documentary Hebrew must be explicitly absent from an executable candidate or represented by a future admitted documentation mechanism.

## 2. Separate documentary discourse from computation
- The title/headings, opening address to the scribe/reader, worked examples used only as explanation, correctness/proof paragraphs, and the final owner's epilogue are candidate documentation, not executable units.
- This separation must be span-by-span. A heading does not make the paragraphs beneath it documentation automatically.
- Input/output contract sentences are not discarded merely because they are prose; they are tracked as interface requirements.

## 3. Convert reusable algorithmic descriptions to explicit A13 acts
- First concrete case: דבר החיבור.
- Its historical intent can be expressed by one named act חיבור, two explicitly named numeric roles, and one numeric result.
- A C M4.2 proof program with roles ראשון/שני, A13 addition, and result production compiled and produced 11 for 5+6.
- This is a viable STRUCTURAL_EXPLICITNESS repair pattern, not a Megillah-specific compiler rule.
- The worked sentence חבר חמש ושש... should become a test/example, not executable source.

## 4. Do not mass-convert every לוח to an act
- A table/section is not automatically a function or procedure.
- Each section must be classified by computational need: reusable act, data declaration, one-time principal computation, proof/documentation, or post-M2 unsupported data relation.
- Markdown position is never the classifier.

## 5. Whole-program transition
- The lexical ועתה at historical line 169 is not the program entry and cannot remain a top-level A13 transition in the current organization.
- The likely principal computation is the final query workflow under לוח אחרון, but D will not declare that solely from the heading.
- A unique late top-level ועתה should be introduced only after all required identities/data definitions are legal preparation and the final computation is expressed as an admitted executable unit or sequence.

## 6. Current hard blockers before a truthful full candidate
- Runtime symbolic calendar labels.
- Signed year numbers.
- Ordered finite runtime collections.
- Numeric ordering propositions.
- Productive >9999 numeral spelling or systematic equivalent source repair.
- General N פעמים counted recurrence or a justified recursive rewrite.
- Explicit binding of the two external day inputs.

Until these are dispositioned by Master/A/B, a whole-file candidate would either be knowingly non-Maraks or would hide a wholesale numeric encoding rewrite.

## 7. Next frontier after Master disposition
1. Create megillah/candidates/Megilat_HaItim_Marak_Candidate.md.
2. Apply only semantically confirmed local repairs plus explicitly approved structural repairs.
3. Externalize only spans proven documentary.
4. Compile/check iteratively and record normalized token frontier after each patch.
5. Do not apply D-PATCH-0001 unless Master explicitly approves the algorithm correction.
6. Do not begin algorithmic differential acceptance until parse/resolve/validate frontier is substantially complete.
