"""Deterministic figure generation for the survival mini-course (module 01).

Every figure is built from synthetic data with a fixed RNG seed and the house
`academic_navy` palette, so re-running reproduces byte-stable SVGs. Conceptual
diagrams use small synthetic examples on purpose — they read more clearly than a
real dataset. Real fitted-model figures (modules 02-03) will load GBSG2 instead.

Usage:  python3 scripts/make_figures.py
Output: assets/figures/*.svg
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- house palette (deck_toolkit/themes.json -> academic_navy) -------------
PRIMARY = "#1B2A41"
ACCENT = "#1C7293"
ACCENT_DARK = "#0F4C5C"
BODY = "#33415A"
MUTED = "#5B6B7F"
LIGHT = "#EEF2F7"
LINE = "#CBD5E1"
CORAL = "#EF6F6C"  # second categorical color (from slate_coral) for contrast
AMBER = "#E0A100"  # third categorical color (from charcoal_amber)
GREEN = "#2E9E6B"  # fourth categorical color (from forest_moss)

OUT = Path(__file__).resolve().parent.parent / "assets" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def _style():
    """Shared rcParams so every figure matches the deck house style."""
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Georgia", "Times New Roman", "DejaVu Serif"],
            "font.size": 12,
            "axes.edgecolor": MUTED,
            "axes.labelcolor": BODY,
            "axes.titlecolor": PRIMARY,
            "text.color": BODY,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )


def _save(fig, name):
    path = OUT / f"{name}.svg"
    fig.savefig(path, format="svg")
    plt.close(fig)
    print(f"  wrote {path.relative_to(OUT.parent.parent)}")


# --- 1.1  hazard -> cumulative hazard -> survival --------------------------
def fig_hazard_vs_cumhazard():
    """Speedometer (h) -> odometer (H=int h) -> survival (S=e^-H).

    Post-surgery shape from 1.1: hazard spikes early (complications), falls as
    the patient recovers, then drifts up slowly with age.
    """
    t = np.linspace(0, 24, 600)  # months
    h = 0.18 * np.exp(-t / 2.5) + 0.012 + 0.0016 * t  # early spike + slow rise
    H = np.cumsum(h) * (t[1] - t[0])  # discrete integral of h
    S = np.exp(-H)

    fig, axes = plt.subplots(1, 3, figsize=(11, 3.3))

    axes[0].plot(t, h, color=ACCENT, lw=2.2)
    axes[0].fill_between(t, h, color=ACCENT, alpha=0.10)
    axes[0].set_title("Hazard $h(t)$")
    axes[0].text(0.5, 0.92, "speedometer\n(rate right now)", transform=axes[0].transAxes,
                 ha="center", va="top", fontsize=10, color=MUTED, style="italic")

    axes[1].plot(t, H, color=ACCENT_DARK, lw=2.2)
    axes[1].set_title(r"Cumulative hazard $H(t)=\int_0^t h$")
    axes[1].text(0.5, 0.18, "odometer\n(total so far)", transform=axes[1].transAxes,
                 ha="center", va="top", fontsize=10, color=MUTED, style="italic")

    axes[2].plot(t, S, color=PRIMARY, lw=2.2)
    axes[2].set_ylim(0, 1.02)
    axes[2].set_title(r"Survival $S(t)=e^{-H(t)}$")
    axes[2].text(0.5, 0.40, "fraction still\nevent-free", transform=axes[2].transAxes,
                 ha="center", va="top", fontsize=10, color=MUTED, style="italic")

    for ax in axes:
        ax.set_xlabel("time (months)")
        ax.set_xlim(0, 24)
        ax.margins(y=0.05)
    fig.tight_layout()
    _save(fig, "1.1_hazard_to_survival")


# --- 1.1 / 3.3  Kaplan-Meier step curve ------------------------------------
def fig_km_step():
    """KM survival estimate as a step function, with censoring ticks.

    Hand-computed S(t) = prod (1 - d_j / n_j) over event times, so the figure
    matches the estimator the course describes rather than a black-box call.
    """
    # (time, event?) for a small synthetic cohort
    times = np.array([2, 3, 5, 6, 7, 9, 11, 13, 15, 18, 20, 23])
    events = np.array([1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1])  # 0 = censored

    order = np.argsort(times)
    times, events = times[order], events[order]
    n = len(times)

    t_steps, s_steps = [0.0], [1.0]
    S, at_risk = 1.0, n
    for i, (ti, ei) in enumerate(zip(times, events)):
        if ei == 1:  # event drops survival
            S *= 1 - 1 / at_risk
            t_steps.extend([ti, ti])
            s_steps.extend([s_steps[-1], S])
        at_risk -= 1
    t_steps.append(times.max())
    s_steps.append(s_steps[-1])

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.step(t_steps, s_steps, where="post", color=PRIMARY, lw=2.2)

    # censoring ticks sit on the curve at the censoring time
    def s_at(t):
        s = 1.0
        ar = n
        for ti, ei in zip(times, events):
            if ti <= t and ei == 1:
                s *= 1 - 1 / ar
            if ti <= t:
                ar -= 1
        return s

    cens_t = times[events == 0]
    ax.plot(cens_t, [s_at(t) for t in cens_t], "|", color=ACCENT,
            markersize=14, markeredgewidth=2.2, label="censored")

    ax.set_ylim(0, 1.02)
    ax.set_xlim(0, times.max() + 0.5)
    ax.set_xlabel("time (months)")
    ax.set_ylabel("$S(t)$  —  probability event-free")
    ax.set_title("Kaplan-Meier estimate: a step down at each event")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    _save(fig, "1.1_km_step")


# --- 1.2  censoring timeline -----------------------------------------------
def fig_censoring_timeline():
    """Per-subject follow-up lines: filled dot = event, open arrow = censored."""
    # (label, entry, observed_time, event?)
    subjects = [
        ("P1", 0, 14, 1),
        ("P2", 0, 24, 0),   # still event-free at study end -> censored
        ("P3", 3, 11, 1),
        ("P4", 0, 24, 0),
        ("P5", 5, 9, 1),
        ("P6", 2, 19, 0),   # lost to follow-up
        ("P7", 0, 7, 1),
        ("P8", 6, 24, 0),
    ]
    study_end = 24

    fig, ax = plt.subplots(figsize=(8, 4.2))
    for i, (lab, t0, t1, ev) in enumerate(subjects):
        y = len(subjects) - i
        ax.hlines(y, t0, t1, color=LINE, lw=2.4, zorder=1)
        if ev == 1:
            ax.plot(t1, y, "o", color=PRIMARY, markersize=9, zorder=3)
        else:
            ax.plot(t1, y, ">", color=ACCENT, markersize=9, zorder=3)
        ax.text(-0.6, y, lab, ha="right", va="center", fontsize=10, color=BODY)

    ax.axvline(study_end, color=CORAL, ls="--", lw=1.6)
    ax.text(study_end, len(subjects) + 0.7, "study ends", color=CORAL,
            ha="center", fontsize=10)

    # legend proxies
    ax.plot([], [], "o", color=PRIMARY, markersize=9, label="event observed ($\\delta=1$)")
    ax.plot([], [], ">", color=ACCENT, markersize=9, label="censored ($\\delta=0$)")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12),
              ncol=2, fontsize=10)

    ax.set_yticks([])
    ax.set_xlim(-2.5, study_end + 2)
    ax.set_ylim(0.3, len(subjects) + 1.3)
    ax.set_xlabel("time (months)")
    ax.set_title("Censoring: each subject contributes follow-up up to their last-seen time")
    ax.spines["left"].set_visible(False)
    fig.tight_layout()
    _save(fig, "1.2_censoring_timeline")


# --- 1.4  CIF vs the 1 - S(t) overestimate ---------------------------------
def fig_cif_vs_oneminuss():
    """Under competing risks, 1 - S(t) overestimates incidence of event 1.

    Build two cause-specific hazards in discrete time, then compute:
      - CIF_1 = sum S(u^-) * h_1(u)        (correct, Aalen-Johansen style)
      - 1 - KM_1 = naive complement treating event 2 as censoring (overestimate)
    """
    t = np.arange(0, 60)
    dt = 1.0
    h1 = np.full_like(t, 0.020, dtype=float)  # event of interest (recurrence)
    h2 = np.full_like(t, 0.035, dtype=float)  # competing event (death)

    S = np.ones_like(t, dtype=float)  # overall survival, both causes
    cif1 = np.zeros_like(t, dtype=float)
    s = 1.0
    acc = 0.0
    for i in range(len(t)):
        acc += s * h1[i] * dt          # weight each instant by being event-free so far
        cif1[i] = acc
        s *= np.exp(-(h1[i] + h2[i]) * dt)
        S[i] = s

    # naive: KM for event 1 alone, treating competing event as censoring
    km1 = np.exp(-np.cumsum(h1) * dt)
    naive = 1 - km1

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(t, naive, color=CORAL, lw=2.2, ls="--",
            label=r"$1-S_1(t)$  (naive, overestimates)")
    ax.plot(t, cif1, color=ACCENT, lw=2.4,
            label=r"$\mathrm{CIF}_1(t)$  (correct, Aalen-Johansen)")
    ax.fill_between(t, cif1, naive, color=CORAL, alpha=0.10)
    ax.annotate("overestimation gap", xy=(45, (cif1[45] + naive[45]) / 2),
                xytext=(28, 0.62), fontsize=10, color=MUTED,
                arrowprops=dict(arrowstyle="->", color=MUTED))

    ax.set_xlim(0, 59)
    ax.set_ylim(0, 0.8)
    ax.set_xlabel("time (months)")
    ax.set_ylabel("probability of event 1 by $t$")
    ax.set_title("Competing risks: why $1-S(t)$ overstates cumulative incidence")
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    fig.tight_layout()
    _save(fig, "1.4_cif_vs_oneminuss")


# ===========================================================================
# Module 02 — loss functions
# ===========================================================================

# --- 2.1  proportional vs. crossing hazards --------------------------------
def fig_proportional_hazards():
    """The PH assumption: a constant hazard ratio (left) vs. a violation (right).

    Left mirrors the model -- two patients whose hazards are a fixed multiple of
    one baseline, so the curves never cross. Right is the surgery example from
    2.1: high early risk that becomes protective later, so the curves cross.
    """
    t = np.linspace(0.2, 24, 400)
    base = 0.02 + 0.0018 * t  # a gently rising baseline hazard

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)

    # Left: proportional — patient B's hazard is a constant 2.4x patient A's
    hr = 2.4
    axes[0].plot(t, base, color=ACCENT, lw=2.2, label="patient A (baseline)")
    axes[0].plot(t, hr * base, color=CORAL, lw=2.2, label=f"patient B ($\\times{hr}$)")
    axes[0].set_title("Proportional hazards — holds\nconstant ratio, curves never cross", fontsize=12)
    axes[0].legend(frameon=False, loc="upper left", fontsize=9)

    # Right: crossing — treated arm high early, protective later
    treated = 0.16 * np.exp(-t / 4) + 0.012
    control = 0.018 + 0.0022 * t
    axes[1].plot(t, control, color=ACCENT, lw=2.2, label="control")
    axes[1].plot(t, treated, color=CORAL, lw=2.2, label="treated (surgery)")
    # mark the crossing point
    cross = np.argmin(np.abs(treated - control))
    axes[1].plot(t[cross], treated[cross], "o", color=PRIMARY, ms=7, zorder=5)
    axes[1].set_title("Proportional hazards violated\nratio flips, curves cross", fontsize=12)
    axes[1].legend(frameon=False, loc="upper right", fontsize=9)

    for ax in axes:
        ax.set_xlabel("time (months)")
        ax.set_xlim(0, 24)
        ax.set_ylim(0, 0.18)
    axes[0].set_ylabel("hazard $h(t)$")
    fig.tight_layout()
    _save(fig, "2.1_proportional_hazards")


# --- 2.2  parametric hazard shapes -----------------------------------------
def fig_hazard_shapes():
    """The hazard shapes each parametric family can take (the 2.2 table, drawn)."""
    t = np.linspace(0.05, 10, 500)

    # exponential: constant
    h_exp = np.full_like(t, 0.35)
    # Weibull hazard h = (k/lam) (t/lam)^(k-1)
    def weib_h(k, lam):
        return (k / lam) * (t / lam) ** (k - 1)
    h_winc = weib_h(2.2, 6.0)   # increasing
    h_wdec = weib_h(0.6, 2.5)   # decreasing
    # log-normal hazard = f/S, computed numerically (hump shape)
    mu, sigma = 1.3, 0.5
    pdf = (1 / (t * sigma * np.sqrt(2 * np.pi))) * np.exp(
        -((np.log(t) - mu) ** 2) / (2 * sigma ** 2))
    from math import erf
    cdf = np.array([0.5 * (1 + erf((np.log(ti) - mu) / (sigma * np.sqrt(2)))) for ti in t])
    h_logn = pdf / np.clip(1 - cdf, 1e-6, None)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t, h_exp, color=MUTED, lw=2.2, label="Exponential — constant")
    ax.plot(t, h_winc, color=ACCENT, lw=2.2, label="Weibull ($k>1$) — rising")
    ax.plot(t, h_wdec, color=CORAL, lw=2.2, label="Weibull ($k<1$) — falling")
    ax.plot(t, h_logn, color=AMBER, lw=2.2, label="Log-normal — rises then falls")

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.2)
    ax.set_xlabel("time")
    ax.set_ylabel("hazard $h(t)$")
    ax.set_title("Each distribution fixes the shape the hazard may take")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    fig.tight_layout()
    _save(fig, "2.2_hazard_shapes")


# --- 2.4  DeepHit joint PMF and the CIFs read off it -----------------------
def fig_deephit_pmf():
    """Left: the network's per-(cause, bin) probability mass. Right: the CIFs
    and overall survival obtained by summing cells (2.4 'read off by summing')."""
    bins = np.arange(1, 13)
    # two causes; smooth bumps, normalized to leave residual survival mass
    p1 = np.exp(-((bins - 5) ** 2) / 8.0) * 0.06   # relapse, peaks ~month 5
    p2 = np.exp(-((bins - 9) ** 2) / 10.0) * 0.045  # death, later/flatter
    cif1 = np.cumsum(p1)
    cif2 = np.cumsum(p2)
    surv = 1 - (cif1 + cif2)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))

    w = 0.4
    axes[0].bar(bins - w / 2, p1, width=w, color=ACCENT, label="cause 1 (relapse)")
    axes[0].bar(bins + w / 2, p2, width=w, color=CORAL, label="cause 2 (death)")
    axes[0].set_title(r"Network output: $p_k(t\mid x)=P(T=t,\,K=k)$")
    axes[0].set_xlabel("time bin")
    axes[0].set_ylabel("probability mass")
    axes[0].legend(frameon=False, fontsize=9)

    axes[1].step(bins, cif1, where="mid", color=ACCENT, lw=2.2, label=r"$\mathrm{CIF}_1$ (relapse)")
    axes[1].step(bins, cif2, where="mid", color=CORAL, lw=2.2, label=r"$\mathrm{CIF}_2$ (death)")
    axes[1].step(bins, surv, where="mid", color=PRIMARY, lw=2.2, label=r"$S(t)$ overall")
    axes[1].set_title("Read off by summing cells")
    axes[1].set_xlabel("time bin")
    axes[1].set_ylim(0, 1.02)
    axes[1].legend(frameon=False, fontsize=9, loc="upper right")

    fig.tight_layout()
    _save(fig, "2.4_deephit_pmf")


# --- 2.5  positioning map of the loss families -----------------------------
def fig_method_map():
    """Place the five loss families on (flexibility, output) axes — a visual of
    the two big trade-off tables in 2.5."""
    # x = flexibility (rigid assumptions -> flexible); y = output (ranking -> prob)
    methods = [
        ("Cox PH", 0.22, 0.12, ACCENT),
        ("Parametric\nNLL", 0.40, 0.88, AMBER),
        ("Discrete-time\nNLL", 0.62, 0.66, GREEN),
        ("DeepHit", 0.86, 0.78, CORAL),
        ("DSM", 0.74, 0.95, ACCENT_DARK),
    ]
    fig, ax = plt.subplots(figsize=(7.6, 4.6))
    for name, x, y, c in methods:
        ax.scatter(x, y, s=260, color=c, alpha=0.9, zorder=3, edgecolor="white", lw=1.5)
        ax.annotate(name, (x, y), textcoords="offset points", xytext=(0, 13),
                    color=PRIMARY, fontsize=9.5, ha="center", va="bottom", zorder=4)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.18)
    ax.set_xlabel(r"flexibility  —  assumptions imposed on time  $\rightarrow$")
    ax.set_ylabel(r"output: ranking  $\rightarrow$  absolute probability")
    ax.set_xticks([0.05, 0.95])
    ax.set_xticklabels(["rigid\n(PH / fixed shape)", "flexible\n(no PH, no shape)"], fontsize=9)
    ax.set_yticks([0.08, 1.0])
    ax.set_yticklabels(["risk\nscore", "full $S(t)$\n+ CIF"], fontsize=9)
    ax.set_title("Where each loss family sits")
    ax.grid(True, color=LIGHT, lw=1)
    ax.set_axisbelow(True)
    fig.tight_layout()
    _save(fig, "2.5_method_map")


# ===========================================================================
# Module 03 — metrics
# ===========================================================================

# --- 3.1  C-index concordant / discordant pairs ----------------------------
def fig_cindex_pairs():
    """The 2.1 worked example, drawn: risk score vs observed time, with each
    comparable pair colored concordant (teal) or discordant (coral)."""
    # (label, time, event?, risk)
    pts = {"A": (2, 1, 0.9), "B": (5, 1, 0.4), "C": (8, 0, 0.7)}
    fig, ax = plt.subplots(figsize=(7, 4.2))

    # comparable pairs: earlier-failing patient (must be an event) vs later
    pairs = [("A", "B", True), ("A", "C", True), ("B", "C", False)]
    for a, b, concordant in pairs:
        (ta, _, ra), (tb, _, rb) = pts[a], pts[b]
        col = ACCENT if concordant else CORAL
        ax.plot([ta, tb], [ra, rb], color=col, lw=2.0, alpha=0.8, zorder=1)

    for lab, (t, ev, r) in pts.items():
        if ev == 1:
            ax.plot(t, r, "o", color=PRIMARY, ms=13, zorder=3)
        else:
            ax.plot(t, r, "o", mfc="white", mec=PRIMARY, mew=2, ms=13, zorder=3)
        ax.annotate(lab, (t, r), color="white" if ev else PRIMARY,
                    fontsize=9, ha="center", va="center", zorder=4,
                    fontweight="bold")

    # legend proxies
    ax.plot([], [], color=ACCENT, lw=2.4, label="concordant (right order)")
    ax.plot([], [], color=CORAL, lw=2.4, label="discordant (wrong order)")
    ax.plot([], [], "o", color=PRIMARY, ms=10, label="event observed")
    ax.plot([], [], "o", mfc="white", mec=PRIMARY, mew=2, ms=10, label="censored")
    ax.legend(frameon=False, fontsize=9, loc="upper right", ncol=1)

    ax.text(0.02, 0.02, r"$\hat{C} = 2/3 \approx 0.67$", transform=ax.transAxes,
            fontsize=12, color=PRIMARY)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("observed time $T$  (earlier = should be riskier)")
    ax.set_ylabel("risk score $r$")
    ax.set_title("C-index: does the riskier patient fail first?")
    fig.tight_layout()
    _save(fig, "3.1_cindex_pairs")


# --- 3.2  Brier score over time vs baselines -------------------------------
def fig_brier_curve():
    """BS(t) for a model vs the KM baseline vs the uninformative 0.25 line; the
    shaded area under the model curve is the integrated Brier score."""
    t = np.linspace(0, 36, 200)
    bs_model = 0.04 + 0.0032 * t - 0.00003 * t ** 2     # good, drifts up mildly
    bs_km = 0.07 + 0.0050 * t - 0.00004 * t ** 2        # covariate-free baseline
    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    ax.axhline(0.25, color=MUTED, ls=":", lw=1.6, label="uninformative (0.25)")
    ax.plot(t, bs_km, color=CORAL, lw=2.2, ls="--", label="Kaplan-Meier baseline")
    ax.plot(t, bs_model, color=ACCENT, lw=2.4, label="model")
    ax.fill_between(t, bs_model, color=ACCENT, alpha=0.10)
    ax.annotate("IBS = area under\nthe model curve", xy=(20, bs_model[110] / 2),
                xytext=(7, 0.16), fontsize=10, color=MUTED,
                arrowprops=dict(arrowstyle="->", color=MUTED))

    ax.set_xlim(0, 36)
    ax.set_ylim(0, 0.3)
    ax.set_xlabel("time (months)")
    ax.set_ylabel("$BS(t)$  (lower = better)")
    ax.set_title("Brier score: calibration over time — beat the KM baseline")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    _save(fig, "3.2_brier_curve")


def _km(times, events):
    """Kaplan-Meier step arrays from (times, events). Returns (t_steps, s_steps)."""
    order = np.argsort(times)
    times, events = np.asarray(times)[order], np.asarray(events)[order]
    n = len(times)
    t_steps, s_steps = [0.0], [1.0]
    S, at_risk = 1.0, n
    for ti, ei in zip(times, events):
        if ei == 1:
            S *= 1 - 1 / at_risk
            t_steps.extend([ti, ti])
            s_steps.extend([s_steps[-1], S])
        at_risk -= 1
    t_steps.append(times.max())
    s_steps.append(s_steps[-1])
    return np.array(t_steps), np.array(s_steps)


# --- 3.3  stratified KM (high vs low risk) ---------------------------------
def fig_stratified_km():
    """The headline evaluation figure: KM curves for model-defined high- and
    low-risk groups, well separated, with a log-rank p-value."""
    rng = np.random.default_rng(7)
    n = 60

    def sample(rate, horizon=36):
        # exponential event times, administrative censoring at `horizon`
        evt = rng.exponential(1 / rate, n)
        t = np.minimum(evt, horizon)
        e = (evt <= horizon).astype(int)
        return t, e

    t_hi, e_hi = sample(0.07)   # high risk: events sooner
    t_lo, e_lo = sample(0.022)  # low risk: events later

    th, sh = _km(t_hi, e_hi)
    tl, sl = _km(t_lo, e_lo)

    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.step(tl, sl, where="post", color=ACCENT, lw=2.4, label="Low risk")
    ax.step(th, sh, where="post", color=CORAL, lw=2.4, label="High risk")

    ax.text(0.97, 0.9, "log-rank $p < 0.001$", transform=ax.transAxes,
            ha="right", fontsize=11, color=PRIMARY)
    ax.set_xlim(0, 36)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("time (months)")
    ax.set_ylabel("$S(t)$")
    ax.set_title("Stratified KM: do the model's risk groups separate?")
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    fig.tight_layout()
    _save(fig, "3.3_stratified_km")


# --- 3.4  time-dependent AUC over horizons ---------------------------------
def fig_auc_over_time():
    """AUC(t): a robust model (flat-high) vs one that degrades at long horizons —
    discrimination resolved by time, which a single C-index hides."""
    t = np.linspace(3, 36, 200)
    auc_robust = 0.82 + 0.02 * np.sin(t / 6)
    auc_degrade = 0.86 - 0.0075 * (t - 3)
    fig, ax = plt.subplots(figsize=(7.2, 4.2))

    ax.axhline(0.5, color=MUTED, ls=":", lw=1.6, label="chance (0.5)")
    ax.plot(t, auc_robust, color=ACCENT, lw=2.4, label="robust model")
    ax.plot(t, auc_degrade, color=CORAL, lw=2.4, label="degrades at long horizons")

    ax.set_xlim(0, 36)
    ax.set_ylim(0.45, 1.0)
    ax.set_xlabel("time horizon $t$ (months)")
    ax.set_ylabel(r"$\mathrm{AUC}(t)$")
    ax.set_title("Time-dependent AUC: when does the model discriminate well?")
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    fig.tight_layout()
    _save(fig, "3.4_auc_over_time")


def main():
    _style()
    np.random.seed(0)
    print("Generating figures ->", OUT)
    # module 01
    fig_hazard_vs_cumhazard()
    fig_km_step()
    fig_censoring_timeline()
    fig_cif_vs_oneminuss()
    # module 02
    fig_proportional_hazards()
    fig_hazard_shapes()
    fig_deephit_pmf()
    fig_method_map()
    # module 03
    fig_cindex_pairs()
    fig_brier_curve()
    fig_stratified_km()
    fig_auc_over_time()
    print("done.")


if __name__ == "__main__":
    main()
