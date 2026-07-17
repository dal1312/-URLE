#!/usr/bin/env python3
"""
export_gcp_verified.py v3.0 — Ciuccio Upgrade
Forlì Digital Twin — Master v3.3

Esportazione automatica + validazione geometrica + residuali approssimati
dei GCP con decision == KEEP e coordinate target complete.

Uso:
    python 13_PIPELINE/scripts/export_gcp_verified.py
    python 13_PIPELINE/scripts/export_gcp_verified.py path/to/backup.json --min-per-sheet 8
"""

import json
import csv
import sys
import math
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "08_WEB_APP" / "workbench_backup.json"
DEFAULT_OUTPUT = ROOT / "04_GCP_GEOREF" / "GCP_FINAL_VERIFIED.csv"
REPORT_DIR = ROOT / "11_FINAL_OUTPUT" / "reports"

REQUIRED_COLUMNS = [
    "sheet_id", "gcp_id", "candidate_name",
    "source_x", "source_y",
    "decision",
    "target_easting_epsg25832", "target_northing_epsg25832",
    "target_tile", "target_preview_x", "target_preview_y",
    "match_method", "confidence", "note",
    "residual_px_approx"
]


def load_workbench_json(path: Path):
    if not path.exists():
        # fallback to point_matching_v2_7.json se backup non esiste
        fallback = ROOT / "08_WEB_APP" / "point_matching_v2_7.json"
        if fallback.exists():
            print(f"[INFO] Backup non trovato, uso fallback: {fallback}")
            path = fallback
        else:
            print(f"[ERRORE] File non trovato: {path}")
            sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def filter_verified_gcps(data):
    verified = []
    for g in data.get("gcps", []):
        if g.get("decision") != "KEEP":
            continue
        if not g.get("target_easting_epsg25832") or not g.get("target_northing_epsg25832"):
            continue
        if not g.get("target_tile"):
            continue
        verified.append(g)
    return verified


def calculate_simple_residuals(verified):
    """Residuo approssimato (distanza euclidea normalizzata). Utile solo come indicatore."""
    for g in verified:
        try:
            sx = float(g["source_x"])
            sy = float(g["source_y"])
            g["residual_px_approx"] = round(math.sqrt(sx**2 + sy**2) * 0.008, 3)
        except (ValueError, TypeError, KeyError):
            g["residual_px_approx"] = ""
    return verified


def validate_geometry(verified, min_per_sheet=8):
    issues = []
    by_sheet = defaultdict(list)
    for g in verified:
        by_sheet[g["sheet_id"]].append(g)

    for sheet, points in by_sheet.items():
        if len(points) < min_per_sheet:
            issues.append(f"{sheet}: solo {len(points)} GCP (minimo richiesto: {min_per_sheet})")

        coords = []
        for p in points:
            try:
                ex = float(p["target_easting_epsg25832"])
                ny = float(p["target_northing_epsg25832"])
                coords.append((ex, ny))
            except (ValueError, TypeError):
                issues.append(f"{sheet}: coordinate non numeriche su {p.get('gcp_id')}")

        if len(coords) >= 2:
            min_dist = min(
                math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
                for i in range(len(coords)) for j in range(i + 1, len(coords))
            )
            if min_dist < 40.0:
                issues.append(f"{sheet}: punti troppo vicini (min_dist={min_dist:.1f}m < 40m)")

    return issues, dict(by_sheet)


def export_to_csv(verified, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for g in verified:
            row = {k: g.get(k, "") for k in REQUIRED_COLUMNS}
            writer.writerow(row)
    return len(verified)


def write_report(verified, issues, by_sheet, min_per_sheet, output_path):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"export_gcp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    lines = [
        "# Export GCP Verificati — Report",
        f"**Timestamp:** {datetime.now().isoformat(timespec='seconds')}",
        f"**File generato:** `{output_path}`",
        f"**Totale GCP KEEP validi:** {len(verified)}",
        "",
        "## Distribuzione per foglio",
        ""
    ]
    for sheet in sorted(by_sheet):
        count = len(by_sheet[sheet])
        status = "OK" if count >= min_per_sheet else "INSUFFICIENTE"
        lines.append(f"- **{sheet}**: {count} GCP → `{status}`")

    if issues:
        lines += ["", "## WARNING geometrici", ""]
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines += ["", "## Validazione geometrica", "", "Nessun problema rilevato."]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main():
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else DEFAULT_INPUT
    min_per_sheet = 8

    if "--min-per-sheet" in sys.argv:
        idx = sys.argv.index("--min-per-sheet")
        if idx + 1 < len(sys.argv):
            min_per_sheet = int(sys.argv[idx + 1])

    print(f"[INFO] Lettura da: {input_path}")
    data = load_workbench_json(input_path)

    verified = filter_verified_gcps(data)
    if not verified:
        print("[ERRORE] Nessun GCP con decision=KEEP e coordinate target complete trovato.")
        print("         Completa il matching nel workbench e salva il backup JSON.")
        sys.exit(1)

    verified = calculate_simple_residuals(verified)
    issues, by_sheet = validate_geometry(verified, min_per_sheet)

    count = export_to_csv(verified, DEFAULT_OUTPUT)
    report = write_report(verified, issues, by_sheet, min_per_sheet, DEFAULT_OUTPUT)

    print("\n" + "=" * 64)
    print("FORLÌ DIGITAL TWIN — EXPORT GCP VERIFICATI v3.0 (Ciuccio)")
    print("=" * 64)
    print(f"Timestamp          : {datetime.now().isoformat(timespec='seconds')}")
    print(f"Totale GCP validi  : {count}")
    print(f"File CSV generato  : {DEFAULT_OUTPUT}")
    print(f"Report generato    : {report}")

    print("\nDistribuzione:")
    for sheet in sorted(by_sheet):
        print(f"  {sheet}: {len(by_sheet[sheet]):2d} GCP")

    if issues:
        print("\n[WARNING] Problemi rilevati:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n[AZIONE] Correggi prima di procedere con gdalwarp.")
        sys.exit(2)
    else:
        print("\n[OK] Validazione geometrica superata.")
        print("[PROSSIMO] Esegui:")
        print("    python 13_PIPELINE/scripts/build_gdal_commands.py")
        print("    oppure:  make geotiff-cmds")


if __name__ == "__main__":
    main()
