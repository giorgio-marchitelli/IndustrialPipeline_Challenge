import os

# --- Variabili MQTT su env ---
MQTT_HOST = os.getenv("MQTT_HOST", "rabbitmq")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "guest")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "guest")
MQTT_TOPIC_PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "sensori")

# --- Simulazione dispositivi ---
NUM_DEVICES = int(os.getenv("NUM_DEVICES", "20")) # 20 dispositivi 
MIN_INTERVAL_MS = int(os.getenv("MIN_INTERVAL_MS", "200")) # millisecondi
MAX_INTERVAL_MS = int(os.getenv("MAX_INTERVAL_MS", "3000"))