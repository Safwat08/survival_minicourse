// deck_lib.js — house-style slide toolkit for survival_minicourse
// Reusable theming + layout helpers on top of pptxgenjs. Pair with render_assets.py
// (equations & code are pre-rendered to images so fonts never get substituted).
//
// Usage:
//   const pptxgen = require("pptxgenjs");
//   const { createDeck } = require("./deck_lib");
//   const manifest = require("./assets/manifest.json");
//   const D = createDeck(pptxgen, { theme: "academic_navy", manifest, assetDir: __dirname + "/assets" });
//   D.titleSlide("MINI-COURSE", "My Title", "Subtitle", ["tag a", "tag b"]);
//   const s = D.contentSlide("A slide", "Section 01");
//   D.formula(s, "eq_key", { x: 0.55, y: 1.5, w: 6.2 });
//   D.bullets(s, [{ t: "point" }], { x: 0.55, y: 2.6, w: 5.9 });
//   D.codePanel(s, "code_key", { x: D.L.CX, y: 1.6, h: 4, title: "lifelines" });
//   D.pres.writeFile({ fileName: "deck.pptx" });

const fs = require("fs");
const path = require("path");

// ---- Type scale (pt). These are FLOORS chosen for legibility on a projector. ----
const SCALE = {
  titleSlideTitle: 58, titleSlideKicker: 17, titleSlideSub: 20, titleSlideTags: 14,
  dividerNum: 110, dividerTitle: 46, dividerSub: 19,
  slideTitle: 33, kicker: 14,
  body: 20, bodySmall: 16, caption: 14, footer: 11,
  cardTitle: 21, cardBody: 15, codeTitle: 14, tableText: 16,
};

// ---- Layout grid (inches, 16:9 wide = 13.333 x 7.5). ----
const LAYOUT = {
  W: 13.333, H: 7.5, marginX: 0.55,
  BX: 0.55, BW: 5.75,     // left text column (two-column slides)
  CX: 6.45, CW: 6.65,     // right code column (ends ~13.1)
  FX: 6.95, FW: 6.1,      // right figure column (figure + code slides)
  bottom: 6.78,           // target content bottom (footer sits below)
};

function loadTheme(name) {
  const themes = JSON.parse(fs.readFileSync(path.join(__dirname, "themes.json"), "utf8"));
  const t = themes[name];
  if (!t) {
    const avail = Object.keys(themes).filter(k => !k.startsWith("_"));
    throw new Error(`Unknown theme "${name}". Available: ${avail.join(", ")}`);
  }
  return t;
}
function listThemes() {
  const themes = JSON.parse(fs.readFileSync(path.join(__dirname, "themes.json"), "utf8"));
  return Object.keys(themes).filter(k => !k.startsWith("_"));
}

