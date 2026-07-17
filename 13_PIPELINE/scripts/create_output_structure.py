#!/usr/bin/env python3
"""
create_output_structure.py v1.0 — Ciuccio
Crea l'intera struttura di output del progetto Forlì Digital Twin v3.3
"""

from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

DIRS = [
    "11_FINAL_OUTPUT/geotiff_final",
    "11_FINAL_OUTPUT/vector",
    "11_FINAL_OUTPUT/residual_maps",
    "11_FINAL_OUTPUT/reports",
    "11_FINAL_OUTPUT/logs",
    "04_GCP_GEOREF",
    "16_CIUCCIO_UPGRADE",
    "docs",
]


def main():
    print(f"[INFO] Creazione struttura output — {datetime.now().isoformat(timespec='seconds')}")
    created = 0
    for d in DIRS:
        p = ROOT / d
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            print(f"  + {d}")
            created += 1
        else:
            print(f"  = {d} (già presente)")

    # Placeholder files
    (ROOT / "11_FINAL_OUTPUT" / "README.md").write_text(
        "# 11_FINAL_OUTPUT\n\n"
        "Cartella generata automaticamente da create_output_structure.py (Ciuccio v3.3)\n\n"
        "- geotiff_final/   → GeoTIFF storici georeferenziati EPSG:25832\n"
        "- vector/          → Layer vettoriali storici\n"
        "- residual_maps/   → Mappe residuali GCP\n"
        "- reports/         → Report di validazione e export\n"
        "- logs/            → Log di pipeline\n",
        encoding="utf-8"
    )

    print(f"\n[OK] Struttura pronta. Directory create: {created}")


if __name__ == "__main__":
    main()
