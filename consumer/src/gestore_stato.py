import config

# Mantiene in memoria ultimo valore persistito per ogni macchina
# Decide se un nuovo evento va salvato o scartato
class GestoreStato:

    def __init__(self):
        self.ultimo_valore_persistito = {}    # Dizionario: {id_device : ultimo valore persistito}

    def imposta_stato_iniziale(self, stato_iniziale):
        # ricostruisce lo stato in memoria a partire dai dati letti dal database all'avvio
        self.ultimo_valore_persistito = stato_iniziale

    def valuta_evento(self, id_device, valore):
        # Controlla se per quella macchina non abbiamo un evento gia salvato
        if id_device not in self.ultimo_valore_persistito:
            self.ultimo_valore_persistito[id_device] = valore
            return True  # se e' il primo si salva sempre

        # Regola 1: Macchina con id multiplo di MULTIPLO_ID_SEMPRE_SALVATO
        if id_device % config.MULTIPLO_ID_SEMPRE_SALVATO == 0:
            self.ultimo_valore_persistito[id_device] = valore  # aggiorna dizionario
            return True

        # Regola 2: Calcolo variazione rispetto all'ultimo valore salvato
        valore_precedente = self.ultimo_valore_persistito[id_device]

        # consideriamo qualsiasi valore diverso da 0 come variazione massima
        if valore_precedente == 0:
            if valore != 0:
                variazione_percentuale = 100
            else:
                variazione_percentuale = 0
        else:
            variazione_percentuale = abs(valore - valore_precedente) / abs(valore_precedente) * 100

        if variazione_percentuale >= config.SOGLIA_VARIAZIONE_PERCENTUALE:
            self.ultimo_valore_persistito[id_device] = valore
            return True

        return False