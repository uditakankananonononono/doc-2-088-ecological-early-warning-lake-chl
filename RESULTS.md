# DOC-2-088 RESULTS - independent gate verdict: SCOPED PASS as HONEST NEGATIVE (wording narrowed per gate)

Gate-derived statement: the independent gate re-downloaded both Zenodo files (md5 matched), ran build_088.py and analysis_088.py unchanged and reproduced the results to full float precision, and verified tag-before-results ordering. The verdict applies to the claim below only.

**Canonical claim:** "In 3,499 matched pairs (the lowest-lakeid subset of eligible cases, due to the control-pool limit), neither rolling-variance nor lag-1 autocorrelation Kendall tau before the authors' first detected breakpoint exceeded that of a matched no-breakpoint lake (AUROC 0.483 and 0.498; 97.5% CIs entirely below 0.55). This is a test of these two indicators on short noisy annual satellite series, not of critical slowing down in lakes."

Label (set mechanically by analysis_088.py): **HONEST NEGATIVE**. G1 pass. Prior art: critical-slowing-down indicators are well known and a published lake study reports limited applicability to empirical lake data; this is a measurement on a different dataset, not a novelty claim.

| item | value |
|---|---|
| data | LAGOS-US lake chlorophyll, Zenodo 10926306 (CC-BY-4.0); chl_ts.csv and bpanom.csv, md5 matched Zenodo (DATA_HASHES.tsv) |
| realised set | 24,452 lakes with complete series; 20,884 lakes with a breakpoint flag; 12,064 eligible cases (window >= 12 years); **3,499 matched pairs** (limited by the supply of controls: only 3,568 lakes have no breakpoint flag; see matching-selection limit below). Expectation at lock-1 was "thousands"; the 300-pair floor was passed |
| S_var (rolling-variance tau), paired AUROC case vs control | **0.483**, 97.5% CI [0.465, 0.501]; mean tau case -0.0034 vs control +0.0217; label-swap null 0.5005; pass (lower bound > 0.55): no |
| S_ac1 (rolling lag-1 autocorrelation tau), paired AUROC | **0.498**, 97.5% CI [0.480, 0.517]; mean tau case -0.0066 vs control +0.0113; label-swap null 0.4995; pass: no |
| G1 label-swap control | both null means within [0.48, 0.52]: pass |
| reported only: window ends 2 years before breakpoint (n = 2,037 pairs) | var_tau AUROC 0.488, ac1_tau AUROC 0.497 |
| reported only: window ends 4 years before breakpoint (n = 1,426 pairs) | var_tau AUROC 0.494, ac1_tau AUROC 0.482 |

## What this shows and does not show
- In 3,499 matched pairs of US lake chlorophyll series, neither the rolling-variance trend nor the rolling lag-1 autocorrelation trend before a detected breakpoint exceeded that of a matched lake without a breakpoint. The variance indicator is slightly below 0.5 (CI upper bound 0.501); the autocorrelation indicator is indistinguishable from 0.5. The 2-year and 4-year lead-gap sensitivities agree (all near 0.48-0.50); they are reported only and do not change the label. The gap2 and gap4 sets are nested subsets of the main 3,499 pairs, not independent replications.
- An AUROC below 0.5 for variance (0.483, CI upper 0.501) is not evidence that cases show falling variance; it was not a preregistered direction and the matching/selection caveats apply.
- This does not show that critical slowing down is absent in lakes. The series are 34-point annual summer medians from satellite interpretation, so each rolling statistic is very noisy (low per-series power). Windows are short (12 to about 30 years).
- "Abrupt shift" is the data authors' statistical breakpoint, not an independently confirmed regime shift, and those detections are not all alternative-stable-state transitions.
- Controls are only the 15% of lakes with no breakpoint flag (3,568 lakes). They may differ from lakes with breakpoints in ways beyond mean log-CHL (matching covered mean-CHL decile and calendar years only), so the comparison is not a randomised one.
- Matching-selection limit (gate-identified): matching is first-come in lakeid order against a 3,568-control pool, so only 3,499 of 12,064 eligible cases (29%) received controls, and they are the lowest-lakeid subset, not a random 29%. The result is about those 3,499 cases only.
- Atypical controls (gate-identified): in the matched pairs the detrended residual SD is higher in controls (0.276) than in cases (0.254); the case value is higher in only 42.6% of pairs. Control lakes are therefore not quiet lakes, the groups differ on more than mean chlorophyll, and the sign of the resulting bias on AUROC is unknown.
- Single dataset, one detrending and window rule, no per-series surrogate null, and no other indicators (skewness, spectral reddening). No claim about forecasting skill or management use.

## Disclosures
- Run once. All four locked files match the lock-1 tag (tag_tree_check.txt; tag commit e2c78daa). No amendments.
- run_log.txt gives UTC times, versions and commands; the analysis exit code was not captured separately, but results.json and the RESULT_JSON line in analysis.log are complete.
- build_088.py and analysis_088.py were smoke-tested on synthetic data in scratch directories before lock-1; no record is kept and no result relies on it.
- The 186 MB time-series file and 34 MB breakpoint file are not in this repo; both are the public Zenodo files with md5s in DATA_HASHES.tsv and input_md5.txt. pairs.tsv (matched windows, 3,499 rows, md5 in input_md5.txt) is NOT in this repo (the browser editor could not take an 80 KB file); it is regenerable with build_088.py (seed 88) from the two Zenodo files, and a copy is in the Drive folder.
