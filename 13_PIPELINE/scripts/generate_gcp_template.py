#!/usr/bin/env python3
"""
generate_gcp_template.py v1.0 — Ciuccio
Genera un CSV template pronto per il matching finale (colonne target vuote).
"""

import csv
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "04_GCP_GEOREF" / "GCP_point_matching_v2_7.csv"
OUT = ROOT / "04_GCP_GEOREF" / "GCP_TEMPLATE_FOR_KEEP.csv"

FIELDS = [
    "sheet_id", "gcp_id", "candidate_name",
    "source_x", "source_y",
    "decision",
    "target_easting_epsg25832", "target_northing_epsg25832",
    "target_tile", "target_preview_x", "target_preview_y",
    "match_method", "confidence", "note"
]


def main():
    if not SRC.exists():
        print(f"[ERRORE] {SRC} non trovato")
        raise SystemExit(1)

    with SRC.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            out_row = {k: r.get(k, "") for k in FIELDS}
            # Lascia decision e target vuoti o con valore di default utile
            if out_row["decision"] in ("", None):
                out_row["decision"] = "REVIEW"
            out_row["target_easting_epsg25832"] = ""
            out_row["target_northing_epsg25832"] = ""
            out_row["target_tile"] = ""
            out_row["target_preview_x"] = ""
            out_row["target_preview_y"] = ""
            writer.writerow(out_row)

    print(f"[OK] Template generato: {OUT}")
    print(f"     Righe: {len(rows)}")
    print(f"     Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print()
    print("Istruzioni:")
    print("  1. Apri 08_WEB_APP/workbench_v3_2.html")
    print("  2. Assegna i target sulla CTR e metti decision=KEEP")
    print("  3. Esporta / salva backup JSON")
    print("  4. Esegui export_gcp_verified.py")


if __name__ == "__main__":
    main()
