# 🚀 Crypto Streaming Pipeline

Pipeline de streaming temps réel pour l'analyse de données de cryptomonnaies avec Apache Kafka, Spark Streaming, et ClickHouse.

## 📋 Table des matières

- [Architecture](#architecture)
- [Technologies](#technologies)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Monitoring](#monitoring)
- [Tests](#tests)
- [Roadmap](#roadmap)

## 🏗️ Architecture

```
┌─────────────┐
│  CoinCap    │
│  API        │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Kafka Producer     │  ← Ingestion temps réel
│  (Python)           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Apache Kafka       │  ← Message Broker
│  (Topic: crypto)    │
└──────┬──────────────┘
       │
       ├─────────────────────┐
       │                     │
       ▼                     ▼
┌──────────────┐    ┌─────────────────┐
│  PostgreSQL  │    │  Spark Streaming│
│  (Raw Data)  │    │  (Transformations)
└──────────────┘    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  ClickHouse     │
                    │  (Time-Series)  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Grafana        │
                    │  (Dashboards)   │
                    └─────────────────┘
```

## 🛠️ Technologies

- **Apache Kafka** : Message broker pour streaming
- **Apache Spark Streaming** : Traitement distribué en temps réel
- **PostgreSQL** : Base de données relationnelle pour données brutes
- **ClickHouse** : Base de données columnar pour time-series
- **Redis** : Cache in-memory
- **Grafana** : Visualisation et dashboards
- **Prometheus** : Monitoring et métriques
- **Docker** : Containerisation

## 📦 Prérequis

- Docker Desktop (ou Docker Engine + Docker Compose)
- Python 3.9+
- Au moins 8 GB de RAM disponible
- 10 GB d'espace disque

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone <votre-repo>
cd crypto-streaming-pipeline
```

### 2. Créer l'environnement Python

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Démarrer les services Docker

```bash
docker-compose up -d
```

**Vérifier que tous les services sont lancés :**

```bash
docker-compose ps
```

Vous devriez voir tous les services avec le statut "Up".

### 4. Vérifier les connexions

**Kafka UI** : http://localhost:8080  
**Grafana** : http://localhost:3000 (admin/admin)  
**Prometheus** : http://localhost:9090  
**ClickHouse** : http://localhost:8123  

## 🎯 Utilisation

### Démarrer le Producer (collecte de données)

```bash
python producer/kafka_producer.py
```

### Démarrer le Consumer (stockage PostgreSQL)

```bash
python consumer/kafka_consumer.py
```

### Démarrer Spark Streaming (transformations)

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 \
  spark/streaming_job.py
```

### Arrêter le pipeline

```bash
docker-compose down
```

Pour supprimer aussi les volumes (données) :

```bash
docker-compose down -v
```

## 📁 Structure du projet

```
crypto-streaming-pipeline/
├── producer/               # Kafka Producer (ingestion API)
│   ├── kafka_producer.py
│   ├── api_client.py
│   └── config.py
├── consumer/               # Kafka Consumer (PostgreSQL)
│   ├── kafka_consumer.py
│   └── db_manager.py
├── spark/                  # Spark Streaming jobs
│   ├── streaming_job.py
│   ├── transformations.py
│   └── clickhouse_writer.py
├── monitoring/             # Prometheus & Grafana configs
│   ├── prometheus.yml
│   └── grafana/
├── tests/                  # Tests unitaires et d'intégration
├── docs/                   # Documentation
├── config/                 # Configurations
├── data/                   # Données locales (gitignored)
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

## ✨ Fonctionnalités

### Phase 1 (Semaine 1) - ✅
- [x] Setup infrastructure Docker
- [x] Kafka Producer basique
- [x] Consommation et stockage PostgreSQL
- [x] Monitoring basique

### Phase 2 (Semaine 2) - 🚧 En cours
- [ ] Spark Streaming avec transformations
- [ ] Agrégations par fenêtre temporelle
- [ ] Moyennes mobiles
- [ ] Stockage ClickHouse

### Phase 3 (Semaine 3) - 📋 À venir
- [ ] Détection d'anomalies
- [ ] Système d'alertes
- [ ] Dashboards Grafana
- [ ] Tests automatisés
- [ ] Documentation complète

## 📊 Monitoring

### Métriques collectées

- **Kafka** : Lag, throughput, nombre de messages
- **Producer** : Taux d'envoi, erreurs, latence
- **Consumer** : Taux de consommation, erreurs
- **Bases de données** : Connexions, requêtes, latence

### Dashboards Grafana

1. **Pipeline Overview** : Vue d'ensemble du pipeline
2. **Kafka Metrics** : Métriques Kafka détaillées
3. **Crypto Prices** : Prix en temps réel
4. **Alerts Dashboard** : Alertes et anomalies

## 🧪 Tests

```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tous les tests avec couverture
pytest --cov=. tests/
```

## 📈 Roadmap

- **v1.0** : Pipeline de base fonctionnel ✅
- **v1.1** : Transformations avancées 🚧
- **v1.2** : ML pour prédictions 📋
- **v2.0** : Multi-cloud deployment 📋

## 🤝 Contribution

Contributions bienvenues ! Voir [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 Licence

MIT License

## 👤 Auteur

Data Engineer en formation - Portfolio project

## 📞 Support

Pour toute question : [Créer une issue](https://github.com/votre-repo/issues)

---

**Note** : Ce projet est à but éducatif et de démonstration de compétences data engineering.
