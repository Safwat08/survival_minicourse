#!/usr/bin/env python3
"""
render_assets.py — render code snippets and equations to crisp PNGs for the deck toolkit.

Why: PowerPoint substitutes monospace fonts unpredictably and has no real math
typesetting. We sidestep both by rendering code (real monospace) and equations
(LaTeX-style mathtext) to images, themed by the palette in themes.json.

Usage:
    python render_assets.py <theme_name> <spec.json> <out_dir>

Spec format (JSON):
{
  "codeFontSize": 15,            # optional, default 15
  "eqFontSize": 30,             # optional, default 30
  "code": {
    "key_a": [["from x import y", 0], ["# a comment", 1], ...]   # [text, is_comment]
  },
  "equations": {
    "key_b": "$S(t) = P(T > t)$"   # mathtext; use \\leq, \\frac, \\sum, \\prod, \\int, etc.
  }
}

Writes <out_dir>/<key>.png for every key and <out_dir>/manifest.json
mapping each key -> {"w": inches, "h": inches} (used by deck_lib.js for placement).
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(1)
    theme_name, spec_path, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    here = os.path.dirname(os.path.abspath(__file__))
    themes = json.load(open(os.path.join(here, "themes.json")))
    if theme_name not in themes:
        avail = [k for k in themes if not k.startswith("_")]
        sys.exit(f"Unknown theme '{theme_name}'. Available: {', '.join(avail)}")
    T = themes[theme_name]
    spec = json.load(open(spec_path))
    os.makedirs(out_dir, exist_ok=True)

    DPI = 220
    hx = lambda h: "#" + h
    CODEBG, CODEFG, CODEAC = hx(T["codeBg"]), hx(T["codeFg"]), hx(T["codeComment"])
    ACCENT, PRIMARY = hx(T["accent"]), hx(T["primary"])

    manifest = {}

    # ---------------- CODE BLOCKS ----------------
    FS = float(spec.get("codeFontSize", 15.0))
    CHARW = FS * 0.602 / 72.0   # DejaVu Sans Mono advance width (in)
    LINEH = FS * 1.55 / 72.0
    PADX, PADY, BAR = 0.16, 0.14, 0.06
    for key, lines in spec.get("code", {}).items():
        maxlen = max((len(t) for t, _ in lines), default=1)
        W = BAR + PADX + maxlen * CHARW + PADX
        Hh = PADY + len(lines) * LINEH + PADY
        fig = plt.figure(figsize=(W, Hh), dpi=DPI)
        fig.patch.set_facecolor(CODEBG)
        fig.add_artist(plt.Rectangle((0, 0), BAR / W, 1, transform=fig.transFigure, color=ACCENT, zorder=2))
        x0 = (BAR + PADX) / W
        for i, (text, is_comment) in enumerate(lines):
            ytop = 1 - (PADY + (i + 0.78) * LINEH) / Hh
            fig.text(x0, ytop, text if text != "" else " ", fontfamily="monospace", fontsize=FS,
                     color=CODEAC if is_comment else CODEFG,
                     style="italic" if is_comment else "normal", va="baseline", ha="left")
        fig.savefig(os.path.join(out_dir, f"{key}.png"), dpi=DPI, facecolor=CODEBG)
        plt.close(fig)
        manifest[key] = {"w": round(W, 3), "h": round(Hh, 3)}

    # ---------------- EQUATIONS (mathtext) ----------------
    EQFS = float(spec.get("eqFontSize", 30))
    for key, tex in spec.get("equations", {}).items():
        fig = plt.figure(figsize=(0.5, 0.5), dpi=DPI)
        t = fig.text(0.5, 0.5, tex, fontsize=EQFS, color=PRIMARY, ha="center", va="center", math_fontfamily="cm")
        fig.canvas.draw()
        bb = t.get_window_extent()
        W, Hh = bb.width / DPI + 0.10, bb.height / DPI + 0.10
        plt.close(fig)
        fig = plt.figure(figsize=(W, Hh), dpi=DPI)
        fig.patch.set_alpha(0)
        fig.text(0.5, 0.5, tex, fontsize=EQFS, color=PRIMARY, ha="center", va="center", math_fontfamily="cm")
        fig.savefig(os.path.join(out_dir, f"{key}.png"), dpi=DPI, transparent=True)
        plt.close(fig)
        manifest[key] = {"w": round(W, 3), "h": round(Hh, 3)}

    json.dump(manifest, open(os.path.join(out_dir, "manifest.json"), "w"), indent=1)
    print(f"OK — {len(manifest)} assets rendered to {out_dir} (theme: {theme_name})")

if __name__ == "__main__":
    main()
