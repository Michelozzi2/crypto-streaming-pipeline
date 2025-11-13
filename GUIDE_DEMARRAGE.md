# 🎉 SETUP TERMINÉ - Guide de démarrage

## ✅ Ce qui a été créé

### 1. Infrastructure Docker (docker-compose.yml)
- **Kafka + Zookeeper** : Pour le streaming de messages
- **Kafka UI** : Interface web pour visualiser Kafka
- **PostgreSQL** : Base de données pour données brutes
- **ClickHouse** : Base columnar pour time-series
- **Redis** : Cache in-memory
- **Grafana** : Dashboards et visualisation
- **Prometheus** : Monitoring et métriques

### 2. Scripts d'initialisation
- **init-db.sql** : Crée les tables PostgreSQL
  - crypto_raw : données brutes
  - crypto_aggregated_5m : agrégations 5 minutes
  - crypto_alerts : alertes de variations
  - crypto_moving_averages : moyennes mobiles
  - crypto_metadata : métadonnées des cryptos

- **clickhouse-init.sql** : Crée les tables ClickHouse
  - crypto.prices : données time-series
  - crypto.ohlc_5m : agrégations OHLC 5 minutes
  - crypto.ohlc_1h : agrégations OHLC 1 heure
  - Vues matérialisées pour calculs automatiques

### 3. Configuration
- **prometheus.yml** : Config monitoring
- **.env** : Variables d'environnement
- **requirements.txt** : Dépendances Python
- **.gitignore** : Fichiers à ignorer
- **README.md** : Documentation du projet

## 🚀 PROCHAINES ÉTAPES

### Étape 1 : Démarrer l'infrastructure (5 min)

```bash
# 1. Ouvre un terminal dans le dossier du projet
cd crypto-streaming-pipeline

# 2. Lance Docker Desktop (ou Docker Engine)

# 3. Démarre tous les services
docker-compose up -d

# 4. Vérifie que tout est bien lancé
docker-compose ps

# Attends 30-60 secondes que tout soit prêt
```

### Étape 2 : Vérifier les interfaces web (2 min)

Ouvre ces URLs dans ton navigateur :

1. **Kafka UI** : http://localhost:8080
   - Tu devrais voir l'interface Kafka (pas de topics pour l'instant, c'est normal)

2. **Grafana** : http://localhost:3000
   - Login : admin / admin
   - Tu peux changer le mot de passe ou skip

3. **Prometheus** : http://localhost:9090
   - Interface de monitoring

4. **ClickHouse** : http://localhost:8123
   - Tu devrais voir "Ok."

### Étape 3 : Setup Python (3 min)

```bash
# 1. Crée un environnement virtuel Python
python -m venv venv

# 2. Active l'environnement
# Sur Mac/Linux :
source venv/bin/activate
# Sur Windows :
venv\Scripts\activate

# 3. Installe les dépendances
pip install -r requirements.txt
```

## 📝 Ce qu'on va faire MAINTENANT

### Prochaine session : Créer le Kafka Producer

On va créer le script Python qui :
1. Se connecte à l'API CoinCap
2. Récupère les prix de 10 cryptos toutes les 10 secondes
3. Envoie les données dans Kafka

**Fichiers à créer :**
- `producer/kafka_producer.py` : Producer principal
- `producer/api_client.py` : Client pour l'API CoinCap
- `producer/config.py` : Configuration

**Ce que tu vas apprendre :**
- Comment se connecter à une API REST
- Comment produire des messages dans Kafka
- Gestion des erreurs et retry logic
- Monitoring avec Prometheus

## 🎓 Concepts importants à retenir

### Kafka
- **Topic** : Canal de messages (comme une file d'attente)
- **Producer** : Envoie des messages dans un topic
- **Consumer** : Lit les messages d'un topic
- **Broker** : Serveur Kafka qui gère les topics

### Architecture
```
API → Producer → Kafka Topic → Consumer → Database
```

### Notre flux
```
CoinCap API → Python Producer → Kafka Topic "crypto-prices-raw"
                                       ↓
                                  Consumer → PostgreSQL
```

## ⚠️ Problèmes courants

### Docker ne démarre pas
```bash
# Vérifie que Docker est lancé
docker ps

# Redémarre Docker Desktop
```

### Port déjà utilisé (ex: 5432, 9092)
```bash
# Trouve le processus qui utilise le port
# Mac/Linux :
lsof -i :5432
# Windows :
netstat -ano | findstr :5432

# Arrête le processus ou change le port dans docker-compose.yml
```

### Python venv ne fonctionne pas
```bash
# Assure-toi d'avoir Python 3.9+
python --version

# Sur Windows, tu dois peut-être faire :
python -m pip install --upgrade pip
```

## 📊 Status actuel

```
✅ Infrastructure Docker configurée
✅ Bases de données initialisées
✅ Monitoring en place
✅ Configuration prête

🚧 À venir (prochaine session) :
   - Producer Kafka
   - Consumer Kafka
   - Spark Streaming
```

## 💡 Conseils

1. **Prends le temps** : Ne rush pas, comprends chaque étape
2. **Teste régulièrement** : Vérifie que chaque composant fonctionne
3. **Lis les logs** : `docker-compose logs -f nom_service`
4. **Documente** : Note ce que tu apprends dans un fichier NOTES.md

## 🎯 Objectif de la semaine 1

À la fin de la semaine 1, tu auras :
- ✅ Infrastructure complète qui tourne
- 🎯 Producer qui envoie des données dans Kafka
- 🎯 Consumer qui stocke dans PostgreSQL
- 🎯 Dashboard Kafka UI qui montre le flux

## 📞 Besoin d'aide ?

Si quelque chose ne marche pas :
1. Vérifie les logs : `docker-compose logs nom_service`
2. Vérifie que Docker a assez de RAM (8GB minimum)
3. Redémarre les services : `docker-compose restart`
4. En dernier recours : `docker-compose down -v && docker-compose up -d`

---

**🎉 FÉLICITATIONS !** Tu as configuré une infrastructure data engineering professionnelle !

**Prêt pour la suite ?** Dis-moi quand tu veux qu'on code le Producer Kafka ! 🚀
