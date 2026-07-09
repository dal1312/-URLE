# URLE Web Workbench Workflow v3.2

## Flusso operativo

1. Avviare un server locale nella cartella `08_WEB_APP`.
2. Aprire `index.html` per il matching storico-CTR.
3. Selezionare un GCP candidato.
4. Cliccare il punto omologo sulla CTR.
5. Verificare coordinate EPSG:25832 e tile.
6. Salvare il lavoro locale.
7. Aprire `readiness.html` per controllare la soglia 8 GCP per foglio.
8. Quando tutti i fogli sono READY, esportare `GCP_FINAL_VERIFIED.csv`.
9. Eseguire la pipeline finale in `13_PIPELINE/scripts`.

## Persistenza

Il modulo `workbench_state.js` usa `localStorage` con chiave `urle_gcp_workbench_v3_2`.

Funzioni disponibili:

- `URLEState.load(data)`
- `URLEState.save(data)`
- `URLEState.clear()`
- `URLEState.exportJson(data)`

## Sicurezza dati operativa

Prima di cancellare dati browser o cambiare dispositivo, esportare un backup JSON del workbench.
