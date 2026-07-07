#!/usr/bin/env python3
from pathlib import Path
import csv

root = Path(__file__).resolve().parents[2]
src = root / "04_GCP_GEOREF/GCP_point_matching_v2_7.csv"
out = root / "04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv"

with src.open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
    fields = f.fieldnames

valid = []
for row in rows:
    if row.get("decision") != "KEEP":
        continue
    if not row.get("target_easting_epsg25832") or not row.get("target_northing_epsg25832"):
        continue
    if not row.get("target_tile"):
        continue
    valid.append(row)

by_sheet = {}
for row in valid:
    by_sheet.setdefault(row["sheet_id"], []).append(row)

expected = ["FO004_042", "FO004_043", "FO004_044", "FO004_045"]
not_ready = [sheet for sheet in expected if len(by_sheet.get(sheet, [])) < 8]

for sheet in expected:
    print(sheet, "verified=", len(by_sheet.get(sheet, [])))

if not_ready:
    print("NOT READY:", ", ".join(not_ready))
    print("GCP_FINAL_VERIFIED.csv not generated")
    raise SystemExit(2)

with out.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(valid)

print("Generated:", out.relative_to(root))
print("Verified rows:", len(valid))
