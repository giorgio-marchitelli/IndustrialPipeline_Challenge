import random
import time

class Macchina:

    COMPORTAMENTI = ["rumoroso", "stabile", "drift"]

    def __init__(self, macchina_id: int, intervallo_min_ms: int, intervallo_max_ms: int):
        # salva attributi ricevuti
        self.macchina_id = macchina_id
        self.intervallo_min_ms = intervallo_min_ms
        self.intervallo_max_ms = intervallo_max_ms

        # assegna a rotazione uno dei 3 comportamenti usando % 3
        self.comportamento = self.COMPORTAMENTI[macchina_id % len(self.COMPORTAMENTI)]

        # valore di temperatura iniziale fra 20 e 30 gradi con precisione 2
        self.valore_base = round(random.uniform(20.0, 30.0), 2)
        self.valore_corrente = self.valore_base
