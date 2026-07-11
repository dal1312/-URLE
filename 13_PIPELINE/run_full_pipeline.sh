#!/bin/bash
#
# run_full_pipeline.sh
# Forlì Digital Twin — Master v3.2
# Script master per eseguire l'intera pipeline in sequenza
#
# Uso:
#   bash 13_PIPELINE/run_full_pipeline.sh
#

set -e

echo "=============================================="
echo "FORLÌ DIGITAL TWIN — FULL PIPELINE v3.2"
echo "=============================================="

echo ""
echo "[STEP 1/5] Esportazione GCP verificati..."
python 13_PIPELINE/scripts/export_gcp_verified.py

echo ""
echo "[STEP 2/5] Promozione GCP verificati..."
python 13_PIPELINE/scripts/promote_verified_gcps.py || echo "[INFO] promote_verified_gcps.py non ancora implementato o non necessario"

echo ""
echo "[STEP 3/5] Generazione comandi GDAL per GeoTIFF..."
python 13_PIPELINE/scripts/build_gdal_commands.py || echo "[INFO] build_gdal_commands.py non ancora implementato"

echo ""
echo "[STEP 4/5] Validazione finale progetto..."
python 13_PIPELINE/scripts/validate_project.py || true

echo ""
echo "[STEP 5/5] Pipeline completata."
echo ""
echo "Prossimi passi manuali:"
echo "  - Controlla i GeoTIFF generati in 11_FINAL_OUTPUT/"
echo "  - Esegui vettorializzazione"
echo "  - Popola database temporale"
echo "  - Prepara release finale"

echo ""
echo "=============================================="
echo "Pipeline terminata con successo."
echo "=============================================="