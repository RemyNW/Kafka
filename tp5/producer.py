import time
import requests
from kafka import KafkaProducer
from requests.auth import HTTPBasicAuth


# Configuration Kafka
kafka_producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: v.encode("utf-8")
)

# Configuration API Meteomatics
USERNAME = "epsi_now_remy"
PASSWORD = "U1dRPt8K7b"
LOCATION = "52.520551,13.461804"  # Coordonnées pour Berlin par exemple
PARAMETERS = "t_2m:C"  # Température à 2m en °C
TOPIC = "meteo"


def get_weather():
    """ Récupère les données météo depuis l'API Meteomatics """
    base_url = "https://api.meteomatics.com"
    datetime = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    api_url = f"{base_url}/{datetime}/{PARAMETERS}/{LOCATION}/json"

    try:
        response = requests.get(api_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erreur lors de la récupération des données météo : {e}")
        return None


def send_to_kafka(data):
    """ Envoie les données dans Kafka """
    kafka_producer.send(
        topic=TOPIC,
        value=str(data)
    )
    kafka_producer.flush()
    print(f"Envoyé dans Kafka : {data}")    


if __name__ == "__main__":
    while True:
        weather_data = get_weather()
        if weather_data:
            send_to_kafka(weather_data)
        time.sleep(10)  # Attente de 10 secondes avant la prochaine requête
