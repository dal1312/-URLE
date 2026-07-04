#!/usr/bin/env python3
from pathlib import Path
import json, csv, sys

ROOT = Path(__file__).resolve().parents[2]

checks = []

def check(path, label):
    p = ROOT / path
    ok = p.exists()
    checks.append((label, path, ok))
    return ok

check("12_MANIFEST/master_manifest_v3_0.json", "Master manifest")
check("12_MANIFEST/master_inventory_v3_0.csv", "Master inventory")
check("03_CTR_MODERNA/CTR_7tiles_EPSG25832.vrt", "CTR VRT")
check("03_CTR_MODERNA/CTR_tile_index_EPSG25832.geojson", "CTR tile index")
check("04_GCP_GEOREF/GCP_point_matching_v2_7.csv", "GCP matching CSV")
check("06_TEMPORAL_MODEL/temporal_features_schema.csv", "Temporal schema")
check("08_WEB_APP/index.html", "Web workbench")

print("FORLI DIGITAL TWIN — VALIDATION")
failed = 0
for label, path, ok in checks:
    print(f"[{'OK' if ok else 'MISSING'}] {label}: {path}")
    if not ok:
        failed += 1

gcp = ROOT / "04_GCP_GEOREF/GCP_point_matching_v2_7.csv"
if gcp.exists():
    with gcp.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    keep = [r for r in rows if r.get("decision") == "KEEP" and r.get("target_easting_epsg25832") and r.get("target_northing_epsg25832")]
    print(f"GCP rows: {len(rows)}")
    print(f"Verified KEEP GCP: {len(keep)}")
    if len(keep) < 32:
        print("[INFO] GCP finali incompleti: procedere con matching point-by-point.")

sys.exit(1 if failed else 0)
