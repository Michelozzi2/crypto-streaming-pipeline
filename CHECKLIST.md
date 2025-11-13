# 📋 Checklist de Progression - Pipeline Crypto Streaming

## Semaine 1 : Fondations (10h)

### Jour 1-2 : Setup Environnement (4h)
- [x] Télécharger et décompresser le projet
- [x] Installer Docker Desktop
- [x] Lancer `./start.sh` (Mac/Linux) ou `start.bat` (Windows)
- [x] Vérifier tous les services : `docker-compose ps`
- [x] Accéder à Kafka UI : http://localhost:8080
- [x] Accéder à Grafana : http://localhost:3000 (admin/admin)
- [x] Accéder à Prometheus : http://localhost:9090
- [x] Créer un environnement virtuel Python
- [x] Installer les dépendances : `pip install -r requirements.txt`

**✍️ Notes :**
```
Date de début : 11/11/2025
Problèmes rencontrés :
Petit problème au lancement de Prometheus

Solutions trouvées :
La configuration de stockage/retention ne se met pas dans prometheus.yml. Utiliser les flags de démarrage (--storage.tsdb.path et --storage.tsdb.retention.time) dans docker-compose ou le command d’exécution du conteneur.


```

---

### Jour 3-4 : Kafka Producer (4h)
- [ ] Comprendre l'architecture du Producer
- [ ] Créer `producer/config.py`
- [ ] Créer `producer/api_client.py`
- [ ] Créer `producer/kafka_producer.py`
- [ ] Tester la connexion à l'API CoinCap
- [ ] Tester l'envoi de messages dans Kafka
- [ ] Visualiser les messages dans Kafka UI
- [ ] Ajouter le monitoring Prometheus

**📝 Compétences acquises :**
```
- Connexion à une API REST : ☐ Compris ☐ Appliqué ☐ Maîtrisé
- Kafka Producer basics : ☐ Compris ☐ Appliqué ☐ Maîtrisé
- Gestion erreurs/retry : ☐ Compris ☐ Appliqué ☐ Maîtrisé
- Monitoring Prometheus : ☐ Compris ☐ Appliqué ☐ Maîtrisé
```

---

### Jour 5-7 : Kafka Consumer + PostgreSQL (2h)
- [ ] Créer `consumer/db_manager.py`
- [ ] Créer `consumer/kafka_consumer.py`
- [ ] Tester la consommation depuis Kafka
- [ ] Vérifier l'insertion dans PostgreSQL
- [ ] Requêtes SQL pour voir les données
- [ ] Ajouter logs et monitoring

---

## Semaine 2 : Transformations (10h)

### Jour 1-2 : Spark Streaming Setup (4h)
- [ ] Installer et configurer Spark
- [ ] Créer `spark/config.py`
- [ ] Premier job Spark : lecture Kafka
- [ ] Test d'affichage dans la console

### Jour 3-4 : Transformations Métier (4h)
- [ ] Implémenter les fenêtres temporelles (5min)
- [ ] Calculer les agrégations (min, max, avg)
- [ ] Calculer les moyennes mobiles
- [ ] Détecter les variations > 5%

### Jour 5-7 : ClickHouse Integration (2h)
- [ ] Écrire les données dans ClickHouse
- [ ] Vérifier les données
- [ ] Requêtes analytiques de test

---

## Semaine 3 : Production & Portfolio (10h)

### Jour 1-2 : Monitoring Avancé (3h)
- [ ] Configurer les métriques Prometheus
- [ ] Créer des alertes
- [ ] Dashboard Grafana infrastructure

### Jour 3-4 : Dashboard Business (4h)
- [ ] Créer dashboard Grafana crypto
- [ ] Graphiques temps réel
- [ ] Visualisations

### Jour 5-7 : Finalisation Portfolio (3h)
- [ ] Tests unitaires (pytest)
- [ ] Documentation technique complète
- [ ] Video démo (2-3 min)
- [ ] Article LinkedIn/Medium
- [ ] Push sur GitHub

---

**Date de début du projet :** ___________
**Date de fin prévue :** ___________

**🎉 Bon courage !**