function createDeck(pptxgen, opts) {
  opts = opts || {};
  const C = typeof opts.theme === "string" ? loadTheme(opts.theme)
          : (opts.theme || loadTheme("academic_navy"));
  const manifest = opts.manifest || {};
  const assetDir = opts.assetDir || "assets";
  const L = LAYOUT;

  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  if (opts.title) pres.title = opts.title;
  if (opts.author) pres.author = opts.author;

  const HEAD = C.headFont, BODY = C.bodyFont, MONO = C.monoFont;
  let pageNo = 0;
  const asset = k => path.join(assetDir, `${k}.png`);
  const mShadow = () => ({ type: "outer", color: "000000", blur: 5, offset: 2, angle: 135, opacity: 0.18 });

  function footer(slide, n) {
    if (opts.footerText)
      slide.addText(opts.footerText, { x: 0.5, y: L.H - 0.38, w: 8, h: 0.3, fontFace: BODY, fontSize: SCALE.footer, color: C.muted, align: "left", margin: 0 });
    slide.addText(String(n), { x: L.W - 1.0, y: L.H - 0.38, w: 0.5, h: 0.3, fontFace: BODY, fontSize: SCALE.footer, color: C.muted, align: "right", margin: 0 });
  }

  function titleSlide(kicker, title, sub, tags) {
    pageNo++;
    const s = pres.addSlide();
    s.background = { color: C.primary };
    if (kicker) s.addText(kicker.toUpperCase(), { x: 0.9, y: 1.35, w: 9, h: 0.4, fontFace: BODY, fontSize: SCALE.titleSlideKicker, bold: true, color: C.accent, charSpacing: 4, margin: 0 });
    s.addText(title, { x: 0.85, y: 1.85, w: 11.8, h: 2.5, fontFace: HEAD, fontSize: SCALE.titleSlideTitle, bold: true, color: C.white, margin: 0, lineSpacingMultiple: 1.0 });
    if (sub) s.addText(sub, { x: 0.9, y: 4.65, w: 11.2, h: 1.3, fontFace: BODY, fontSize: SCALE.titleSlideSub, color: "B6C7DA", margin: 0, lineSpacingMultiple: 1.2 });
    if (tags && tags.length) s.addText(tags.join("  ·  "), { x: 0.9, y: 6.5, w: 11.8, h: 0.4, fontFace: BODY, fontSize: SCALE.titleSlideTags, italic: true, color: "8DA1B8", margin: 0 });
    return s;
  }

  function contentSlide(title, kicker) {
    pageNo++;
    const s = pres.addSlide();
    s.background = { color: C.white };
    if (kicker) s.addText(kicker.toUpperCase(), { x: 0.55, y: 0.34, w: 11, h: 0.3, fontFace: BODY, fontSize: SCALE.kicker, bold: true, color: C.accent, charSpacing: 2, margin: 0 });
    s.addText(title, { x: 0.55, y: kicker ? 0.68 : 0.5, w: 12.2, h: 0.85, fontFace: HEAD, fontSize: SCALE.slideTitle, bold: true, color: C.primary, margin: 0 });
    footer(s, pageNo);
    return s;
  }

  function divider(num, title, sub) {
    pageNo++;
    const s = pres.addSlide();
    s.background = { color: C.primary };
    s.addText(num, { x: 0.9, y: 2.05, w: 3, h: 1.7, fontFace: HEAD, fontSize: SCALE.dividerNum, bold: true, color: C.accent, margin: 0 });
    s.addText(title, { x: 3.2, y: 2.35, w: 9.2, h: 1.3, fontFace: HEAD, fontSize: SCALE.dividerTitle, bold: true, color: C.white, margin: 0, valign: "middle" });
    if (sub) s.addText(sub, { x: 3.25, y: 3.75, w: 9.2, h: 2.0, fontFace: BODY, fontSize: SCALE.dividerSub, color: "B6C7DA", margin: 0, lineSpacingMultiple: 1.22 });
    s.addText(String(pageNo), { x: L.W - 1.0, y: L.H - 0.38, w: 0.5, h: 0.3, fontFace: BODY, fontSize: SCALE.footer, color: "5B7088", align: "right", margin: 0 });
    return s;
  }

  // code panel = pre-rendered image scaled to fill its box (never font-substituted)
  function codePanel(slide, key, o) {
    o = Object.assign({ x: L.CX, y: 4.0, w: L.CW, h: 3.0, title: null, cap: 1.5 }, o || {});
    const m = manifest[key];
    if (!m) throw new Error(`No rendered asset for code key "${key}". Add it to the spec and re-run render_assets.py.`);
    let yTop = o.y;
    if (o.title) { slide.addText(o.title, { x: o.x, y: o.y, w: o.w, h: 0.34, fontFace: BODY, fontSize: SCALE.codeTitle, bold: true, color: C.accentDark, margin: 0 }); yTop = o.y + 0.4; }
    const avH = o.h - (o.title ? 0.4 : 0);
    const sc = Math.min(o.w / m.w, avH / m.h, o.cap);
    const dw = m.w * sc, dh = m.h * sc, px = o.x + (o.w - dw) / 2;
    slide.addShape(pres.shapes.RECTANGLE, { x: px, y: yTop, w: dw, h: dh, fill: { color: C.codeBg }, line: { type: "none" }, shadow: mShadow() });
    slide.addImage({ path: asset(key), x: px, y: yTop, w: dw, h: dh });
    return yTop + dh;
  }

  // equation strip = light panel with centered, stacked typeset-math images.
  // HOUSE RULE: every equation gets a `where` legend defining its symbols.
  //   o.where = [[symbol, definition], ...]
  function formula(slide, keys, o) {
    if (!Array.isArray(keys)) keys = [keys];
    o = Object.assign({ x: 0.55, y: 1.4, w: 12.2, lineH: 0.8, cap: 1.5, where: null, legendFs: 16, legendH: 0.78 }, o || {});
    const maxW = o.w - 0.5;
    const placed = keys.map(k => {
      const m = manifest[k];
      if (!m) throw new Error(`No rendered asset for equation key "${k}".`);
      const sc = Math.min(maxW / m.w, o.lineH / m.h, o.cap);
      return { k, w: m.w * sc, h: m.h * sc };
    });
    if (!o.where) console.warn(`formula("${keys.join(",")}"): no \`where\` legend — house style asks every equation to define its symbols.`);
    const gap = 0.16;
    const eqInner = placed.reduce((a, p) => a + p.h, 0) + gap * (placed.length - 1);
    const legendBlock = o.where ? o.legendH + 0.16 : 0;
    const stripH = eqInner + legendBlock + 0.4;
    const eqRegion = stripH - legendBlock;
    slide.addShape(pres.shapes.RECTANGLE, { x: o.x, y: o.y, w: o.w, h: stripH, fill: { color: C.light }, line: { type: "none" } });
    slide.addShape(pres.shapes.RECTANGLE, { x: o.x, y: o.y, w: 0.08, h: stripH, fill: { color: C.accent }, line: { type: "none" } });
    let cy = o.y + (eqRegion - eqInner) / 2;
    placed.forEach(p => { slide.addImage({ path: asset(p.k), x: o.x + (o.w - p.w) / 2, y: cy, w: p.w, h: p.h }); cy += p.h + gap; });
    if (o.where) {
      const runs = [{ text: "where   ", options: { italic: true, bold: true, color: C.muted } }];
      o.where.forEach((wd, i) => {
        runs.push({ text: wd[0], options: { bold: true, color: C.accentDark } });
        runs.push({ text: " = " + wd[1], options: { color: C.body } });
        if (i < o.where.length - 1) runs.push({ text: "    ·    ", options: { color: C.line } });
      });
      slide.addText(runs, { x: o.x + 0.28, y: o.y + eqRegion + 0.02, w: o.w - 0.56, h: o.legendH, fontFace: BODY, fontSize: o.legendFs, valign: "top", margin: 0, lineSpacingMultiple: 1.12 });
    }
    return o.y + stripH;
  }

  function figurePlaceholder(slide, o) {
    o = Object.assign({ x: L.FX, y: 2.0, w: L.FW, h: 3.0, label: "FIGURE", note: "Add figure here." }, o || {});
    slide.addShape(pres.shapes.RECTANGLE, { x: o.x, y: o.y, w: o.w, h: o.h, fill: { color: C.light }, line: { color: C.accent, width: 1.5, dashType: "dash" } });
    slide.addText(o.label, { x: o.x, y: o.y + o.h / 2 - 0.62, w: o.w, h: 0.42, fontFace: BODY, fontSize: 16, bold: true, color: C.accentDark, align: "center", margin: 0 });
    slide.addText("Note: " + o.note, { x: o.x + 0.35, y: o.y + o.h / 2 - 0.08, w: o.w - 0.7, h: 1.0, fontFace: BODY, fontSize: SCALE.caption, italic: true, color: C.muted, align: "center", margin: 0, lineSpacingMultiple: 1.1 });
  }

  // items: [{ t, lvl, b(bold), c(color), fs, sa(spaceAfter) }]
  function bullets(slide, items, o) {
    o = Object.assign({ x: 0.55, y: 2.0, w: 6.0, h: 4.5, fontSize: SCALE.body, color: C.body }, o || {});
    const runs = items.map(it => ({ text: it.t, options: { bullet: { indent: 18 }, indentLevel: it.lvl || 0, breakLine: true, bold: it.b || false, color: it.c || o.color, fontSize: it.fs || o.fontSize, paraSpaceAfter: it.sa != null ? it.sa : 12 } }));
    slide.addText(runs, { x: o.x, y: o.y, w: o.w, h: o.h, fontFace: BODY, valign: "top", margin: 0 });
  }

  function card(slide, x, y, w, h, fill) {
    slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill || C.white }, line: { color: C.line, width: 1 }, rectRadius: 0.08, shadow: { type: "outer", color: "000000", blur: 4, offset: 1, angle: 135, opacity: 0.10 } });
  }

  function callout(slide, x, y, w, h, title, text) {
    card(slide, x, y, w, h, C.light);
    let ty = y + 0.16;
    if (title) { slide.addText(title, { x: x + 0.28, y: ty, w: w - 0.56, h: 0.4, fontFace: BODY, fontSize: SCALE.bodySmall, bold: true, color: C.accentDark, margin: 0 }); ty += 0.42; }
    slide.addText(text, { x: x + 0.28, y: ty, w: w - 0.56, h: y + h - ty - 0.12, fontFace: BODY, fontSize: SCALE.bodySmall, italic: !title, color: title ? C.body : C.accentDark, margin: 0, lineSpacingMultiple: 1.16, valign: "middle" });
  }

  // header row + body rows; columns auto. rows = array of arrays of strings.
  function table(slide, rows, o) {
    o = Object.assign({ x: 0.55, y: 1.65, w: 12.23, colW: null, rowH: 0.8, fontSize: SCALE.tableText }, o || {});
    const data = rows.map((r, ri) => r.map(cell => ri === 0
      ? { text: cell, options: { bold: true, color: C.white, fill: { color: C.primary } } }
      : (typeof cell === "string" ? cell : cell)));
    slide.addTable(data, { x: o.x, y: o.y, w: o.w, colW: o.colW || undefined, rowH: o.rowH, fontFace: BODY, fontSize: o.fontSize, color: C.body, valign: "middle", border: { pt: 0.5, color: C.line }, align: "left", autoPage: false });
  }

  return { pres, theme: C, SCALE, L, LAYOUT: L,
    titleSlide, contentSlide, divider, codePanel, formula, figurePlaceholder,
    bullets, card, callout, table, footer, shapes: () => pres.shapes };
}

module.exports = { createDeck, loadTheme, listThemes, SCALE, LAYOUT };
