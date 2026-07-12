#!/usr/bin/env python3
"""
vectorize_historical.py
Forlì Digital Twin — Master v3.2
Script per vettorializzazione semi-automatica dei raster storici

Layer generati:
- mura
- strade
- edifici
- chiese
- conventi
- palazzi
- torri
- canali
- orti
- vigne
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEOTIFF_DIR = ROOT / "11_FINAL_OUTPUT" / "geotiff_final"
OUTPUT_DIR = ROOT / "11_FINAL_OUTPUT" / "vector"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=== VETTORIALIZZAZIONE STORICA FORLÌ ===\n")

# Placeholder per layer
layers = [
    "mura", "strade", "edifici", "chiese", "conventi",
    "palazzi", "torri", "canali", "orti", "vigne"
]

for layer in layers:
    gpkg = OUTPUT_DIR / f"{layer}.gpkg"
    # Qui in futuro: gdal_polygonize o rasterio + shapely
    # Per ora creiamo file placeholder
    with open(gpkg, "w") as f:
        f.write(f"# Placeholder GeoPackage per layer: {layer}\n")
        f.write("# Esegui manualmente in QGIS o usa script avanzato\n")
    print(f"[OK] Placeholder creato: {gpkg.name}")

print("\n[INFO] Per vettorializzazione reale usa:")
print("  - QGIS: Raster > Conversion > Polygonize")
print("  - OGR: gdal_polygonize.py")
print("  - Python avanzato: rasterio + shapely + fiona")

print("\n[PROSSIMO] Apri i GeoTIFF in QGIS e traccia i layer manualmente.")
print(f"Output directory: {OUTPUT_DIR}")