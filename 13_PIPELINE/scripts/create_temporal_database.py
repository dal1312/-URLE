#!/usr/bin/env python3
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
out_dir = ROOT / "07_DATABASE"
out_dir.mkdir(exist_ok=True)
db = out_dir / "forli_temporal_model.sqlite"

con = sqlite3.connect(db)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    title TEXT,
    year TEXT,
    institution TEXT,
    resource_type TEXT,
    status TEXT,
    notes TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS features (
    feature_id TEXT PRIMARY KEY,
    name TEXT,
    feature_type TEXT,
    year_start INTEGER,
    year_end INTEGER,
    start_precision TEXT,
    end_precision TEXT,
    status TEXT,
    source_id TEXT,
    confidence TEXT,
    geometry_ref TEXT,
    notes TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    name TEXT,
    event_type TEXT,
    year_start INTEGER,
    year_end INTEGER,
    location_ref TEXT,
    source_id TEXT,
    confidence TEXT,
    notes TEXT
)
""")

cur.execute("""
CREATE VIEW IF NOT EXISTS v_features_1488 AS
SELECT *
FROM features
WHERE (year_start IS NULL OR year_start <= 1488)
AND (year_end IS NULL OR year_end >= 1488)
""")

con.commit()
con.close()
print(f"Creato/aggiornato: {db}")
