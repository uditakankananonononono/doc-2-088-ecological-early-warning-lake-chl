"""DOC-2-088 frozen analysis (PROTOCOL.md lock-1). Run once. Needs chl_ts.csv, pairs.tsv."""
import json, numpy as np, pandas as pd
from scipy.stats import kendalltau
from sklearn.metrics import roc_auc_score as auc
rng = np.random.default_rng(12345)
ts = pd.read_csv("chl_ts.csv", usecols=["lagoslakeid", "year", "chl_median_ugl"]); ts = ts[ts.chl_median_ugl > 0]
S = {l: g.sort_values("year").set_index("year").chl_median_ugl for l, g in ts.groupby("lagoslakeid")}
pairs = pd.read_csv("pairs.tsv", sep="\t")
def ind(l, s, e, gap=0):
    y = np.log(S[l].loc[s:e - gap].values.astype(float)); n = len(y); t = np.arange(n); y = y - np.polyval(np.polyfit(t, y, 1), t)
    w = max(6, n // 2); v = [np.var(y[i:i + w], ddof=1) for i in range(n - w + 1)]
    a = [np.corrcoef(y[i:i + w - 1], y[i + 1:i + w])[0, 1] for i in range(n - w + 1)]
    f = lambda z: kendalltau(np.arange(len(z)), z)[0] if np.nanstd(z) > 0 else 0.0
    return f(v), f(np.nan_to_num(a))
def scores(gap):
    out = []
    for r in pairs.itertuples():
        if r.end - gap - r.start + 1 < 12: out.append((np.nan,) * 4); continue
        out.append(ind(r.case, r.start, r.end, gap) + ind(r.control, r.start, r.end, gap))
    return np.array(out)
def pair_auc(x, y_, idx): a, b = x[idx], y_[idx]; return float(np.mean((a > b) + 0.5 * (a == b)))
res = {"n_pairs": len(pairs)}
if len(pairs) < 300:
    res["LABEL"] = "INSUFFICIENT-DATA"; print("RESULT_JSON", json.dumps(res)); open("results.json", "w").write(json.dumps(res, indent=1)); raise SystemExit
M = scores(0); ok = ~np.isnan(M[:, 0]); M = M[ok]; n = len(M); res["n_pairs_scored"] = int(n)
for k, name in enumerate(["var_tau", "ac1_tau"]):
    c, d = M[:, k], M[:, 2 + k]; boot = [pair_auc(c, d, rng.integers(0, n, n)) for _ in range(2000)]
    sw = [float(np.mean(np.where(rng.random(n) < 0.5, c > d, d > c) + 0.5 * (c == d))) for _ in range(200)]
    res[name] = dict(paired_AUROC=pair_auc(c, d, np.arange(n)), ci975=[float(np.percentile(boot, 1.25)), float(np.percentile(boot, 98.75))], mean_case=float(c.mean()), mean_control=float(d.mean()), label_swap_null_mean=float(np.mean(sw)), pass_=bool(np.percentile(boot, 1.25) > 0.55))
res["G1"] = dict(swap_null_means={k: res[k]["label_swap_null_mean"] for k in ["var_tau", "ac1_tau"]}, pass_=bool(all(0.48 <= res[k]["label_swap_null_mean"] <= 0.52 for k in ["var_tau", "ac1_tau"])))
sens = {}
for gap in (2, 4):
    Mg = scores(gap); Mg = Mg[~np.isnan(Mg[:, 0])]; sens[f"gap{gap}"] = dict(n=int(len(Mg)), var_tau_AUROC=pair_auc(Mg[:, 0], Mg[:, 2], np.arange(len(Mg))), ac1_tau_AUROC=pair_auc(Mg[:, 1], Mg[:, 3], np.arange(len(Mg))))
res["reported_only_lead_gap_sensitivity"] = sens
res["LABEL"] = "INVALID" if not res["G1"]["pass_"] else ("WARNING-SIGNAL-DETECTED" if (res["var_tau"]["pass_"] or res["ac1_tau"]["pass_"]) else "HONEST NEGATIVE")
print("RESULT_JSON", json.dumps(res, default=float)); open("results.json", "w").write(json.dumps(res, default=float, indent=1))
