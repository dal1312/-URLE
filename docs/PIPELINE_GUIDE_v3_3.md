# Forlì Digital Twin — Pipeline Guide v3.3 (Ciuccio Upgrade)

## Panoramica

Questa guida descrive il flusso completo per portare i fogli storici FO004 (Catasto Gregoriano di Forlì) da raster grezzo a GeoTIFF georeferenziati in **EPSG:25832**.

## Prerequisiti

- Python 3.9+
- GDAL / ogr (gdal_translate, gdalwarp, gdaladdo)
- Browser moderno per il workbench

## Flusso Operativo

### 1. Matching GCP (fase manuale critica)

1. Apri `08_WEB_APP/workbench_v3_2.html`
2. Carica / usa `point_matching_v2_7.json`
3. Per ogni foglio (FO004_042 … 045):
   - Identifica punti omologhi stabili (angoli di edifici, intersezioni stradali, porte storiche, spigoli di mura)
   - Clicca il target sulla CTR
   - Imposta `decision = KEEP`
   - Compila almeno **8 punti KEEP** per foglio
4. Esporta / salva il backup JSON (workbench_backup.json)

### 2. Esportazione e validazione

```bash
make structure
make export-gcp
# oppure
python 13_PIPELINE/scripts/export_gcp_verified.py
```

Se tutto ok viene generato:
- `04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv`
- report in `11_FINAL_OUTPUT/reports/`

### 3. Generazione comandi GDAL

```bash
make geotiff-cmds
```

Viene creato:
- `13_PIPELINE/scripts/gdal_georef_final_commands.sh`

### 4. Esecuzione georeferenziazione

```bash
bash 13_PIPELINE/scripts/gdal_georef_final_commands.sh
```

Output:
- `11_FINAL_OUTPUT/geotiff_final/FO004_0XX_FINAL_EPSG25832.tif`

### 5. Pipeline completa (alternativa)

```bash
make pipeline
```

Esegue automaticamente i passi 0→5 con logging.

## Criteri di accettazione GCP

- Minimo 8 punti KEEP per foglio
- Distanza minima tra punti target ≥ 40 m
- Residuali il più bassi possibili (valutare dopo gdalwarp con `gdalinfo` o script residuali)
- Preferire punti su elementi costruiti stabili nel tempo

## Prossimi passi dopo i GeoTIFF

1. Vettorializzazione (`vectorize_historical.py`)
2. Popolamento database temporale
3. Viewer pubblico
4. Release e pubblicazione

---

Generato da Dott. Ing. Massimo Valtieri (Ciuccio) — Upgrade v3.3
