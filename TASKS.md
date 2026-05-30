# Tasks

## Active

### Repo & Structure
- [ ] **Set up GitHub repo** - initialize with README, folder structure (slides/, notebooks/, docs/)
- [ ] **Write intro README** - scope, audience, how to use the repo

### Presentation Slides
- [ ] **Section 1: Background of survival data** (~5 slides)
  - What is survival analysis
  - What is censored data
  - What is an event
  - Multi-events and competing events
- [ ] **Section 2: Applications of survival analysis** (~5 slides)
  - Clinician goals: risk score, risk stratification, event probability by time
  - Types of events: recurrence, death
- [ ] **Section 3: Loss functions for survival analysis** (~5 slides)
  - Cox PH loss
  - Negative log-likelihood loss
  - Log-rank loss
  - DeepHIT loss
- [ ] **Section 4: Thresholds** (~3 slides)
  - Median
  - Youden
  - Max log-rank training cutoff
- [ ] **Section 5: Evaluation metrics** (~5 slides)
  - C-index
  - Brier score
  - KM curves
  - Time-dependent AUCs
- [ ] **Section 6: Packages overview** (~3 slides)
  - pycox, lifelines, torchsurv, scikit-survival
- [ ] **Section 7: Tutorial — SSL3D-Survival** (~5–10 slides)
  - End-to-end walkthrough

### Notebooks / Code
- [ ] **Notebook: survival basics** - censoring, KM curves, log-rank test with lifelines
- [ ] **Notebook: Cox PH on tabular + image features** - scikit-survival / pycox
- [ ] **Notebook: Deep learning survival (DeepSurv / DeepHIT)** - torchsurv or pycox
- [ ] **Notebook: SSL3D-Survival tutorial** - full pipeline walkthrough
- [ ] **Add benchmark datasets** - TCIA or similar public 3D imaging + survival data

## Waiting On

## Someday

- [ ] **Interactive threshold explorer** - visualize Youden / max log-rank cutoffs
- [ ] **Time-dependent AUC deep dive** - notebook with worked example

## Done
