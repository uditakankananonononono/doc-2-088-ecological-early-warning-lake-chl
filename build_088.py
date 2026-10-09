"""DOC-2-088: build matched case/control windows (frozen rules in PROTOCOL.md). Needs chl_ts.csv, bpanom.csv. No indicator is computed here."""
import numpy as np, pandas as pd
ts = pd.read_csv("chl_ts.csv", usecols=["lagoslakeid", "year", "chl_median_ugl"]).dropna(subset=["chl_median_ugl"]); ts = ts[ts.chl_median_ugl > 0]
bp = pd.read_csv("bpanom.csv", usecols=["lagoslakeid", "year", "is.breakpoint"])
bpy = bp[bp["is.breakpoint"] == 1].groupby("lagoslakeid").year.min()
yrs = ts.groupby("lagoslakeid").year.agg(["min", "max", "count"]); lakes_full = yrs[(yrs["max"] - yrs["min"] + 1 == yrs["count"]) & (yrs["count"] >= 25)].index
ts = ts[ts.lagoslakeid.isin(lakes_full)]; mean = ts.groupby("lagoslakeid").chl_median_ugl.apply(lambda s: np.log(s).mean()); first = yrs["min"]
cases = [(l, int(bpy[l])) for l in bpy.index if l in mean.index and int(bpy[l]) - 1 - first[l] + 1 >= 12]
nobp = sorted(set(mean.index) - set(bpy.index)); rng = np.random.default_rng(88)
q = pd.qcut(mean, 10, labels=False); pool = {d: [l for l in nobp if q[l] == d] for d in range(10)}
rows = []; used = set()
for l, by in sorted(cases):
    s, e = int(first[l]), by - 1  # window = first observed year .. year before breakpoint (>= 12 yrs)
    cand = [c for c in pool[q[l]] if c not in used and yrs.loc[c, "min"] <= s and yrs.loc[c, "max"] >= e]
    if not cand: continue
    c = cand[rng.integers(len(cand))]; used.add(c); rows.append((l, c, s, e))
pd.DataFrame(rows, columns=["case", "control", "start", "end"]).to_csv("pairs.tsv", sep="\t", index=False)
print("BUILD_DONE lakes_complete", len(lakes_full), "breakpoint_lakes", len(bpy), "eligible_cases", len(cases), "matched_pairs", len(rows))
