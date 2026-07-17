#!/bin/bash
#
# run_full_pipeline.sh v3.0 — Ciuccio Upgrade
# Forlì Digital Twin — Master v3.3
#
# Esegue l'intera pipeline in sequenza con fail-fast e logging.
#

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LOG_DIR="11_FINAL_OUTPUT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/pipeline_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG_FILE") 2>&1

echo "=============================================="
echo "FORLÌ DIGITAL TWIN — FULL PIPELINE v3.3"
echo "Ciuccio Upgrade"
echo "Timestamp: $(date -Iseconds)"
echo "Log: $LOG_FILE"
echo "=============================================="
echo ""

echo "[STEP 0/6] Creazione struttura output..."
python 13_PIPELINE/scripts/create_output_structure.py

echo ""
echo "[STEP 1/6] Validazione progetto..."
python 13_PIPELINE/scripts/validate_project.py || true

echo ""
echo "[STEP 2/6] Esportazione / promozione GCP verificati..."
if python 13_PIPELINE/scripts/export_gcp_verified.py; then
    echo "[OK] export_gcp_verified.py completato"
else
    echo "[INFO] export fallito — provo promote_verified_gcps.py"
    python 13_PIPELINE/scripts/promote_verified_gcps.py || {
        echo "[ERRORE] Nessun GCP KEEP valido trovato."
        echo "         Completa il matching nel workbench e riprova."
        exit 2
    }
fi

echo ""
echo "[STEP 3/6] Generazione comandi GDAL..."
python 13_PIPELINE/scripts/build_gdal_commands.py

echo ""
echo "[STEP 4/6] Esecuzione georeferenziazione (se script generato)..."
if [[ -x 13_PIPELINE/scripts/gdal_georef_final_commands.sh ]]; then
    bash 13_PIPELINE/scripts/gdal_georef_final_commands.sh
else
    echo "[SKIP] Script GDAL non eseguibile o non generato"
fi

echo ""
echo "[STEP 5/6] Validazione finale..."
python 13_PIPELINE/scripts/validate_project.py || true

echo ""
echo "[STEP 6/6] Pipeline terminata."
echo ""
echo "Prossimi passi manuali / opzionali:"
echo "  - Controlla i GeoTIFF in 11_FINAL_OUTPUT/geotiff_final/"
echo "  - Esegui vettorializzazione (vectorize_historical.py)"
echo "  - Popola database temporale"
echo "  - Prepara release finale"
echo ""
echo "=============================================="
echo "Pipeline v3.3 completata."
echo "Log salvato in: $LOG_FILE"
echo "=============================================="
