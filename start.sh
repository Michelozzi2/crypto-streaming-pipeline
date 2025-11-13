#!/bin/bash

echo "🚀 Crypto Streaming Pipeline - Démarrage"
echo "========================================"
echo ""

# Vérification Docker
echo "➡️  Vérification de Docker..."
if ! docker ps &> /dev/null; then
    echo "❌ Docker n'est pas lancé. Lance Docker Desktop d'abord."
    exit 1
fi
echo "✅ Docker est prêt!"

# Vérification Python
echo "➡️  Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé."
    exit 1
fi
echo "✅ Python détecté"

# Création environnement virtuel
echo "➡️  Création de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
else
    echo "✅ Environnement virtuel existant"
fi

# Installation dépendances
echo "➡️  Installation des dépendances..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dépendances installées"

# Démarrage Docker
echo "➡️  Démarrage des services Docker..."
docker-compose up -d

echo ""
echo "========================================"
echo "🎉 Infrastructure démarrée !"
echo "========================================"
echo ""
echo "📊 Interfaces Web :"
echo "  • Kafka UI:    http://localhost:8080"
echo "  • Grafana:     http://localhost:3000 (admin/admin)"
echo "  • Prometheus:  http://localhost:9090"
echo "  • ClickHouse:  http://localhost:8123"
echo ""
echo "📝 Prochaines étapes :"
echo "  1. Vérifie les interfaces web"
echo "  2. Lance : python producer/kafka_producer.py"
echo ""
