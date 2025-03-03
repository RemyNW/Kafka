# Kafka & MinIO Data Pipeline

Ce projet met en place un pipeline de données en utilisant **Apache Kafka** et **MinIO**. Il permet de **consommer des fichiers JSON** et de les stocker dans **MinIO** après leur passage par Kafka.

## 📌 Fonctionnalités

✅ **Kafka Producer** : Récupère des transactions aléatoires d'une API et les envoie à Kafka sous forme de fichiers JSON.\
✅ **Kafka Consumer** : LConsomme les messages Kafka et les stocke dans MinIO sous forme de fichiers JSON.\
✅ **Kafka Admin** : Permet de créer et supprimer des topics Kafka.\
✅ **MinIO** : Sert de stockage objet pour sauvegarder les fichiers JSON.

---

## 🛠️ Pré-requis

- **Docker & Docker Compose**
- **Python 3.x** avec `pip` installé
- **Kafka et MinIO** configurés via `docker-compose`

---

## 🚀 Installation & Démarrage

### 1️⃣ Lancer Kafka et MinIO avec Docker Compose

```sh
docker-compose up -d
```

Vérifie que les services sont bien démarrés avec :

```sh
docker ps
```

### 2️⃣ Créer un topic Kafka

```sh
python admin.py create -n transactions
```

### 3️⃣ Démarrer le Consumer Kafka

Le consumer écoute les messages et les stocke dans MinIO.

```sh
python consumer.py
```

### 4️⃣ Envoyer des fichiers JSON avec le Producer

Le producer récupère des transactions depuis une API externe et les envoie au topic Kafka `transactions`. Pour démarer le producer :

```sh
python producer.py
```

### 5️⃣ Vérifier les fichiers sur MinIO

Accède à **MinIO Console** : [http://localhost:8900](http://localhost:8900)\
Connecte-toi avec **minio / password** et vérifie que le fichier JSON est bien stocké.

---

## 📂 Structure du projet

```
📁 kafka_minio_project
│-- 📜 docker-compose.yml       # Configuration Docker pour Kafka & MinIO
│-- 📜 admin.py                 # Gestion des topics Kafka
│-- 📜 producer.py              # Producteur Kafka (envoie les fichiers JSON)
│-- 📜 consumer.py              # Consumer Kafka (stocke les fichiers dans MinIO)
│-- 📜 README.md                # Documentation du projet
│-- 📜 data.json                # Exemple de fichier JSON à envoyer
```

---

## 🛠️ Configuration

### Modifier les paramètres Kafka et MinIO

Tu peux modifier les configurations dans **docker-compose.yml** et **les fichiers Python** si besoin.

- **Kafka** tourne sur `localhost:9092`
- **MinIO** tourne sur `localhost:9000` avec accès `minio / password`

---

## 🐛 Dépannage

**Kafka ne fonctionne pas ?** 🔥\
➡️ Vérifie si Kafka est bien démarré :

```sh
docker logs kafka
```

➡️ Supprime et recrée le topic si nécessaire :

```sh
python admin.py delete -n transactions
python admin.py create -n transactions
```

**MinIO ne fonctionne pas ?** 🛠️\
➡️ Vérifie si MinIO est bien accessible :\
[http://localhost:8900](http://localhost:8900)

**Le consumer ne stocke pas les fichiers ?** 🤔\
➡️ Vérifie les logs du consumer :

```sh
python consumer.py
```
