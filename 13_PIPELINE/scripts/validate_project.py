#!/usr/bin/env python3
"""
validate_project.py v3.0 — Ciuccio Upgrade
Forlì Digital Twin — Master v3.3

Validazione completa di struttura, file core e stato GCP.
"""

from pathlib import Path
import json
import csv
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

CHECKS = [
    ("12_MANIFEST/master_manifest_v3_0.json", "Master manifest v3.0"),
    ("12_MANIFEST/master_inventory_v3_0.csv", "Master inventory"),
    ("03_CTR_MODERNA/CTR_7tiles_EPSG25832.vrt", "CTR VRT"),
    ("03_CTR_MODERNA/CTR_tile_index_EPSG25832.geojson", "CTR tile index"),
    ("04_GCP_GEOREF/GCP_point_matching_v2_7.csv", "GCP matching CSV"),
    ("06_TEMPORAL_MODEL/temporal_features_schema.csv", "Temporal schema"),
    ("08_WEB_APP/index.html", "Web index"),
    ("08_WEB_APP/workbench_v3_2.html", "Workbench v3.2"),
    ("08_WEB_APP/point_matching_v2_7.json", "Point matching JSON"),
    ("13_PIPELINE/run_full_pipeline.sh", "Full pipeline script"),
]


def main():
    print("=" * 64)
    print("FORLÌ DIGITAL TWIN — VALIDATION v3.0 (Ciuccio)")
    print(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 64)

    failed = 0
    for path, label in CHECKS:
        p = ROOT / path
        ok = p.exists()
        status = "OK     " if ok else "MISSING"
        print(f"[{status}] {label}: {path}")
        if not ok:
            failed += 1

    # GCP analysis
    print()
    gcp_csv = ROOT / "04_GCP_GEOREF" / "GCP_point_matching_v2_7.csv"
    if gcp_csv.exists():
        with gcp_csv.open(encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        keep = [
            r for r in rows
            if r.get("decision") == "KEEP"
            and r.get("target_easting_epsg25832")
            and r.get("target_northing_epsg25832")
        ]
        print(f"GCP totali nel matching CSV : {len(rows)}")
        print(f"GCP KEEP con coordinate     : {len(keep)}")

        by_sheet = {}
        for r in keep:
            by_sheet.setdefault(r["sheet_id"], 0)
            by_sheet[r["sheet_id"]] += 1

        print("Distribuzione KEEP per foglio:")
        for sheet in sorted(by_sheet):
            print(f"  {sheet}: {by_sheet[sheet]}")

        if len(keep) < 32:
            print("[INFO] GCP finali incompleti — procedere con matching point-by-point nel workbench.")
    else:
        print("[MISSING] GCP matching CSV non trovato")

    # Final verified
    final = ROOT / "04_GCP_GEOREF" / "GCP_FINAL_VERIFIED.csv"
    if final.exists():
        with final.open(encoding="utf-8-sig") as f:
            final_rows = list(csv.DictReader(f))
        print(f"\nGCP_FINAL_VERIFIED.csv     : {len(final_rows)} righe")
    else:
        print("\nGCP_FINAL_VERIFIED.csv     : non ancora generato")

    print()
    if failed:
        print(f"[RISULTATO] {failed} file core mancanti.")
        sys.exit(1)
    else:
        print("[RISULTATO] Struttura core OK.")
        sys.exit(0)


if __name__ == "__main__":
    main()
