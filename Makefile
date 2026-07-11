# Makefile - Forlì Digital Twin Master v3.2

.PHONY: all export-gcp pipeline help

all: pipeline

export-gcp:
	python 13_PIPELINE/scripts/export_gcp_verified.py

pipeline:
	bash 13_PIPELINE/run_full_pipeline.sh

clean:
	rm -rf 11_FINAL_OUTPUT/geotiff_final/*.tif

help:
	@echo "Comandi disponibili:"
	@echo "  make export-gcp   - Esporta GCP verificati"
	@echo "  make pipeline     - Esegui pipeline completa"
	@echo "  make clean        - Pulisci output GeoTIFF"
