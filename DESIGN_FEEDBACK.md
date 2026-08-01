# Design.pdf — review and revision brief

Review of the 4-page `Design.pdf` handout against the course it summarises
(`survival_minicourse/`, 20 lessons across 5 modules, ~20,700 words).

**Constraint: stays at 4 pages.** Every addition below is paid for by a specific
cut. Nothing here asks for a fifth page.

---

## 1. What is working — do not redesign these

The visual system is strong and should survive the revision intact:

- **Palette and surface.** Dark forest ground with cream/emerald/oxblood accents.
  Legible, distinctive, consistent across all four pages.
- **Type pairing.** EB Garamond display against a monospace label face. The
  monospace eyebrow labels (`h(t) · HAZARD`, `COX PARTIAL LIKELIHOOD`) read as
  instrument panels and suit the subject.
- **Numbered module rubric.** The oxblood/emerald `01`–`05` numerals on page 2,
  echoed as section markers on pages 3 and 4, are doing real navigational work.
- **The page-4 head-swap diagram.** `SCAN → BACKBONE → z → three heads → three
  losses` is the single best object in the document. It makes the course's central
  claim ("survival is a head") in one glance. Keep it, and give it more room.
- **The silent-failure callout.** Correct, well-placed, appropriately alarming.

---

## 2. Blocking errors — fix before anything else

### 2.1 The footer claim is false

Page 4 footer: `RUNNABLE CODE TARGETS GBSG2`

There is no GBSG2 anywhere in the course. `grep -ri gbsg` over all 20 lessons
returns nothing. The only concrete dataset load in the whole course is
`datasets.load_dataset("SUPPORT")` in lesson 4.5. Lesson 5.2 uses placeholder
paths (`mydataset`) throughout.

The claim was inherited from `index.qmd` line 57, which is *also* wrong — the
string appears in `scripts/make_figures.py` only as a future-tense aspiration
("Real fitted-model figures (modules 02-03) **will** load GBSG2 instead"). Every
figure in the course is currently synthetic.

**Fix:** delete the claim, or replace with something true. `FIGURES GENERATED
DETERMINISTICALLY` on the same line *is* accurate (fixed RNG seed) — keep it.
Suggested replacement for the second line: `SYNTHETIC FIGURES · RUNNABLE PACKAGE
EXAMPLES`. Flag to the course owner that `index.qmd:57` needs the same fix.

### 2.2 The loss map's axis labels are clipped

In the page-3 scatter, the rotated y-axis label renders as **`FUL`** at the top
and **`K SCORE`** at the bottom. These are truncations of "full distribution" and
"risk score" — the label is being cut by the plot bounding box.

This is the most damaging bug in the document, because the y-axis is the more
useful of the two dimensions (what the model *outputs*: a ranking vs. an absolute
probability) and the reader cannot see what it means. The course's own version of
this figure (`assets/figures/2.5_method_map.svg`) labels it fully and legibly:
`output: ranking → absolute probability`, ticked `risk score` and `full S(t) + CIF`.

**Fix:** restore the full axis labels. Reserve left gutter width for them rather
than letting the panel clip.

### 2.3 The loss map's x-axis contradicts the paragraph above it

The PDF labels the x-axis `MORE STRUCTURE IMPOSED ON TIME → LESS` and places
**COX PH at the far-left "more structure" pole**.

The paragraph directly above says Cox "leaves the baseline hazard **unspecified**"
and that "more structure buys smoother **extrapolation**." Both statements make
Cox's placement wrong: Cox imposes the *least* structure on time, and it cannot
extrapolate past follow-up. The decision strip three inches below confirms this,
routing `Need to extrapolate past follow-up? → PARAMETRIC NLL`, not Cox.

The course figure avoids this by labelling the axis in two parts:
`rigid (PH / fixed shape)` → `flexible (no PH, no shape)`. That naming keeps Cox
correctly at the rigid end, because Cox is rigid in the *proportional-hazards*
sense while parametric models are rigid in the *fixed-shape* sense. Compressing
both into the single word "structure" is what broke it.

**Fix:** adopt the course's axis wording verbatim —
`rigid (PH / fixed shape)` on the left, `flexible (no PH, no shape)` on the right.
The point positions then need no change.

### 2.4 The Brier card contradicts the Brier lesson

