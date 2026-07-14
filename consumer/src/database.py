import time
import psycopg2  #per usare postgresql
import config
 
 
def connetti():
    # parametri presi da config, riprova finche' postgres non e' pronto
    connesso = False
    tentativi = 0
    connessione = None
 
    while not connesso and tentativi < 20:
        try:
            connessione = psycopg2.connect(
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORTA,
                dbname=config.POSTGRES_DATABASE,
                user=config.POSTGRES_UTENTE,
                password=config.POSTGRES_PASSWORD,
            )
            connesso = True
        except psycopg2.OperationalError as errore:
            tentativi += 1
            # TODO: sostituire con log
            print(f"PostgreSQL non ancora pronto, ritento tra 3 secondi... (tentativo {tentativi})")
            time.sleep(3)
 
    if not connesso:
        raise Exception("Impossibile connettersi a PostgreSQL dopo 20 tentativi")
 
    return connessione
 
 
#crea schema in DB
def crea_schema(connessione):
    comando_sql = """
        CREATE TABLE IF NOT EXISTS eventi (
            id SERIAL PRIMARY KEY,
            id_macchina INTEGER NOT NULL,
            valore REAL NOT NULL,
            comportamento TEXT NOT NULL,
            timestamp_evento TIMESTAMP NOT NULL,
            timestamp_salvataggio TIMESTAMP NOT NULL DEFAULT NOW()
        );
    """
 
    cursore = connessione.cursor()
    cursore.execute(comando_sql)
    connessione.commit()  #fa partire i comandi eseguiti con execute
    cursore.close()
 
 
#inserisce evento quando GestoreStato.valuta_evento() restituisce True
def inserisci_evento(connessione, id_macchina, valore, comportamento, timestamp_evento):
 
    comando_sql = """
        INSERT INTO eventi (id_macchina, valore, comportamento, timestamp_evento)
        VALUES (%s, %s, %s, %s);
    """
    cursore = connessione.cursor()
    cursore.execute(comando_sql, (id_macchina, valore, comportamento, timestamp_evento))  #passa i parametri dentro la query
    connessione.commit()
    cursore.close()
 