# Forlì Digital Twin — Master Project v3.3 (Ciuccio Upgrade)

**Autore upgrade:** Dott. Ing. Massimo Valtieri (Ciuccio)  
**Data:** 2026-07-17  
**CRS:** EPSG:25832  

## Cosa è stato fatto in questo upgrade

- Hardening completo di tutti gli script della pipeline (`export_gcp_verified.py`, `promote_verified_gcps.py`, `build_gdal_commands.py`, `validate_project.py`)
- Nuovi script:
  - `create_output_structure.py`
  - `generate_gcp_template.py`
- `run_full_pipeline.sh` riscritto con logging e fail-fast
- Makefile avanzato con target chiari
- Struttura `11_FINAL_OUTPUT/` completa
- Documentazione tecnica:
  - `docs/PIPELINE_GUIDE_v3_3.md`
  - `docs/GCP_MATCHING_PROTOCOL.md`
- `project_status.json` aggiornato a v3.3

## Stato attuale

Il collo di bottiglia rimane **esclusivamente** il matching manuale dei GCP nel workbench.

Una volta che hai almeno 8 punti `KEEP` con coordinate target reali per ogni foglio (FO004_042 … 045), la pipeline è pronta a generare i GeoTIFF finali in un unico comando.

## Comandi rapidi

```bash
# Dopo aver completato il matching e salvato il backup JSON
make structure
make export-gcp
make geotiff-cmds
bash 13_PIPELINE/scripts/gdal_georef_final_commands.sh

# oppure tutto insieme
make pipeline
```

## Documentazione

- [PIPELINE_GUIDE_v3_3.md](docs/PIPELINE_GUIDE_v3_3.md)
- [GCP_MATCHING_PROTOCOL.md](docs/GCP_MATCHING_PROTOCOL.md)

## Prossimi passi scientifici

1. Completare matching GCP (priorità assoluta)
2. Generare GeoTIFF
3. Vettorializzazione storica
4. Database temporale
5. Viewer pubblico e release

---

Upgrade eseguito da **Dott. Ing. Massimo Valtieri (Ciuccio)** — livello SUPREMO.
