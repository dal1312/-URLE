# Protocollo di Matching GCP — Forlì Digital Twin v3.3

## Obiettivo

Ottenere un set di Ground Control Points di alta qualità per trasformare i raster storici FO004 in coordinate EPSG:25832 con residuali accettabili.

## Priorità dei punti (in ordine)

1. **PRIORITY_REVIEW / A**  
   - Porte storiche (Porta Schiavonia, Porta Ravaldino, Barriera San Pietro, Barriera Vittorio Emanuele)
   - Rocca di Ravaldino e opere fortificate
   - Complessi religiosi maggiori (San Domenico, Sant’Agostino)

2. **REVIEW / B**  
   - Incroci stradali principali e assi viari stabili
   - Spigoli di isolati e mura urbane
   - Piazze storiche (Piazza Mercuriale, Piazza Garibaldi)

3. **LOW_PRIORITY_REVIEW / C**  
   - Punti secondari, da usare solo se servono a migliorare la distribuzione spaziale

## Regole operative

- Ogni punto deve avere corrispondenza **omologa univoca** tra carta storica e CTR moderna.
- Evitare elementi soggetti a modifiche recenti (edifici nuovi, rettifiche stradali).
- Distribuzione spaziale: coprire i quattro quadranti del foglio.
- Distanza minima consigliata tra due punti target: ≥ 40–50 metri.
- Numero minimo per foglio: **8 punti KEEP**.
- Preferire punti con alta confidenza geometrica (angoli netti, intersezioni chiare).

## Decision values ammessi

- `KEEP`          → usato per la trasformazione
- `REJECT`        → scartato definitivamente
- `REVIEW`        → da rivedere
- `PRIORITY_REVIEW`
- `LOW_PRIORITY_REVIEW`

## Workflow consigliato

1. Inizia dai 4–5 punti PRIORITY_REVIEW di ogni foglio.
2. Aggiungi punti REVIEW per raggiungere quota 8+.
3. Controlla distribuzione e distanza minima.
4. Salva backup JSON.
5. Esegui `make export-gcp`.

## Residuali

Dopo la georeferenziazione con TPS:
- Residuali medi ideali < 2–3 metri
- Residuali massimi accettabili < 5–6 metri (in contesti urbani storici)

Se residuali alti → rivedere i punti più lontani o aggiungere punti intermedi.

---

Protocollo redatto da Dott. Ing. Massimo Valtieri (Ciuccio) — v3.3