Page 3, `BRIER SCORE` card: "Overall probabilistic error, **plus calibration**."

Lesson 3.2's first key takeaway is: "**It is not a calibration metric by itself.**
Report it alongside the C-index and a calibration curve or calibration
slope/intercept at clinically relevant horizons."

**Fix:** "Overall probabilistic error. Not a calibration metric on its own."
This is also a better card, because it states a trap rather than a category.

### 2.5 DEEPHIT label overflows the panel

On page 3, "competing risks, native" extends past the right edge of the plot grid.
Either shorten to "competing risks" or move the label to the left of its dot.

---

## 3. The representation problem: space does not track substance

Comparing the area each module occupies in the PDF against its weight in the
course. Course words are exact (`wc -w` per module directory); PDF area shares are
estimated by measuring vertical bands on the pages rendered at 110 dpi, excluding
chrome (headers, course map, stats bar, footers), so treat them as ±3pp:

| Module | Course words | Share of course | Share of PDF area | Delta |
|---|---|---|---|---|
| 01 Background | 3,451 | 17% | 27% | **+10pp** |
| 02 Loss Functions | 6,056 | 29% | 27% | −2pp |
| 03 Metrics | 4,509 | 22% | **11%** | **−11pp** |
| 04 Packages | 1,483 | **7%** | 16% | **+9pp** |
| 05 Medical Imaging | 5,195 | 25% | 18% | **−7pp** |

Three findings:

**Packages is the most over-represented section.** At 1,483 words it is by far the
smallest module — a routing table, not a body of teaching — yet it gets a
half-page five-row table with full-sentence prose in every cell. It is a lookup
you consult once.

**Metrics is the most under-represented.** 22% of the course compressed into four
small cards at the bottom of page 3. The course treats metrics as a first-class
module with four full lessons including IPCW weighting, time-dependent AUC, and
threshold discipline; the handout treats it as a glossary.

**Medical imaging is under-represented and it is the promised payoff.** The
abstract on page 1 explicitly sells the course as "ending in a full walkthrough of
finetuning a self-supervised 3D backbone on MRI with a survival head attached."
Lesson 5.2 is 3,690 words — the largest single lesson in the course — and is an
8-step operational walkthrough (stage into nnU-Net raw layout → build
`survival_labels.json` → preprocess to `.b2nd` → configure → smoke test → train →
swap the loss → read results). The handout shows the head-swap diagram and one
warning. A reader finishes page 4 knowing survival is a head, but with no idea
that a runnable pipeline exists.

---

## 4. Where the space comes from

Roughly **0.45 of a page** is recoverable without deleting any content:

| Source | Recovered | How |
|---|---|---|
| Page 1 gap (caption → stats bar) | ~120px | Largest dead zone in the document; pull the stats bar up |
| Page 3 gap (decision strip → `03 METRICS`) | ~85px | Tighten to match the page-2 section rhythm |
| Page 4 gap (packages table → `05`) | ~85px | Same |
| Page 2 gap (course map → `01 BACKGROUND`) | ~50px | Same |
| Loss map interior | ~150px | The 4×3 grid holds 5 points and is ~55% empty; reduce plot height, keep point positions |
| Packages table prose | ~120px | See below |

**On the packages table:** the "how much of the loop you own" spine is the right
idea, but each cell is a full sentence where a phrase would do. Compress to a
two-column layout — package name, then a ≤8-word capability phrase — and let the
`ALL OF IT` gradient bar carry the ordering it already carries:

```
lifelines        KM, Nelson-Aalen, classical Cox and AFT
scikit-survival  sklearn-shaped estimators, forests, reference IPCW metrics
auton-survival   deep mixtures and competing risks behind a fit() interface
pycox            the deep-loss library, with a training harness
torchsurv        losses and metrics as plain PyTorch — the 3D-imaging fit
```

That is the same information at roughly 60% of the height.

---

## 5. Where the space goes

### 5.1 Give module 05 the walkthrough it promises (≈0.3 page, page 4)

The head-swap diagram answers "what changes." Nothing answers "what do I actually
run." Add a horizontal 8-step spine beneath it, in the same monospace idiom as the
existing eyebrow labels:

