# Comandi

## Far partire i servizi da zero 
docker compose down -v
docker compose up --build

## Fermato container e ora riprendere 
docker compose up


##  SQL

Far partire terminale Postgre
    docker exec -it industrialpipeline_challenge-postgres-1 psql -U postgres -d pipeline_industriale

Contare eventi totali:
    SELECT COUNT(*) FROM eventi;

Ultimo valore per ogni macchina:
    SELECT DISTINCT ON (id_macchina) id_macchina, valore, timestamp_salvataggio FROM eventi ORDER BY id_macchina, id DESC;

Verifica regola del 15% (deve dare 0 rows):
    WITH eventi_con_precedente AS (SELECT id, id_macchina, valore, timestamp_salvataggio, LAG(valore) OVER (PARTITION BY id_macchina ORDER BY id) AS valore_precedente FROM eventi WHERE id_macchina % 5 != 0) SELECT id, id_macchina, valore_precedente, valore, ROUND(CAST(ABS(valore - valore_precedente) / NULLIF(ABS(valore_precedente), 0) * 100 AS numeric), 2) AS variazione_percentuale FROM eventi_con_precedente WHERE valore_precedente IS NOT NULL AND ABS(valore - valore_precedente) / NULLIF(ABS(valore_precedente), 0) * 100 < 15 ORDER BY id;


## API

http://localhost:8000/eventi
http://localhost:8000/eventi?limite=20
http://localhost:8000/eventi/7
