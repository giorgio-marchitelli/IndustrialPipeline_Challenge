import os

# Parametri di connessione a RabbitMQ (MQTT)
MQTT_HOST = os.getenv("MQTT_HOST", "rabbitmq")
MQTT_PORTA = int(os.getenv("MQTT_PORTA", "1883"))
MQTT_UTENTE = os.getenv("MQTT_UTENTE", "guest")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "guest")
MQTT_TOPIC_SOTTOSCRIZIONE = os.getenv("MQTT_TOPIC_SOTTOSCRIZIONE", "sensori/#")

# Parametri di connessione a PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORTA = int(os.getenv("POSTGRES_PORTA", "5432"))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "pipeline_industriale")
POSTGRES_UTENTE = os.getenv("POSTGRES_UTENTE", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")


# Regole di business per la persistenza degli eventi
SOGLIA_VARIAZIONE_PERCENTUALE = float(os.getenv("SOGLIA_VARIAZIONE_PERCENTUALE", "15"))
MULTIPLO_ID_SEMPRE_SALVATO = int(os.getenv("MULTIPLO_ID_SEMPRE_SALVATO", "5"))