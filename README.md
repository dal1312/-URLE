# Forlì Digital Twin Operational v2.0

Pacchetto operativo generato dalla tavola del Catasto Gregoriano di Forlì.

## Immagine sorgente
- File usato: `iipgggsrv.fcgi`
- Dimensione originale rilevata: 8000 × 6383 px

## Contenuto
- `00_MASTER/` immagine master JPG/TIFF
- `01_RESTAURO/` versione restaurata leggera
- `02_WEB/` viewer HTML operativo
- `03_GIS/geojson/` layer iniziali in coordinate pixel
- `04_DATABASE/` CSV, SQLite e query SQL
- `06_DOC/` documentazione operativa

## Uso rapido
Apri:

`02_WEB/index.html`

## Nota scientifica
I layer sono in coordinate pixel e sono preliminari. Il passaggio successivo è georeferenziare la carta e trasformare i layer in EPSG:25832 o EPSG:32633.
