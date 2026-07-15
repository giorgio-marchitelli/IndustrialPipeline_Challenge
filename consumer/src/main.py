import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

import config
import database
import api
from gestore_stato import GestoreStato

gestore = GestoreStato()  #dizionario di ogni macchina e valore
connessione_db = database.connetti()
database.crea_schema(connessione_db)
api.imposta_connessione(connessione_db)  #passa la connessione all'API
# TODO: sostituire con log
print("Schema database pronto")


# alla connessione di paho-mqtt parte sta funzion
def on_connect(client, userdata, flags, reason_code, properties=None):  #parametri utili alla connessione
    if reason_code == 0:
        # TODO: sostituire con log
        print("Connesso a RabbitMQ (MQTT)")
        client.subscribe(config.MQTT_TOPIC_SOTTOSCRIZIONE)
        # TODO: sostituire con log
        print(f"Sottoscritto al topic {config.MQTT_TOPIC_SOTTOSCRIZIONE}")
    else:
        # TODO: sostituire con log
        print(f"Connessione fallita, codice: {reason_code}")


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
            # TODO: sostituire con log
            print(f"Salvato evento macchina {id_macchina}, valore {valore}")
        else:
            # TODO: sostituire con log
            print(f"Scartato evento macchina {id_macchina}, valore {valore}")

    except Exception as errore:
        # TODO: sostituire con log
        print(f"Errore nella gestione del messaggio: {errore}")


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
        # TODO: sostituire con log
        print(f"RabbitMQ non ancora pronto, ritento tra 3 secondi... (tentativo {tentativi})")
        time.sleep(3)

if not connesso:
    raise Exception("Impossibile connettersi a RabbitMQ dopo 20 tentativi")

# non piu loop.forever altrimenti non partiva mai blocco API
client.loop_start()  # MQTT gira in thread separato cosi' puo' partire anche l'API
# TODO: sostituire con log
print("Avvio API REST sulla porta 8000")
api.app.run(host="0.0.0.0", port=8000)  #avvia il server Flask porta 8000