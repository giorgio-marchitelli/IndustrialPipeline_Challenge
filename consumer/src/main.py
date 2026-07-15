import json
import time
import logging
from datetime import datetime

import paho.mqtt.client as mqtt

import config
import database
import api
from gestore_stato import GestoreStato

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("consumer")

gestore = GestoreStato()  #dizionario di ogni macchina e valore
connessione_db = database.connetti()
database.crea_schema(connessione_db)
stato_iniziale = database.leggi_ultimo_valore_per_macchina(connessione_db)
gestore.imposta_stato_iniziale(stato_iniziale)
api.imposta_connessione(connessione_db)  #passa la connessione all'API
logger.info(f"Schema database pronto, stato ricostruito per {len(stato_iniziale)} macchine")


# alla connessione di paho-mqtt parte sta funzion
def on_connect(client, userdata, flags, reason_code, properties=None):  #parametri utili alla connessione
    if reason_code == 0:
        logger.info("Connesso a RabbitMQ (MQTT)")
        client.subscribe(config.MQTT_TOPIC_SOTTOSCRIZIONE)
        logger.info(f"Sottoscritto al topic {config.MQTT_TOPIC_SOTTOSCRIZIONE}")
    else:
        logger.error(f"Connessione fallita, codice: {reason_code}")


# chiamata da paho-mqtt ogni volta che arriva un messaggio
def on_message(client, userdata, msg):
    try:
        evento = json.loads(msg.payload.decode())  #decodifica

        id_macchina = evento["macchina_id"]
        valore = evento["valore"]
        comportamento = evento["comportamento"]
        timestamp_evento = datetime.fromtimestamp(evento["timestamp"])  #formato epoch

        deve_salvare = gestore.valuta_evento(id_macchina, valore)  #true o false

        if deve_salvare:
            database.inserisci_evento(connessione_db, id_macchina, valore, comportamento, timestamp_evento)
            logger.info(f"Salvato evento macchina {id_macchina}, valore {valore}")
        else:
            logger.info(f"Scartato evento macchina {id_macchina}, valore {valore}")

    except Exception as errore:
        logger.error(f"Errore nella gestione del messaggio: {errore}")


client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)  # specifica versione delle firme di chiamate callback
client.username_pw_set(config.MQTT_UTENTE, config.MQTT_PASSWORD)  #credenziali
client.on_connect = on_connect
client.on_message = on_message

connesso = False
tentativi = 0

while not connesso and tentativi < 20:
    try:
        client.connect(config.MQTT_HOST, config.MQTT_PORTA)
        connesso = True
    except Exception as errore:
        tentativi += 1
        logger.warning(f"RabbitMQ non ancora pronto, ritento tra 3 secondi... (tentativo {tentativi})")
        time.sleep(3)

if not connesso:
    raise Exception("Impossibile connettersi a RabbitMQ dopo 20 tentativi")

# non piu loop.forever altrimenti non partiva mai blocco API
client.loop_start()  # MQTT gira in thread separato cosi' puo' partire anche l'API
logger.info("Avvio API REST sulla porta 8000")
api.app.run(host="0.0.0.0", port=8000)  #avvia il server Flask porta 8000