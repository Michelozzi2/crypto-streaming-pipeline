# 🎉 COMMENCER ICI - Guide de démarrage rapide

## ✅ Tu as téléchargé le projet !

Bravo ! Tu as maintenant tous les fichiers nécessaires pour créer un **pipeline de streaming temps réel** professionnel.

---

## 🎯 Qu'est-ce que ce projet ?

Un système complet qui :
1. **Récupère** les prix de cryptomonnaies en temps réel (API CoinCap)
2. **Ingère** les données via Apache Kafka
3. **Transforme** avec Spark Streaming (moyennes, agrégations, alertes)
4. **Stocke** dans PostgreSQL et ClickHouse
5. **Visualise** sur des dashboards Grafana en temps réel

**Résultat :** Un projet portfolio qui impressionne les recruteurs et décroche des missions freelance !

---

## 📋 PRÉREQUIS (15 minutes)

### 1. Docker Desktop
- **Mac** : https://docs.docker.com/desktop/install/mac-install/
- **Windows** : https://docs.docker.com/desktop/install/windows-install/
- **Linux** : https://docs.docker.com/desktop/install/linux-install/

**Vérification :**
```bash
docker --version
# Devrait afficher : Docker version 24.x.x ou plus
```

### 2. Python 3.9+
- **Télécharge** : https://www.python.org/downloads/
- ⚠️ **Windows** : Coche "Add Python to PATH" pendant l'installation

**Vérification :**
```bash
python --version
# ou sur Mac/Linux :
python3 --version
# Devrait afficher : Python 3.9.x ou plus
```

---

## 🚀 DÉMARRAGE RAPIDE (10 minutes)

### Étape 1 : Ouvre un terminal dans le dossier du projet

```bash
cd chemin/vers/crypto-streaming-pipeline
```

### Étape 2 : Lance tout automatiquement

**Sur Mac/Linux :**
```bash
chmod +x start.sh
./start.sh
```

**Sur Windows :**
```bash
start.bat
```

Ce script va :
- ✅ Créer un environnement virtuel Python
- ✅ Installer toutes les dépendances
- ✅ Démarrer tous les services Docker (Kafka, PostgreSQL, etc.)
- ✅ Afficher les URLs des interfaces web

⏱️ **Attends 1-2 minutes** que tous les services démarrent...

---

## 🌐 VÉRIFICATION (5 minutes)

Ouvre ces URLs dans ton navigateur :

### 1. Kafka UI - http://localhost:8080
Interface pour visualiser Kafka (topics, messages, consumers)
- Tu devrais voir une interface web
- Pas de topics pour l'instant, c'est normal !

### 2. Grafana - http://localhost:3000
Dashboards et visualisations
- Login : `admin`
- Password : `admin`
- Tu peux changer le mot de passe ou skip

### 3. Prometheus - http://localhost:9090
Monitoring et métriques
- Interface de recherche de métriques

### 4. ClickHouse - http://localhost:8123
Base de données columnar
- Tu devrais voir juste "Ok."

**✅ Si les 4 interfaces fonctionnent, tout est OK !**

---

## 🎓 PROCHAINE ÉTAPE : Coder le Producer Kafka

Maintenant que l'infrastructure tourne, on va créer le **Producer** qui :
1. Se connecte à l'API CoinCap
2. Récupère les prix de 10 cryptos toutes les 10 secondes
3. Envoie les données dans Kafka

**Reviens me voir et on code ça ensemble !**

---

## 📚 DOCUMENTATION

**Lis ces fichiers dans l'ordre :**

1. **GUIDE_DEMARRAGE.md** - Explications détaillées de ce qui a été créé
2. **CHECKLIST.md** - Planning complet des 3 semaines
3. **README.md** - Documentation technique
4. **RESSOURCES.md** - Liens utiles et tutoriels

---

## ⚠️ PROBLÈMES COURANTS

### "Docker n'est pas lancé"
**Solution :** Lance Docker Desktop et attends qu'il soit complètement démarré (icône dans la barre)

### "Port 5432 already in use"
**Solution :** Tu as déjà PostgreSQL qui tourne
```bash
# Arrête PostgreSQL local ou change le port dans docker-compose.yml
```

### "Python not found"
**Solution :** 
- Windows : Réinstalle Python en cochant "Add to PATH"
- Mac/Linux : Utilise `python3` au lieu de `python`

### Les services ne démarrent pas
```bash
# Voir les logs
docker-compose logs

# Redémarrer un service
docker-compose restart nom_du_service

# Tout redémarrer
docker-compose down
docker-compose up -d
```

---

## 💡 CONSEILS

### 1. Utilise un bon éditeur de code
**Visual Studio Code** (gratuit) : https://code.visualstudio.com/

Extensions recommandées :
- Python
- Docker
- SQL (PostgreSQL)
- GitLens

### 2. Prends des notes
Crée un fichier `MES_NOTES.md` où tu notes :
- Ce que tu apprends
- Les problèmes rencontrés
- Les solutions

### 3. Fais des commits Git réguliers
```bash
git init
git add .
git commit -m "Initial setup"
```

---

## 🎯 OBJECTIF DE LA SEMAINE 1

À la fin de la semaine 1, tu auras :
- ✅ Infrastructure complète qui tourne (FAIT !)
- 🎯 Producer qui envoie des données dans Kafka
- 🎯 Consumer qui stocke dans PostgreSQL
- 🎯 Premières visualisations dans Kafka UI

**Durée : 10h réparties sur 7 jours**

---

## 📊 CE QUE TU VAS APPRENDRE

### Technologies
✅ Apache Kafka (streaming)
✅ Apache Spark (traitement distribué)
✅ PostgreSQL (SQL)
✅ ClickHouse (columnar DB)
✅ Docker & Docker Compose
✅ Prometheus & Grafana
✅ Python async programming

### Compétences
✅ Architecture event-driven
✅ ETL temps réel
✅ Data modeling time-series
✅ Monitoring et observabilité
✅ Tests et documentation

**Ces compétences te permettront de décrocher des missions à 400-500€/jour !**

---

## 🎉 FÉLICITATIONS !

Tu as configuré une infrastructure data engineering professionnelle identique à celle de Netflix, Uber, ou Spotify.

**Maintenant, on passe à l'action !**

**Reviens me voir pour créer le Producer Kafka ! 🚀**

---

## 📞 Besoin d'aide ?

Si tu es bloqué :
1. Vérifie les logs : `docker-compose logs nom_service`
2. Consulte GUIDE_DEMARRAGE.md
3. Reviens me demander de l'aide !

---

**Date de début :** ___________  
**Infrastructure OK :** ☐ Oui ☐ Non  
**Prêt pour le Producer :** ☐ Oui ☐ Pas encore
