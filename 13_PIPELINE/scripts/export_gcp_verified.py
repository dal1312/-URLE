#!/usr/bin/env python3
"""
export_gcp_verified.py
Forlì Digital Twin — Master v3.2
Esportazione automatica GCP verificati dal Workbench v3.2

Uso:
    python export_gcp_verified.py                    # usa default
    python export_gcp_verified.py backup.json        # input custom
    python export_gcp_verified.py backup.json --output 04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv
"""

import json
import csv
import sys
from pathlib import Path
from datetime import datetime

# === CONFIGURAZIONE ===
ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "08_WEB_APP" / "workbench_backup.json"   # cambia se usi nome diverso
DEFAULT_OUTPUT = ROOT / "04_GCP_GEOREF" / "GCP_FINAL_VERIFIED.csv"

REQUIRED_COLUMNS = [
    "sheet_id", "gcp_id", "candidate_name",
    "source_x", "source_y",
    "decision",
    "target_easting_epsg25832", "target_northing_epsg25832",
    "target_tile", "target_preview_x", "target_preview_y",
    "match_method", "confidence", "note"
]


def load_workbench_json(path: Path) -> dict:
    if not path.exists():
        print(f"[ERRORE] File non trovato: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def filter_verified_gcps(data: dict) -> list:
    gcps = data.get("gcps", [])
    verified = []
    for g in gcps:
        if (g.get("decision") == "KEEP" and
            g.get("target_easting_epsg25832") and
            g.get("target_northing_epsg25832")):
            verified.append(g)
    return verified


def export_to_csv(verified: list, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for g in verified:
            row = {k: g.get(k, "") for k in REQUIRED_COLUMNS}
            writer.writerow(row)

    print(f"[OK] Esportati {len(verified)} GCP verificati → {output_path}")


def print_summary(verified: list):
    print("\n=== RIEPILOGO ESPORTAZIONE ===")
    print(f"Data/ora: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Totale GCP verificati (KEEP + coordinate): {len(verified)}")

    by_sheet = {}
    for g in verified:
        sid = g["sheet_id"]
        by_sheet.setdefault(sid, 0)
        by_sheet[sid] += 1

    print("\nPer foglio:")
    for sheet in sorted(by_sheet):
        print(f"  {sheet}: {by_sheet[sheet]} GCP")

    if len(verified) < 24:
        print("\n[ATTENZIONE] Meno di 24 GCP verificati. Si consiglia almeno 6-8 per foglio.")
    else:
        print("\n[OK] Quantità sufficiente per procedere con la pipeline.")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = DEFAULT_OUTPUT

    # Supporto --output
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_path = Path(sys.argv[idx + 1])

    print(f"[INFO] Lettura da: {input_path}")
    data = load_workbench_json(input_path)

    verified = filter_verified_gcps(data)
    if not verified:
        print("[ERRORE] Nessun GCP con decision=KEEP e coordinate target trovate.")
        print("         Completa il matching nel Workbench e usa 'Backup JSON'.")
        sys.exit(1)

    export_to_csv(verified, output_path)
    print_summary(verified)

    print("\n[PROSSIMO STEP] Esegui:")
    print("    python 13_PIPELINE/scripts/promote_verified_gcps.py")
    print("    python 13_PIPELINE/scripts/build_gdal_commands.py")


if __name__ == "__main__":
    main()