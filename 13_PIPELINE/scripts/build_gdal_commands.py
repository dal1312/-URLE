#!/usr/bin/env python3
from pathlib import Path
import csv
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[2]
GCP_CSV = ROOT / "04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv"
OUT = ROOT / "13_PIPELINE/scripts/gdal_georef_final_commands.sh"

sheet_to_file = {
    "FO004_042": "02_RASTER_STORICI/CT_FO004_042.jpg",
    "FO004_043": "02_RASTER_STORICI/01CT_FO004_043.jpg",
    "FO004_044": "02_RASTER_STORICI/CT_FO004_044.jpg",
    "FO004_045": "02_RASTER_STORICI/CT_FO004_045.jpg",
}

if not GCP_CSV.exists():
    print(f"Manca {GCP_CSV}")
    raise SystemExit(1)

rows_by_sheet = defaultdict(list)
with GCP_CSV.open(encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        if r.get("decision") != "KEEP":
            continue
        if not r.get("target_easting_epsg25832") or not r.get("target_northing_epsg25832"):
            continue
        rows_by_sheet[r["sheet_id"]].append(r)

cmds = ["#!/bin/sh", "set -e", "mkdir -p 11_FINAL_OUTPUT/geotiff_final"]
for sheet, rows in rows_by_sheet.items():
    if len(rows) < 8:
        print(f"[WARN] {sheet}: solo {len(rows)} GCP validi. Minimo consigliato: 8.")
        continue
    src = sheet_to_file.get(sheet)
    tmp = f"11_FINAL_OUTPUT/geotiff_final/{sheet}_with_gcps.tif"
    out = f"11_FINAL_OUTPUT/geotiff_final/{sheet}_FINAL_EPSG25832.tif"
    gcps = []
    for r in rows:
        gcps.append(
            f'-gcp {r["source_x"]} {r["source_y"]} '
            f'{r["target_easting_epsg25832"]} {r["target_northing_epsg25832"]}'
        )
    cmds.append(
        f'gdal_translate -of GTiff -a_srs EPSG:25832 {" ".join(gcps)} "{src}" "{tmp}"'
    )
    cmds.append(
        f'gdalwarp -r cubic -tps -t_srs EPSG:25832 -co COMPRESS=DEFLATE -co TILED=YES "{tmp}" "{out}"'
    )

OUT.write_text("\n".join(cmds) + "\n", encoding="utf-8")
print(f"Creato: {OUT}")
