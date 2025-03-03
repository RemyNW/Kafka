import json
import ast
from kafka import KafkaConsumer
from minio import Minio
from minio.error import S3Error
import io
from datetime import datetime


minio_client = Minio(
    "localhost:9000",
    access_key="minio",
    secret_key="password",
    secure=False
)

bucket_name = "meteo"

# Vérifie que le bucket existe, sinon le crée
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)
    print(f"Bucket '{bucket_name}' créé avec succès !")


# Configuration Kafka
kafka_consumer = KafkaConsumer(
    "meteo",  # On écoute le topic 'meteo'
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: x.decode("utf-8")
)


def extract_data(message):
    """ Extrait les données utiles du message JSON """
    try:
        data = ast.literal_eval(message)

        temp_data = data["data"][0]["coordinates"][0]["dates"][0]
        result = {
            "datetime": temp_data["date"],
            "temperature": temp_data["value"]
        }
        return result
    except (KeyError, IndexError, json.JSONDecodeError, TypeError, ValueError, SyntaxError) as e:
        print(f"Erreur lors de l'extraction des données : {e}")
        return None


def send_to_minio(data):
    """ Envoie les données JSON vers MinIO """
    try:
        # Conversion en JSON et création d'un fichier en mémoire
        json_data = json.dumps(data, indent=4)
        json_bytes = json_data.encode("utf-8")
        json_file = io.BytesIO(json_bytes)

        # Création d'un nom de fichier unique basé sur le timestamp
        filename = f"meteo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Envoi dans MinIO
        minio_client.put_object(
            bucket_name,
            filename,
            data=json_file,
            length=len(json_bytes),
            content_type="application/json"
        )
        print(f"Fichier '{filename}' envoyé avec succès dans le bucket '{bucket_name}'")
    except S3Error as e:
        print(f"Erreur lors de l'envoi dans MinIO : {e}")


if __name__ == "__main__":
    print("En attente des messages...")
    for message in kafka_consumer:
        print(f"Message brut reçu : {message.value}")  # Debug
        cleaned_data = extract_data(message.value)
        if cleaned_data:
            print(json.dumps(cleaned_data, indent=4))
            send_to_minio(cleaned_data)  # Envoi des données dans MinIO