```
NIfTI + clinical.csv → nnU-Net raw layout → survival_labels.json
  → preprocess .b2nd → configure → smoke test → train → C-index / IBS
```

Mark the leakage boundary on this spine — lesson 5.2 flags the preprocessing step
as sitting *inside* it, and that is a visual point a linear diagram makes for free.
This single addition converts the handout's biggest claim from an assertion into
something the reader can see the shape of.

### 5.2 Give metrics room to state the trap in each metric (≈0.15 page, page 3)

Keep the four cards, but let each one carry the *failure* rather than the
definition. Definitions are what the site is for; traps are what a handout is for.

| Card | Current | Better |
|---|---|---|
| C-index | "Does it order patients correctly? Discrimination only" | Keep — add "ignores calibration entirely" |
| Brier score | "…plus calibration" **(wrong)** | "Not a calibration metric on its own" |
| Kaplan-Meier | "The descriptive baseline and the risk-stratification plot" | "Separation is not validation — freeze the cutpoint before the test set" |
| Time-dependent AUC | "Discrimination resolved across the follow-up horizon" | Keep — add "only inside the follow-up window" |

These correspond to the actual key takeaways in lessons 3.1–3.4 and give the
metrics block a reason to exist beyond naming four things.

### 5.3 Trim module 01's double coverage (frees the page-1 space)

Module 01 currently gets two separate figure treatments: the `h(t) / H(t) / S(t)`
triptych on page 1, and the follow-up/KM pair on page 2. It is the second-smallest
module. Both figures are good, but two is one too many for 17% of the course.

