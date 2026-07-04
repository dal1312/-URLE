# Pipeline Finale — Forlì Digital Twin

## Obiettivo finale

Produrre:
1. GeoTIFF storici definitivi;
2. layer vettoriali storici;
3. database temporale;
4. viewer web finale;
5. pacchetto di pubblicazione.

## Fase A — GCP reali

Input:
- `03_CTR_MODERNA/CTR_7tiles_EPSG25832.vrt`
- `02_RASTER_STORICI/*.jpg`
- `04_GCP_GEOREF/GCP_point_matching_v2_7.csv`

Output:
- `04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv`

Regola:
un GCP è valido solo se `decision=KEEP` e contiene target EPSG:25832.

## Fase B — GeoTIFF storici finali

Input:
- raster storici;
- `GCP_FINAL_VERIFIED.csv`

Output:
- `11_FINAL_OUTPUT/geotiff_final/FO004_042_FINAL_EPSG25832.tif`
- `11_FINAL_OUTPUT/geotiff_final/FO004_043_FINAL_EPSG25832.tif`
- `11_FINAL_OUTPUT/geotiff_final/FO004_044_FINAL_EPSG25832.tif`
- `11_FINAL_OUTPUT/geotiff_final/FO004_045_FINAL_EPSG25832.tif`

## Fase C — Vettorializzazione

Layer:
- mura;
- fossati;
- porte;
- strade;
- isolati;
- edifici;
- chiese;
- conventi;
- palazzi;
- torri;
- canali;
- orti;
- vigne.

Output:
- GeoPackage finale;
- GeoJSON web semplificati.

## Fase D — Database temporale

Ogni oggetto deve avere:
- `feature_id`;
- `name`;
- `feature_type`;
- `year_start`;
- `year_end`;
- `geometry_ref`;
- `source_id`;
- `confidence`.

## Fase E — Viewer finale

Funzioni:
- mappa base storica;
- layer attivabili;
- timeline;
- ricerca;
- popup;
- schede storiche;
- confronto moderno/storico.

## Fase F — Release

Output:
- pacchetto ZIP finale;
- manifest;
- checksum;
- licenze;
- citazione;
- documentazione.
