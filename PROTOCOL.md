# DOC-2-088 "Ecological early-warning signals": do critical-slowing-down indicators rise before detected abrupt shifts in 24,452 US lake chlorophyll series, relative to matched lakes without shifts? (frozen protocol, lock-1)

Written 2026-10-10 IST and committed BEFORE the lake time series or breakpoint table was downloaded, matched or scored. The ledger holds only the title and source line for DOC-2-088 (no spec text), so this is one narrow, checkable test of the topic. Dedup: no existing mega27, doc230, sp-* or exp200 build binds to DOC-2-088 (matrix owner, 2026-10-10). Prior art: critical-slowing-down indicators are well known, and a published lake study reports limited applicability of such signals to empirical lake data (Early warning signals have limited applicability to empirical lake data, PMC10692136). No novelty claim; this is a measurement on a different, larger dataset.

## Data (frozen)
- LAGOS-US lake chlorophyll dataset, Zenodo record 10926306 (CC-BY-4.0; companion data to "Abrupt changes in algal biomass of thousands of US lakes ..."): cp_chl_climate_timeseries.csv (annual summer-median remote-sensing CHL, 1984-2018, per lake) and cp_chl_bpanom.csv (per lake-year is.breakpoint flag from the data authors' own breakpoint analysis). Downloaded by acquire_088.py; md5 verified against Zenodo's published md5 and recorded in DATA_HASHES.tsv.
- "Abrupt shift" here means the data authors' detected breakpoint (is.breakpoint = 1), NOT an independently confirmed regime shift. The label is a statistical detection on the same series.

## Case and control windows (build_088.py; no indicator computed there)
- Lakes with a complete annual series (no gaps, >= 25 years, CHL > 0, log scale). Case = lake with a breakpoint; its first breakpoint year b defines the window from the lake's first observed year to b-1. Eligible only if the window has >= 12 years.
- Control = a distinct lake with NO breakpoint flag in any year, in the same decile of lake mean log-CHL, observed over the case's whole window, chosen at random (seed 88), without replacement. The control uses the identical calendar years. Cases with no available control are dropped and counted.
- Expectation (not examined before lock-1): the data description gives 24,452 lakes and 71% of climate-influenced lakes with abrupt shifts, so thousands of eligible pairs are likely. Realised counts are reported against this.

## Indicators (analysis_088.py)
- log CHL, linear detrend over the window, rolling window = max(6, n//2), rolling variance and rolling lag-1 autocorrelation; indicator = Kendall tau of each rolling series against time (S_var, S_ac1).

## Estimands and gates
- Primary 1: paired AUROC of S_var, case vs matched control (probability the case's tau exceeds its control's; ties 0.5). Primary 2: same for S_ac1.
- Inference: bootstrap over pairs, 2,000 resamples, seed 12345, 97.5% percentile intervals (Bonferroni over 2 primaries).
- G0 floor: fewer than 300 matched scored pairs -> INSUFFICIENT-DATA, no scoring.
- G1 (control): within-pair label swaps (200 random swaps) give mean AUROC within [0.48, 0.52] for both indicators, else INVALID.
- Pass criterion per indicator: lower bound of the 97.5% interval > 0.55.
- Labels (mechanical): INSUFFICIENT-DATA; INVALID; WARNING-SIGNAL-DETECTED (either primary passes); HONEST NEGATIVE (neither).
- Reported only, cannot change the label: AUROC with the window ending 2 and 4 years before the breakpoint (lead-gap sensitivity); mean tau for cases and controls.

## Limits stated up front
- The series are 34-point annual summer medians from satellite interpretation, so rolling statistics are very noisy; a negative may reflect low power per series, not absence of the phenomenon.
- Breakpoint labels are statistical detections, not confirmed regime shifts; a detected level shift can itself raise variance near the end of the window (the lead-gap sensitivity is only a partial check). Control matching is on lake mean log-CHL and calendar years only; lakes with breakpoints may differ in other ways (size, depth, land use) that affect variance trends. No claim of mechanism or of forecasting skill for management.
- Single dataset, single detrending and window rule, no surrogate-data null per series, no tests of alternative indicators (skewness, spectral reddening).
- Single run; crash fixes are dated AMENDMENT-N.md files committed before outcomes exist. analysis_088.py was smoke-tested on synthetic noise only in a scratch directory; no result is claimed from that.
