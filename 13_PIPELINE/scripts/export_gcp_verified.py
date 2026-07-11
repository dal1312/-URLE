#!/usr/bin/env python3
"""
export_gcp_verified.py v2.0
Forlì Digital Twin — Master v3.2
Esportazione automatica + validazione geometrica GCP verificati

Uso:
    python export_gcp_verified.py
    python export_gcp_verified.py backup.json --min-per-sheet 6
"""

import json
import csv
import sys
import math
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "08_WEB_APP" / "workbench_backup.json"
DEFAULT_OUTPUT = ROOT / "04_GCP_GEOREF" / "GCP_FINAL_VERIFIED.csv"

REQUIRED_COLUMNS = [
    "sheet_id", "gcp_id", "candidate_name",
    "source_x", "source_y",
    "decision",
    "target_easting_epsg25832", "target_northing_epsg25832",
    "target_tile", "target_preview_x", "target_preview_y",
    "match_method", "confidence", "note"
]


def load_workbench_json(path: Path):
    if not path.exists():
        print(f"[ERRORE] File non trovato: {path}")
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_verified_gcps(data):
    return [g for g in data.get("gcps", [])
            if g.get("decision") == "KEEP"
            and g.get("target_easting_epsg25832")
            and g.get("target_northing_epsg25832")]


def calculate_simple_residuals(verified):
    """Calcolo residui approssimati (solo per report, non preciso senza matrice completa)."""
    for g in verified:
        try:
            sx, sy = float(g["source_x"]), float(g["source_y"])
            g["residual_px_approx"] = round(math.sqrt(sx**2 + sy**2) * 0.01, 2)
        except:
            g["residual_px_approx"] = ""
    return verified


def validate_geometry(verified, min_per_sheet=6):
    issues = []
    by_sheet = {}
    for g in verified:
        sid = g["sheet_id"]
        by_sheet.setdefault(sid, []).append(g)

    for sheet, points in by_sheet.items():
        if len(points) < min_per_sheet:
            issues.append(f"{sheet}: solo {len(points)} GCP (minimo consigliato: {min_per_sheet})")

        coords = []
        for p in points:
            try:
                ex = float(p["target_easting_epsg25832"])
                ny = float(p["target_northing_epsg25832"])
                coords.append((ex, ny))
            except:
                pass

        if len(coords) >= 2:
            min_dist = min(
                math.hypot(coords[i][0]-coords[j][0], coords[i][1]-coords[j][1])
                for i in range(len(coords)) for j in range(i+1, len(coords))
            )
            if min_dist < 50:
                issues.append(f"{sheet}: punti troppo vicini (<50m) — possibile clustering")

    return issues, by_sheet


def export_to_csv(verified, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for g in verified:
            row = {k: g.get(k, "") for k in REQUIRED_COLUMNS}
            writer.writerow(row)
    return len(verified)


def print_report(verified, issues, by_sheet, min_per_sheet):
    print("\n" + "="*60)
    print("FORLÌ DIGITAL TWIN — EXPORT GCP VERIFICATI v2.0")
    print("="*60)
    print(f"Timestamp: {datetime.now().isoformat(timespec='seconds')}")
    print(f"Totale GCP verificati: {len(verified)}")

    print("\nDistribuzione per foglio:")
    for sheet in sorted(by_sheet):
        count = len(by_sheet[sheet])
        status = "OK" if count >= min_per_sheet else "INSUFFICIENTE"
        print(f"  {sheet}: {count:2d} GCP  [{status}]")

    if issues:
        print("\n[WARNING] Problemi geometrici rilevati:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n[OK] Validazione geometrica superata.")

    print("\nFile generato:")
    print(f"  {DEFAULT_OUTPUT}")


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else DEFAULT_INPUT
    min_per_sheet = 6

    if "--min-per-sheet" in sys.argv:
        idx = sys.argv.index("--min-per-sheet")
        if idx + 1 < len(sys.argv):
            min_per_sheet = int(sys.argv[idx + 1])

    print(f"[INFO] Lettura da: {input_path}")
    data = load_workbench_json(input_path)

    verified = filter_verified_gcps(data)
    if not verified:
        print("[ERRORE] Nessun GCP verificato trovato.")
        sys.exit(1)

    verified = calculate_simple_residuals(verified)
    issues, by_sheet = validate_geometry(verified, min_per_sheet)

    count = export_to_csv(verified, DEFAULT_OUTPUT)
    print_report(verified, issues, by_sheet, min_per_sheet)

    if issues:
        print("\n[AZIONE] Correggi i problemi sopra prima di procedere con la pipeline.")
    else:
        print("\n[PROSSIMO] Esegui:")
        print("    python 13_PIPELINE/scripts/promote_verified_gcps.py")

if __name__ == "__main__":
    main()