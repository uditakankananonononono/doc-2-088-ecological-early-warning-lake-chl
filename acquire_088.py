"""DOC-2-088: download LAGOS-US lake CHL time series and breakpoint table (Zenodo 10926306, CC-BY-4.0). Writes chl_ts.csv, bpanom.csv, DATA_HASHES.tsv (md5 checked against Zenodo's published md5)."""
import hashlib, requests, json
rec = requests.get("https://zenodo.org/api/records/10926306", timeout=60).json(); md5s = {f["key"]: f["checksum"].split(":")[1] for f in rec["files"]}
out = ["file\tmd5\tzenodo_md5\tbytes"]
for key, name in [("cp_chl_climate_timeseries.csv", "chl_ts.csv"), ("cp_chl_bpanom.csv", "bpanom.csv")]:
    h = hashlib.md5(); n = 0
    with requests.get(f"https://zenodo.org/records/10926306/files/{key}", stream=True, timeout=300) as r, open(name, "wb") as f:
        r.raise_for_status()
        for ch in r.iter_content(1 << 20): f.write(ch); h.update(ch); n += len(ch)
    assert h.hexdigest() == md5s[key], f"md5 mismatch {key}"; out.append(f"{name}\t{h.hexdigest()}\t{md5s[key]}\t{n}")
open("DATA_HASHES.tsv", "w").write("\n".join(out) + "\n"); print("ACQ_DONE")
