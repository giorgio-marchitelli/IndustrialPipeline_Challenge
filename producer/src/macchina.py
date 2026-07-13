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

    # calcola dopo quanto parte prossimo evento
    def prossimo_intervallo_secondi(self) -> float:
        intervallo_ms = random.uniform(self.intervallo_min_ms, self.intervallo_max_ms)
        return intervallo_ms / 1000.0  # in secondi

    # genera valore in base al comportamento
    def genera_valore(self) -> float:
        if self.comportamento == "rumoroso":
            self.valore_corrente = self.valore_base + random.uniform(-5.0, 5.0)  # oscillazione ampia

        elif self.comportamento == "stabile":
            self.valore_corrente = self.valore_base + random.uniform(-0.2, 0.2)  # variazione minima

        elif self.comportamento == "drift":
            self.valore_corrente += random.uniform(0.05, 0.15)  # aggiunta costante al valore corrente

        return round(self.valore_corrente, 2)

    # restituisce dizionario
    def costruisci_evento(self) -> dict:
        return {
            "macchina_id": self.macchina_id,
            "valore": self.genera_valore(),
            "comportamento": self.comportamento,
            "timestamp": time.time(),  # tempo in cui e' stato creato
        }