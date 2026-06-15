# Presentation house style — `deck_toolkit/`

Every slide deck for this project is built with this toolkit so all decks share one
look: palette, fonts, type scale, layout grid, and — critically — **equations and
code are rendered to images** rather than typed as slide text. PowerPoint substitutes
monospace fonts unpredictably and cannot typeset math; rendering to images removes both
problems and guarantees the deck looks identical on any machine.

The canonical reference deck built with this style is
`Survival_Modelling_3D_Imaging_v3.pptx` in the repo root.

## Files

| File | Role |
|---|---|
| `themes.json` | Single source of truth for palettes (read by both JS and Python). |
| `deck_lib.js` | Theming + layout helper library on top of `pptxgenjs`. |
| `render_assets.py` | Renders code snippets + equations to themed PNGs + a `manifest.json`. |
| `example/` | A 4-slide working example (`build_example.js`, `example_spec.json`). |

## Build sequence

```bash
# 1. render the equation + code images for your chosen theme
python deck_toolkit/render_assets.py academic_navy my_spec.json out/assets

# 2. build the deck (deck_lib reads the manifest produced above)
node my_deck.js          # calls createDeck({ theme:"academic_navy", manifest, assetDir:"out/assets" })

# 3. QA: convert to images and inspect (catch overflow/overlap)
python <pptx-skill>/scripts/office/soffice.py --headless --convert-to pdf my_deck.pptx
pdftoppm -jpeg -r 120 my_deck.pdf shots/s
```

> **Assets are theme-specific.** Equation color = the theme `primary`; code colors
> come from the theme. If you change the theme you must re-run `render_assets.py`
> before rebuilding, or the images will carry the old palette.

## Palettes

Pick by passing the key to `createDeck({ theme })` (default `academic_navy`). To use
**M31 brand colors**, copy any block in `themes.json`, rename it, and drop in the brand
hex values (no `#`); everything else inherits automatically.

| key | look |
|---|---|
| `academic_navy` | Navy + teal, restrained conference-talk feel (default) |
| `charcoal_amber` | Neutral charcoal with a warm amber accent |
| `forest_moss` | Calm biology-leaning green |
| `ocean_teal` | Deep blue + bright teal |
| `berry_cream` | Distinctive, editorial |
| `slate_coral` | Modern slate with a friendly coral accent |

Each theme defines: `primary` (dark backgrounds/headings/code bg), `accent`,
`accentDark` (emphasis), `body`, `muted`, `light` (panels), `line`, code colors, and
the three fonts. One color dominates; the accent is used sparingly.

## Type scale (pt) — these are minimum legible sizes

Title slide 58 · divider numeral 110 / title 46 / subtitle 20 · slide title 33 ·
kicker 14 · **body 20** · small/card body 16 · caption 14 · table 17 · code title 14 ·
**code render 15** · **equation render 30**. Nothing on a content slide goes below ~14pt.
Body text is deliberately large (≥ 20pt on primary content) — keep bullets short so they
don't wrap past 2 lines at this size.

## Fonts

Headings **Georgia** (serif, for personality), body **Calibri**, code rendered in a
real monospace (DejaVu Sans Mono, embedded in the image). Set per theme in `themes.json`.

## Layout grid (16:9 wide, 13.333 × 7.5 in)

- 0.55" side margins; content bottom ~6.78" (footer below).
- Two-column slides: text left (`BX/BW`), code right (`CX/CW`); figure+code slides use `FX/FW`.
- Section **dividers** are full-bleed `primary` with a big accent numeral.
- **Fill the slide:** code panels scale up to fill their box; short columns get a
  `callout()` card carrying a one-line takeaway rather than leaving dead space.
- **No** accent underlines beneath titles and **no** full-width colored header bars
  (these read as AI-generated). Use whitespace and the kicker label instead.

## Equations

Author as mathtext strings in the spec (`"$S(t)=\\prod_{t_i\\le t}(1-d_i/n_i)$"`).
Use real math: `\\frac`, `\\sum`, `\\prod`, `\\int`, `\\leq`, subscripts, Greek.
They render as typeset images placed in a light accent-barred strip via `formula()`.
Never type an equation as monospace slide text.

**Every equation must define its symbols.** Pass `formula(slide, key, { where: [["S(t)",
"survival function"], ["d_i", "events at t_i"], ...] })`; the helper renders a `where: …`
legend (bold symbol = plain definition) inside the equation strip. `formula()` warns if
`where` is omitted. Don't assume the audience reads notation — spell out every term.

## Code snippets

Author as `[text, is_comment]` line arrays in the spec. Comments render in the accent
tint and italic; keep lines ≲ 50 chars so they stay large in the right column (the
panel auto-scales, longer lines just shrink). Place with `codePanel()`.

## QA (required before delivering)

Render to images and inspect every slide for overflow, overlap, off-edge elements, and
large dead space — ideally with a fresh-eyes subagent. Fix real defects, then stop.
