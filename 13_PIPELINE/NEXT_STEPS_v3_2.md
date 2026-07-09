# Forlì Digital Twin — Next Steps v3.2

## Stato operativo

Il viewer web è stato corretto per caricare il file `point_matching_v2_7.json` dal percorso reale dentro `08_WEB_APP`.

## Priorità 1 — GCP

Completare il matching manuale dei punti di controllo.

Requisito minimo per ogni foglio storico:

- almeno 8 punti con `decision=KEEP`;
- `source_x` e `source_y` numerici;
- `target_easting_epsg25832` e `target_northing_epsg25832` numerici;
- `target_tile` compilato.

Output atteso:

```text
04_GCP_GEOREF/GCP_FINAL_VERIFIED.csv
```

## Priorità 2 — GeoTIFF finali

Dopo il CSV verificato, generare i GeoTIFF finali in:

```text
11_FINAL_OUTPUT/geotiff_final/
```

## Priorità 3 — vettorializzazione

Creare layer storici per mura, strade, isolati, edifici, chiese, conventi, palazzi, torri, canali e aree agricole.

## Priorità 4 — viewer pubblico

Separare il workbench tecnico dal viewer pubblico finale.
