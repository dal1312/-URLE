#!/usr/bin/env python3
from pathlib import Path
import csv

root = Path(__file__).resolve().parents[2]
path = root / "04_GCP_GEOREF/GCP_point_matching_v2_7.csv"

with path.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

print("GCP rows:", len(rows))

sheets = {}
for row in rows:
    sheet = row.get("sheet_id", "UNKNOWN")
    sheets.setdefault(sheet, []).append(row)

for sheet, items in sorted(sheets.items()):
    verified = 0
    for row in items:
        if row.get("decision") == "KEEP" and row.get("target_easting_epsg25832") and row.get("target_northing_epsg25832"):
            verified += 1
    state = "READY" if verified >= 8 else "NEEDS_MATCHING"
    print(sheet, "total=", len(items), "keep_verified=", verified, "state=", state)
