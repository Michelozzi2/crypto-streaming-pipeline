# 📡 Producer Kafka - Documentation

Ce dossier contient le code du Producer Kafka qui récupère les données de cryptomonnaies et les envoie dans Kafka.

## 📁 Fichiers

1. **config.py** - Configuration du producer
2. **api_client.py** - Client pour l'API CoinCap
3. **kafka_producer.py** - Producer Kafka principal

## 🚀 Installation

Les fichiers doivent être dans le dossier `producer/` :

```
crypto-streaming-pipeline/
└── producer/
    ├── config.py
    ├── api_client.py
    └── kafka_producer.py
```

## ▶️ Lancement

```bash
# Active l'environnement virtuel
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Lance le producer
python producer/kafka_producer.py
```

## 🧪 Tests

Tester le client API seul :
```bash
python producer/api_client.py
```

## 📊 Ce que fait le Producer

1. Se connecte à l'API CoinCap
2. Récupère les prix de 10 cryptos toutes les 10 secondes
3. Formate les données
4. Envoie dans Kafka (topic: `crypto-prices-raw`)
5. Log toutes les actions

## 🎛️ Configuration

Modifier dans le fichier `.env` :
- `DATA_FETCH_INTERVAL` : Intervalle entre chaque récupération (secondes)
- `CRYPTOS_TO_TRACK` : Liste des cryptos séparées par virgules

## 📝 Logs

Les logs sont écrits dans :
- Console (stdout)
- Fichier `producer.log`

## 🛑 Arrêt

Appuie sur `Ctrl+C` pour arrêter proprement le producer.
