# Plan: Survival Mini-Course → Interactive Quarto Site

Goal: turn the existing markdown textbook into a Brilliant.org-style interactive
course **without rewriting the prose**. The markdown stays the source of truth; a
thin Quarto publishing layer adds a navigable website, static figures, and
(later) live in-browser widgets.

Inspired by `github.com/rohitg00/ai-engineering-from-scratch` — a build-along
repo. Our gap vs. that repo: our content explains deeply but nothing runs, has no
figures, and isn't published as a site. This plan closes that gap.

## Decisions (locked 2026-06-15)

| Question | Decision |
|---|---|
| Substrate | **Quarto + JupyterLite** — reuses markdown+LaTeX, Pyodide runs Python in-browser, no reader install |
| First pass | **Static figures across all lessons**; live widgets deferred to Phase 2 |
| Dataset | Built-in tabular **GBSG2 / METABRIC** for runnable model code (modules 02–03). Background figures use **synthetic numpy** data — clearer for teaching, zero deps |
| Theme | `academic_navy` from `deck_toolkit/themes.json` (navy `#1B2A41` + teal `#1C7293`) |

## Repo layout after this work

```
survival_minicourse/
├── _quarto.yml            # site config: sidebar nav, theme, html format
├── index.qmd              # landing page
├── 01_background/ … 06_recipes/   # existing .md, rendered as-is
├── assets/figures/        # committed SVGs (deterministic, script-generated)
├── scripts/
│   ├── make_figures.py    # regenerates every figure (fixed seed)
│   └── data.py            # shared GBSG2 loader (Phase 2 / modules 02–03)
├── _extensions/           # jupyterlite extension (installed Phase 2)
└── requirements.txt       # numpy, matplotlib, lifelines, scikit-survival, pycox
```

Relative cross-links (`../03_metrics/3.3_km_curves.md`) keep working under Quarto.

## Phase 1 — figures + site (this pass)

Vertical slice first: **module 01 only**, end to end, to validate look-and-feel.

1. `scripts/make_figures.py` — deterministic SVGs from synthetic data, house palette.
   - `hazard_vs_cumhazard` — speedometer/odometer + `S(t)=e^{-H(t)}` (1.1)
   - `km_step` — Kaplan-Meier step curve built event-by-event (1.1 / 3.3)
   - `censoring_timeline` — per-subject lollipop, observed ● vs censored ▷ (1.2)
   - `cif_vs_oneminuss` — competing-risks CIF vs the `1−S(t)` overestimate (1.4)
   - Verify: figures open and are legible; re-running reproduces identical output.
2. Scaffold `_quarto.yml` + `index.qmd`, theme = academic_navy. Verify: `quarto render` clean.
3. Embed figures into 1.1–1.4 at the prose anchor points (surgical edits, alt-text + captions).
4. Render + QA the slice (overflow, placement, LaTeX). Fresh-eyes pass.

Then roll the same pattern across modules 02–06 (figures for Cox PH curves,
loss-comparison, C-index pairs, Brier, KM, etc.) on a follow-up pass.

## Phase 2 — live widgets (later)

Install the JupyterLite extension; swap ~5 static figures for live Pyodide cells
where parameter→consequence *is* the lesson:

1. **hazard → survival** — slider on `h(t)`, watch `S(t)=e^{-H}` redraw (1.1)
2. **censoring** — drag the follow-up window; subjects flip observed/censored (1.2)
3. **proportional hazards** — slider on β (parallel curves) + "break PH" toggle (crossing) (2.1)
4. **Cox risk set** — animate the shrinking risk set / softmax as events fire (2.1)
5. **C-index** — drag points; concordant/discordant pairs light up (3.1)

Known constraint: **scikit-survival and pycox likely lack Pyodide wheels** (pycox
pulls in PyTorch). In-browser widgets must lean on `lifelines` + hand-written
numpy. Static figures are unaffected (rendered at build time).

## Conventions

- Figures are **script-generated and deterministic** (fixed RNG seed) — never
  hand-tweaked one-offs. A prose edit regenerates a consistent figure.
- SVG (scales crisply; Quarto/HTML native). PNG fallback only if a backend needs it.
- One shared palette/style helper in `make_figures.py` so every figure matches.
- Quarto degrades gracefully: if a widget fails to load, the static figure remains.
