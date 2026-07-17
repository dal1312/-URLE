# UPGRADE REPORT v3.3 — Forlì Digital Twin

**Eseguito da:** Dott. Ing. Massimo Valtieri (Ciuccio)  
**Data:** 2026-07-17  
**Branch:** `ciuccio/v3.3-full-upgrade`

## File modificati / creati

### Script pipeline (13_PIPELINE/scripts/)
- `export_gcp_verified.py` → v3.0 (hardening + report)
- `promote_verified_gcps.py` → v3.0
- `build_gdal_commands.py` → v3.0 (gdaladdo + compressione migliore)
- `validate_project.py` → v3.0
- `create_output_structure.py` → nuovo
- `generate_gcp_template.py` → nuovo

### Orchestrazione
- `13_PIPELINE/run_full_pipeline.sh` → v3.0
- `Makefile` → v3.3 completo

### Documentazione
- `docs/PIPELINE_GUIDE_v3_3.md`
- `docs/GCP_MATCHING_PROTOCOL.md`
- `README_MASTER_v3_3.md`

### Runtime / Status
- `00_RUNTIME/data/project_status.json` → aggiornato a 3.3

### Struttura
- `11_FINAL_OUTPUT/` completa (geotiff_final, vector, residual_maps, reports, logs)

## Cosa rimane da fare all’operatore

1. Aprire il workbench e completare i target reali (minimo 8 KEEP per foglio).
2. Salvare il backup JSON.
3. Lanciare `make pipeline`.

## Note tecniche

Tutti gli script sono retrocompatibili con la struttura esistente del repository.  
Nessun dato geografico è stato inventato.  
La pipeline è ora production-ready non appena i GCP KEEP sono disponibili.

---

Fine upgrade. Sistema pronto.
