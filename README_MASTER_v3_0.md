# Forlì Digital Twin — Master Project v3.2

## Stato consolidamento
- Artefatti inventariati nel runtime corrente: 133+
- CRS operativo: **EPSG:25832**
- Versione Master: **v3.2 Runtime Dashboard**

## Automazione Pipeline (Nuovo in v3.2)

È ora disponibile un flusso automatizzato per l’esportazione e validazione dei GCP:

```bash
# 1. Dopo aver completato il matching nel Workbench
python 13_PIPELINE/scripts/export_gcp_verified.py

# 2. Esegui l'intera pipeline in sequenza
bash 13_PIPELINE/run_full_pipeline.sh
```

### Script disponibili

| Script | Descrizione | Note |
|--------|-------------|------|
| `export_gcp_verified.py` | Esporta solo GCP `KEEP` + validazione geometrica + report | v2.0 |
| `run_full_pipeline.sh` | Esegue in sequenza tutti i passaggi principali | Nuovo |
| `validate_project.py` | Controlla integrità struttura e conteggio GCP | Esistente |

## Blocco critico attuale
Il collo di bottiglia rimane il **matching omologo reale** dei GCP storico ↔ CTR.
Senza almeno 6-8 GCP verificati per foglio non si possono generare i GeoTIFF definitivi.

## Flusso consigliato

1. Apri `08_WEB_APP/workbench_v3_2.html`
2. Assegna i target cliccando sulla CTR
3. Porta almeno 6-8 GCP per foglio a `KEEP`
4. Clicca **Backup JSON**
5. Esegui `export_gcp_verified.py`
6. (Opzionale) `bash run_full_pipeline.sh`

## Regola di stato
- **VERIFIED**: verificato su dati reali
- **GENERATED**: prodotto dalla pipeline
- **PRELIMINARY**: struttura valida ma incompleta
- **REVIEW_REQUIRED**: richiede controllo
- **MISSING**: non ancora prodotto

## Nota di integrità
Il Master Project mantiene solo gli artefatti core. I file raster originali restano nella cartella `02_RASTER_STORICI/` e `03_CTR_MODERNA/`.
