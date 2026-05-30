# CLAUDE.md — Survival Mini-Course

Guidance for working on the teaching modules in this directory (`01_background/` through `08_recipes/`, plus `references/`). Merges with the parent `../CLAUDE.md` behavioral guidelines.

## Confusion is a defect signal

When the user asks a clarifying question about anything in the modules, treat it as evidence that **the module is not clear enough** — not merely a question to answer in chat.

Every such question gets a two-part response:

1. **Answer** the question directly in the conversation.
2. **Fix the source.** Expand or rewrite the relevant module so a future reader would not hit the same confusion — add the missing definition, example, gloss, or cross-link.

The chat answer is disposable; the module is the artifact that has to improve. If a question was worth asking, the clarification belongs in the file.

## Redirect to the owning module

A question often surfaces in one module but really belongs to another — the concept is *owned* by a different section. When that is the case:

1. **Redirect** — tell the user which module owns the concept.
2. **Edit there** — make the clarifying fix in that owning module, not the one where the question happened to come up.

The module where the question arose can keep a brief cross-link; the full explanation lives where the concept is introduced.

## How to expand

- Put the clarification **where the term is introduced**, not wherever the question happened to surface.
- Keep it gradual and self-contained: define terms before use, gloss jargon on first appearance, cross-link to the section with the full treatment.
- Prefer a short, concrete example over more prose.
- Stay surgical — expand the unclear part, don't rewrite the whole module.

## After expanding

Briefly state what was unclear and which file(s) changed, so the improvement is traceable.
