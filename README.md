# Forlì Digital Twin — Master v3.2 Runtime Dashboard

## Avvio

Metodo consigliato:

```bash
python start_server.py
```

Oppure aprire:

```text
index.html
```

Dashboard:

```text
00_RUNTIME/index.html
```



---

# Forlì Digital Twin

Digital Twin storico-temporale della citta di Forli.

Il progetto integra cartografia storica, Catasto Gregoriano, fogli catastali storici, CTR moderna EPSG:25832, workbench GCP, modello temporale, pipeline GIS, viewer web, manifest e inventario dei dati.

## Stato corrente

Il progetto e consolidato nel Master v3.2 operativo.

Completato:
- inventario generale;
- CTR moderna georeferenziata;
- mosaico virtuale VRT;
- workbench GCP corretto;
- schema temporale;
- struttura web GIS;
- pipeline tecnica;
- script rapido di controllo GCP.

Da completare:
- matching reale dei GCP;
- esportazione GCP_FINAL_VERIFIED.csv;
- GeoTIFF storici finali;
- vettorializzazione;
- database storico popolato;
- rilascio web finale.

## CRS operativo

EPSG:25832 - ETRS89 UTM zone 32N.

## Avvio workbench

Da terminale entrare nella cartella 08_WEB_APP e avviare un server locale Python sulla porta 8000.

Poi aprire il browser sulla porta 8000.

## Controllo GCP

Da root repository eseguire lo script 13_PIPELINE/scripts/check_gcp_status.py.

## Pipeline finale

Seguire 13_PIPELINE/PIPELINE_FINAL_COMPLETION.md.

## Piano operativo

Seguire 13_PIPELINE/NEXT_STEPS_v3_2.md.

## Repository

https://github.com/dal1312/-URLE
