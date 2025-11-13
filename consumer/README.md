# 💾 Consumer Kafka - Documentation

Ce dossier contient le code du Consumer Kafka qui lit les messages et les stocke dans PostgreSQL.

## 📁 Fichiers

1. **config.py** - Configuration du consumer
2. **db_manager.py** - Gestionnaire PostgreSQL
3. **kafka_consumer.py** - Consumer Kafka principal

## 🚀 Installation

Les fichiers doivent être dans le dossier `consumer/` :

```
crypto-streaming-pipeline/
└── consumer/
    ├── config.py
    ├── db_manager.py
    └── kafka_consumer.py
```

## ▶️ Lancement

```bash
# Active l'environnement virtuel
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Lance le consumer
python consumer/kafka_consumer.py
```

## 🧪 Tests

Tester la connexion PostgreSQL seule :
```bash
python consumer/db_manager.py
```

## 📊 Ce que fait le Consumer

1. Se connecte à Kafka (topic: `crypto-prices-raw`)
2. Consomme les messages en temps réel
3. Parse les données JSON
4. Stocke dans PostgreSQL par batch (100 messages)
5. Commit Kafka après insertion réussie
6. Log toutes les actions

## 🎛️ Configuration

Modifier dans le fichier `.env` :
- `BATCH_SIZE` : Taille des batchs avant insertion (défaut: 100)
- `KAFKA_CONSUMER_GROUP` : Nom du consumer group

## 📝 Logs

Les logs sont écrits dans :
- Console (stdout)
- Fichier `consumer.log`

## 🛑 Arrêt

Appuie sur `Ctrl+C` pour arrêter proprement le consumer.

Le consumer flush automatiquement le buffer avant de s'arrêter.
