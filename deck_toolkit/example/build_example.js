// build_example.js — minimal demo of the deck toolkit.
// Run AFTER rendering assets:
//   python ../render_assets.py <theme> example_spec.json assets
//   node build_example.js <theme>
// Produces example_<theme>.pptx.

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const { createDeck, listThemes } = require("../deck_lib");

const theme = process.argv[2] || "academic_navy";
const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, "assets", "manifest.json"), "utf8"));

const D = createDeck(pptxgen, {
  theme,
  manifest,
  assetDir: path.join(__dirname, "assets"),
  title: "Deck Toolkit Example",
  footerText: "Deck toolkit example",
});
const C = D.theme, L = D.L;

// 1. Title
D.titleSlide("HOUSE STYLE DEMO", "Deck Toolkit Example",
  `Theme: ${theme}. Same engine, swap one string to restyle the whole deck.`,
  ["palette", "type scale", "typeset equations", "rendered code"]);

// 2. Divider
D.divider("01", "A Section", "Dividers use the primary color full-bleed with the accent numeral.");

// 3. Content: equation strip + bullets (left) + code (right)
const s = D.contentSlide("Equation, bullets & code", "Section 01 · Demo");
D.formula(s, "ex_surv", { x: 0.55, y: 1.4, w: 12.2, lineH: 0.7, where: [
  ["S(t)", "survival function"], ["T", "event time"], ["h(t)", "hazard rate"], ["t", "time"],
] });
D.bullets(s, [
  { t: "Body text uses the theme body color at a legible floor size.", sa: 14 },
  { t: "Emphasis / takeaways use the dark accent and bold.", c: C.accentDark, b: true, sa: 14 },
  { t: "Sub-point with indent", lvl: 1, sa: 8 },
  { t: "Another sub-point", lvl: 1 },
], { x: L.BX, y: 2.95, w: L.BW, h: 3.6 });
D.codePanel(s, "ex_fit", { x: L.CX, y: 2.9, w: L.CW, h: 3.85, title: "Code is a crisp image — no font substitution" });

// 4. Cards row
const s2 = D.contentSlide("Cards & callouts", "Section 01 · Demo");
["Primary", "Accent", "Dark accent"].forEach((lbl, i) => {
  const x = 0.55 + i * 4.09;
  const col = [C.primary, C.accent, C.accentDark][i];
  D.card(s2, x, 1.7, 3.85, 2.6, C.white);
  s2.addShape(D.shapes().RECTANGLE, { x, y: 1.7, w: 3.85, h: 0.16, fill: { color: col }, line: { type: "none" } });
  s2.addText(lbl, { x: x + 0.28, y: 2.0, w: 3.3, h: 0.5, fontFace: C.headFont, fontSize: 21, bold: true, color: C.primary, margin: 0 });
  s2.addText("Reusable card with an accent top-bar.", { x: x + 0.28, y: 2.6, w: 3.3, h: 1.5, fontFace: C.bodyFont, fontSize: 15, color: C.body, margin: 0, lineSpacingMultiple: 1.2 });
});
D.callout(s2, 0.55, 4.6, 12.23, 1.0, "Callout",
  "Callouts fill whitespace with a takeaway in a light panel. Available themes: " + listThemes().join(", ") + ".");

D.pres.writeFile({ fileName: path.join(__dirname, `example_${theme}.pptx`) }).then(f => console.log("WROTE", f));
