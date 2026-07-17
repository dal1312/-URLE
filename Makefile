# Makefile — Forlì Digital Twin Master v3.3 (Ciuccio Upgrade)
# Dott. Ing. Massimo Valtieri

.PHONY: all structure export-gcp promote-gcp geotiff-cmds pipeline validate residuals template clean help

all: structure pipeline

structure:
	python 13_PIPELINE/scripts/create_output_structure.py

export-gcp:
	python 13_PIPELINE/scripts/export_gcp_verified.py

promote-gcp:
	python 13_PIPELINE/scripts/promote_verified_gcps.py

geotiff-cmds:
	python 13_PIPELINE/scripts/build_gdal_commands.py

template:
	python 13_PIPELINE/scripts/generate_gcp_template.py

validate:
	python 13_PIPELINE/scripts/validate_project.py

pipeline:
	bash 13_PIPELINE/run_full_pipeline.sh

clean:
	rm -rf 11_FINAL_OUTPUT/geotiff_final/*.tif
	rm -rf 11_FINAL_OUTPUT/logs/*
	rm -f 13_PIPELINE/scripts/gdal_georef_final_commands.sh
	@echo "[OK] Output temporanei puliti"

help:
	@echo "=================================================="
	@echo "Forlì Digital Twin — Makefile v3.3 (Ciuccio)"
	@echo "=================================================="
	@echo ""
	@echo "  make structure     - Crea cartelle 11_FINAL_OUTPUT e relative"
	@echo "  make template      - Genera GCP_TEMPLATE_FOR_KEEP.csv"
	@echo "  make export-gcp    - Esporta GCP KEEP verificati"
	@echo "  make promote-gcp   - Promuove da matching CSV a FINAL"
	@echo "  make geotiff-cmds  - Genera script gdal_translate + gdalwarp"
	@echo "  make validate      - Validazione completa progetto"
	@echo "  make pipeline      - Esegue l'intera pipeline end-to-end"
	@echo "  make clean         - Pulisce GeoTIFF e log temporanei"
	@echo "  make help          - Questo messaggio"
	@echo ""
	@echo "Flusso consigliato dopo matching manuale:"
	@echo "  1. make structure"
	@echo "  2. make export-gcp"
	@echo "  3. make geotiff-cmds"
	@echo "  4. bash 13_PIPELINE/scripts/gdal_georef_final_commands.sh"
	@echo "  oppure semplicemente: make pipeline"
