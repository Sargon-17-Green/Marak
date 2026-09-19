# Marak for LLM / AI coding agents

This directory is for documentation written specifically for language models and AI coding agents.

It is **not normative**. If anything here conflicts with the specification or conformance suite, this guide is wrong.

The guide should favor canonical, edition-specific constructions and explicit negative rules. In particular, an agent must not invent Marak syntax by translating familiar Python/C/JavaScript concepts.

Core anti-hallucination rules include:
- do not infer semantics from punctuation, Markdown, indentation or newlines;
- do not treat `ועתה` as `main`;
- do not treat `הוצא` as terminating `return`;
- do not turn propositions into Boolean values;
- do not bind roles positionally;
- do not assume hoisting or source-order execution;
- if the current edition cannot express an intended meaning unambiguously, report that instead of guessing.

Future machine-oriented files may include canonical-pattern and negative-pattern corpora derived directly from conformance fixtures.
