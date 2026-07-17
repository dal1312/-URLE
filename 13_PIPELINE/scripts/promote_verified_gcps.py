#!/usr/bin/env python3
"""
promote_verified_gcps.py v3.0 — Ciuccio Upgrade
Forlì Digital Twin — Master v3.3

Promuove i GCP con decision=KEEP e coordinate complete
dal CSV di matching (o dal JSON) verso GCP_FINAL_VERIFIED.csv.
Esegue anche un controllo minimo di completezza per foglio.
"""

import csv
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
SRC_CSV = ROOT / "04_GCP_GEOREF" / "GCP_point_matching_v2_7.csv"
OUT_CSV = ROOT / "04_GCP_GEOREF" / "GCP_FINAL_VERIFIED.csv"
MIN_PER_SHEET = 8
EXPECTED_SHEETS = ["FO004_042", "FO004_043", "FO004_044", "FO004_045"]


def main():
    if not SRC_CSV.exists():
        print(f"[ERRORE] File sorgente mancante: {SRC_CSV}")
        sys.exit(1)

    with SRC_CSV.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)

    valid = []
    for row in rows:
        if row.get("decision") != "KEEP":
            continue
        if not row.get("target_easting_epsg25832") or not row.get("target_northing_epsg25832"):
            continue
        if not row.get("target_tile"):
            continue
        valid.append(row)

    by_sheet = defaultdict(list)
    for row in valid:
        by_sheet[row["sheet_id"]].append(row)

    print("=" * 60)
    print("PROMOTE VERIFIED GCPs v3.0")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print()

    not_ready = []
    for sheet in EXPECTED_SHEETS:
        count = len(by_sheet.get(sheet, []))
        status = "OK" if count >= MIN_PER_SHEET else "INSUFFICIENTE"
        print(f"  {sheet}: {count:2d} GCP  [{status}]")
        if count < MIN_PER_SHEET:
            not_ready.append(sheet)

    if not_ready:
        print()
        print(f"[ERRORE] Fogli non pronti (minimo {MIN_PER_SHEET} GCP KEEP): {', '.join(not_ready)}")
        print("         Completa il matching nel workbench prima di promuovere.")
        sys.exit(2)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(valid)

    print()
    print(f"[OK] Generato: {OUT_CSV.relative_to(ROOT)}")
    print(f"     Righe verificate: {len(valid)}")
    print()
    print("[PROSSIMO] Esegui:")
    print("    python 13_PIPELINE/scripts/build_gdal_commands.py")


if __name__ == "__main__":
    main()
