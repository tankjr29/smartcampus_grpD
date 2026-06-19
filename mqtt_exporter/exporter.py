import time
from prometheus_client import start_http_server, Gauge
import paho.mqtt.client as mqtt
import random

# Définition de la métrique Prometheus
PLACES_LIBRES = Gauge('parking_places_libres', 'Nombre de places disponibles dans le parking')

# Configuration du Broker Public HiveMQ
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "campus/parking/kossivi/places"

def on_connect(client, userdata, flags, rc):
    print(f" Connecté au Broker public HiveMQ avec le code : {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f" Abonné au topic : {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        valeur = int(payload)
        
        PLACES_LIBRES.set(valeur)
        print(f" [MÀJ PROMETHEUS] -> {valeur} places libres reçues.")
    except ValueError:
        print(f" Erreur de format sur le message : {payload}")

def main():
    # Lancement du serveur d'exposition Prometheus sur le port 8000
    start_http_server(8000)
    print(" Serveur Metrics Prometheus accessible sur le port 8000")

    # Client MQTT avec ID unique
    client_id = f"Python_Exporter_{random.randint(1000, 9999)}"
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f" Connexion au broker public : {MQTT_BROKER}...")
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception as e:
            print(f" Échec de connexion au serveur public ({e}), nouvelle tentative...")
            time.sleep(3)

    client.loop_forever()

if __name__ == '__main__':
    main()