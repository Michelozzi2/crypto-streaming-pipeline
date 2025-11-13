"""
Configuration du Consumer Kafka pour le pipeline crypto
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC_RAW = os.getenv('KAFKA_TOPIC_RAW', 'crypto-prices-raw')
KAFKA_CONSUMER_GROUP = os.getenv('KAFKA_CONSUMER_GROUP', 'crypto-consumer-group')

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5433))  # 5433 car on a changé le port
POSTGRES_DB = os.getenv('POSTGRES_DB', 'crypto_data')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'crypto_user')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'crypto_password')

# Application Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))  # Nombre de messages avant commit DB

# Consumer Configuration
CONSUMER_AUTO_COMMIT = False  # On commit manuellement après insertion DB
CONSUMER_ENABLE_AUTO_COMMIT = False
CONSUMER_MAX_POLL_RECORDS = 500  # Nombre max de messages par poll

print(f"✅ Configuration Consumer chargée:")
print(f"   - Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"   - Topic: {KAFKA_TOPIC_RAW}")
print(f"   - Consumer Group: {KAFKA_CONSUMER_GROUP}")
print(f"   - PostgreSQL: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")