Recommendation: **keep the page-2 censoring pair** (censoring is the concept that
makes this an unfamiliar subject, and the "curve steps down at events, not at
censorings" caption is the most instructive line on that page) and **shrink the
page-1 triptych** to a third of its current height as a decorative band under the
abstract. The speedometer/odometer analogy survives in the caption.

---

## 6. Smaller craft notes

- **Page 1 headline scale.** "Survival Analysis" at roughly 72pt against a 1-inch
  margin is larger than the page needs. Dropping to ~56pt recovers vertical space
  and reads less like a poster, more like a technical abstract — which is what the
  running header (`abstract · 01 / 04`) says it is.
- **The three page-1 charts have no axis values.** That is defensible for a
  conceptual triptych, but the y-axes carry no ticks *and* no labels, so they read
  as decoration. One tick (`1.0` on the S(t) panel) would anchor them.
- **`READ THE COURSE` appears on page 1 and `READ THE FULL COURSE` on page 4.**
  Pick one wording. The page-4 treatment (large, underlined) is the stronger of
  the two; page 1 can be smaller since the reader has not yet been sold.
- **Section-header rhythm is inconsistent.** Page 2's `01 BACKGROUND — THE
  CENSORED LABEL` sits ~50px below the block above it; page 3's `03 METRICS` sits
  ~85px below. Normalise to one value.
- **The decision strip on page 3 is excellent** and is the most immediately useful
  object in the document. Consider whether it deserves to be larger than the
  scatter above it, rather than smaller — a reader will use the strip and merely
  admire the map.

---

## 7. Suggested revised page plan

| Page | Now | Proposed |
|---|---|---|
| 1 | Title, abstract, large triptych, dead zone, stats, links | Title (smaller), abstract, **slim** triptych band, stats, links — tightened, no dead zone |
| 2 | Course map, module 01 censoring | Unchanged — this page is working |
| 3 | Loss map (buggy), decision strip, 4 metric cards | Loss map **fixed** and shorter, decision strip **larger**, metric cards carrying traps |
| 4 | Packages table (verbose), head swap, silent failure | Packages **condensed**, head swap, **+ 8-step pipeline spine**, silent failure, corrected footer |

Net effect: the same four pages, with the two sections that carry the course's
actual argument — how you evaluate, and how you ship it on a scan — given the room
their weight in the course justifies.

---
---

# Round 2 — review of the revised `.dc.html`

Reviewed against the Claude Design version of *Survival Mini-Course Abstract*
(project `08831b26-96f3-436c-9052-b50bdb3194be`).

## 0. What round 1 fixed — confirmed

All five blocking errors are resolved, and several fixes went beyond the brief:

- Loss-map x-axis now reads `RIGID · PH / FIXED SHAPE` → `FLEXIBLE · NO PH, NO SHAPE`,
  matching the course figure. Cox's position is now correct.
- Loss-map y-axis restored to `RISK SCORE` / `FULL S(t) + CIF` — no longer clipped.
- DeepHit label switched to `text-anchor="end"`; no overflow.
- Brier card now reads "Not a calibration metric on its own." C-index, KM and
  time-dependent AUC cards all carry their traps.
- Packages table condensed to short phrases.
- Headline dropped to 58px; dead zones replaced with `flex:1` spacers, which is a
  better fix than the fixed-margin tightening I suggested.
- Em-dashes converted to colons throughout, matching the course's own style pass.

Do not revisit any of the above.

---

## 1. BLOCKING: page 4 is truncated mid-element

The stored file ends inside an SVG attribute:

```html
<rect x="183.5" y="12.5" width="150" height="30" fill="none" stroke="rgba(254,229,202,
</x-dc>
</body>
</html>
```

The new 8-step pipeline figure is cut off at **step 2 of 8**. Everything after it
is gone from the file:

- steps 3–8 of the pipeline, and the leakage boundary that was supposed to be
  marked on it
- the closing `</g></svg></figure>`
- **the `THE SILENT FAILURE` callout** (present in the original PDF, now absent)
- **the page-4 footer** — which means the false `RUNNABLE CODE TARGETS GBSG2`
  line cannot be confirmed as fixed, because it no longer exists either

Net effect: the document is now ~3.5 pages, and the missing half-page is precisely
the section round 1 identified as the under-represented payoff. Regenerate page 4
completely before any other work.

---

## 2. The three opening curves are mathematically inconsistent

This is why they look wrong. It is not a stylistic problem.

The caption claims `ONE OBJECT, THREE VIEWS` — h(t), H(t) and S(t) are supposed to
be three renderings of the same hazard. They must satisfy H(t) = ∫h and S(t) = e^−H.
The three paths are hand-drawn cubic béziers that satisfy neither. Sampling them
and differentiating numerically:

```
corr( H'(t),  h(t) )        = -0.469     must be +1.00
corr( -S'(t), h(t) )        = -0.837     must be strongly positive
```

Both are **negative**. Concretely, reading the drawn panels:

| t | h(t) says | S(t) actually does |
|---|---|---|
| 0.0 | hazard at maximum (0.86) | barely falling (S' = −0.39) |
| 0.4 | hazard at minimum (0.12) | falling fastest (S' = −1.07) |

**The survival curve drops fastest exactly where the hazard is lowest.** A reader
with any feel for the subject registers the contradiction without being able to
name it, which is what "weird" means here. On the opening page of a document whose
first teaching claim is that these three are the same object, it undercuts the
premise.

### Fix: use the course's own math

`scripts/make_figures.py::fig_hazard_vs_cumhazard` defines the intended shape and
derives the other two from it, so they are consistent by construction:

```python
h = 0.18*exp(-t/2.5) + 0.012 + 0.0016*t    # early spike, recovery, slow late rise
H = cumulative_integral(h)
S = exp(-H)
```

Path data generated from exactly that, in a `0 0 192 56` box (drop-in for the
existing three panels, scale as needed). Verified `corr(H', h) = +1.0000`:

**h(t) — hazard**
```
M0.0,2.0 L0.5,3.4 L8.2,21.0 L15.9,32.9 L23.6,40.8 L31.3,46.0 L39.0,49.4 L46.7,51.6
L54.4,52.9 L62.1,53.6 L69.8,53.9 L77.5,54.0 L85.2,53.9 L92.9,53.7 L100.6,53.3
L108.3,53.0 L116.0,52.5 L123.7,52.1 L131.4,51.6 L139.1,51.2 L146.8,50.7 L154.5,50.2
L162.2,49.7 L169.9,49.2 L177.6,48.7 L185.3,48.2
```

**H(t) — cumulative hazard**
```
M0.0,54.0 L0.5,53.5 L8.2,46.9 L15.9,42.1 L23.6,38.6 L31.3,36.0 L39.0,33.9 L46.7,32.2
L54.4,30.6 L62.1,29.2 L69.8,27.9 L77.5,26.6 L85.2,25.3 L92.9,23.9 L100.6,22.6
L108.3,21.2 L116.0,19.7 L123.7,18.2 L131.4,16.6 L139.1,15.0 L146.8,13.3 L154.5,11.5
L162.2,9.7 L169.9,7.8 L177.6,5.8 L185.3,3.8
```

**S(t) — survival**
```
M0.0,2.0 L0.5,2.6 L8.2,9.9 L15.9,14.4 L23.6,17.5 L31.3,19.7 L39.0,21.3 L46.7,22.6
L54.4,23.7 L62.1,24.6 L69.8,25.5 L77.5,26.4 L85.2,27.2 L92.9,28.0 L100.6,28.8
L108.3,29.6 L116.0,30.4 L123.7,31.2 L131.4,32.0 L139.1,32.9 L146.8,33.7 L154.5,34.5
L162.2,35.3 L169.9,36.1 L177.6,36.9 L185.3,37.6
```

Two supporting changes so the panels read as one object rather than three:

- **Mark the shared inflection.** h(t) bottoms out at t = 9.5 of 24 (40% across).
  A faint vertical rule at 40% in all three panels shows that this is where H stops
  steepening and where S's decline is slowest. That single alignment is what makes
  "one object, three views" legible.
- **Anchor the scales.** H and S start at a known value; ticking `0` on H's origin
  and `1.0` on S's origin costs almost nothing and stops the panels reading as
  decoration.

---

## 3. Module 05 should have page 4 to itself

Agreed that this is the reason the course exists, and the current allocation still
understates it. Two supporting facts:

- Module 05 is **5,195 words**, the second-largest module. Lesson 5.2 alone (3,690
  words) is the largest single lesson in the course.
- Page 2's course map labels it `2 LESSONS`, the smallest count on the page. That
  number is technically true and rhetorically backwards: it makes the payoff look
  like an afterthought. Change that cell to `2 LESSONS · 8-STEP BUILD` so the row
  carries weight rather than just count.

### Move packages off page 4

The condensed packages table is now five short rows, and it is doing the same job
as the loss decision strip on page 3: routing a reader to a choice. Merge them into
one routing band on page 3 — *which loss, then which library* — and page 4 is free.

### What page 4 should hold

Ordered by what a reader takes away, with rough budget:

1. **Head swap** (~20%). Keep as-is, slightly smaller. It answers "what changes."
2. **The 8-step pipeline** (~25%). Finish it, and mark the leakage boundary as a
   bracket spanning the preprocessing step — lesson 5.2 flags that step as sitting
   *inside* the boundary, and a linear diagram makes that point for free.
   ```
   NIfTI + clinical.csv → nnU-Net raw layout → survival_labels.json
     → preprocess .b2nd → configure → smoke test → train → C-index / IBS
                          └──── inside the leakage boundary ────┘
   ```
3. **All seven failure modes** (~30%). Currently the document shows **one of the
   seven** in lesson 5.1's table. That table is the most reusable artifact in the
   module — the kind of thing a reader pins above a desk — and it compresses well
   to a numbered two-column grid (`#` + mode, symptom). Keep the per-slice split
   visually emphasised as the worst offender, but show the whole set.
4. **Footer / CTA** (~10%). Restore, with the corrected data line.

### One thing the handout still never shows

Nothing in four pages shows a **result**. Lesson 5.2 §8 is about reading the output,
and the course's whole argument is that survival metrics replace accuracy. If space
remains after the above, a single small object — a C-index / IBS readout, or the
two-arm risk-group KM the walkthrough ends on — would close the loop from "swap the
head" to "here is what you get." This is the lowest-priority item on the page;
drop it before compressing anything above.

---

## 4. Smaller notes on the revision

- **`{{ courseUrl }}` and `{{ repoUrl }}` are unresolved template variables** in the
  page-1 link block. Confirm they interpolate at export; the original PDF had the
  literal URLs. The visible link text is hardcoded and correct, so this only affects
  whether the anchors actually resolve.
- **Page 1 and page 4 CTAs still differ** (`READ THE COURSE` vs `READ THE FULL
  COURSE`). Unchanged from round 1; pick one.
- **Loss-map grid is still ~55% empty** — 4×3 cells for 5 points. Now that the axis
  labels are correct, the panel can lose ~25% of its height without crowding, which
  helps fund the page-3 routing band.
