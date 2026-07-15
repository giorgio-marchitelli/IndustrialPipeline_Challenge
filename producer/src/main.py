import time
import json
import threading
import logging

import paho.mqtt.client as mqtt

# variabili d'ambiente e classi macchina
import config
from macchina import Macchina

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("producer")


# una singola connessione a MQTT condivisa da tutte le macchine
# funzione : loop infinito , singolo thread , singola macchina
def avvia_macchina(macchina: Macchina, client_mqtt: mqtt.Client):

    # topic formato : "sensori"/id_macchina
    topic = f"{config.MQTT_TOPIC_PREFIX}/{macchina.macchina_id}"

    # infinito
    while True:
        evento = macchina.costruisci_evento()
        payload = json.dumps(evento)  # da dizionario creato da macchina.py a JSON
        client_mqtt.publish(topic, payload)

        logger.info(f"Pubblicato su {topic}: {payload}")  # pubblica su topic

        attesa = macchina.prossimo_intervallo_secondi()
        time.sleep(attesa)  # aspetta intervallo prima di ripetere


def main():
    # Crea e connette il client MQTT
    client_mqtt = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client_mqtt.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)

    # Tenta la connessione a RabbitMQ, riprovando finche non e' pronto
    connesso = False
    tentativi = 0
    while not connesso and tentativi < 20:
        try:  # tenta di connettersi
            client_mqtt.connect(config.MQTT_HOST, config.MQTT_PORT)
            connesso = True
        except ConnectionRefusedError:
            tentativi += 1
            logger.warning(f"RabbitMQ non ancora pronto, ritento tra 3 secondi... (tentativo {tentativi})")
            time.sleep(3)  # attende 3 secondi

    if not connesso:
        raise Exception("Impossibile connettersi a RabbitMQ dopo 20 tentativi")

    client_mqtt.loop_start()  # avvia thread che gestisce comunicazione in background

    # Crea le 20 macchine dentro lista formato Macchina(id, 200, 3000),
    macchine = []
    for i in range(1, config.NUM_DEVICES + 1):
        nuova_macchina = Macchina(i, config.MIN_INTERVAL_MS, config.MAX_INTERVAL_MS)  # id macchina = i
        macchine.append(nuova_macchina)  # aggiungo sta macchina alla lista

    # Avvia e tiene attivi i thread
    threads = []  # Lista di thread
    for macchina in macchine:  # scorre lista macchine
        thread = threading.Thread(target=avvia_macchina, args=(macchina, client_mqtt))
        thread.start()  # avvia thread
        threads.append(thread)  # aggiunge a lista

    for thread in threads:
        thread.join()  # continua a far girare main finche thread sono attivi


# se file e' stato lanciato direttamente -> esegui main
if __name__ == "__main__":
    main()