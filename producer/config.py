"""
Configuration du Producer Kafka pour le pipeline crypto
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# API Configuration (v3 - REST API)
COINCAP_API_URL = os.getenv('COINCAP_API_URL', 'https://rest.coincap.io/v3')
COINCAP_API_KEY = os.getenv('COINCAP_API_KEY', '')  # REQUIS pour v3 (gratuit sur pro.coincap.io)

# Liste des cryptos à tracker
CRYPTOS_TO_TRACK = os.getenv(
    'CRYPTOS_TO_TRACK',
    'bitcoin,ethereum,ripple,litecoin,cardano,polkadot,dogecoin,solana,avalanche-2,chainlink'
).split(',')

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_TOPIC_RAW = os.getenv('KAFKA_TOPIC_RAW', 'crypto-prices-raw')

# Application Configuration
DATA_FETCH_INTERVAL = int(os.getenv('DATA_FETCH_INTERVAL', 10))  # secondes
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Retry Configuration
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))  # secondes

# Monitoring (pour plus tard)
PROMETHEUS_PORT = int(os.getenv('PROMETHEUS_PORT', 8000))
METRICS_ENABLED = os.getenv('METRICS_ENABLED', 'true').lower() == 'true'

# Validation
if not CRYPTOS_TO_TRACK:
    raise ValueError("Au moins une crypto doit être configurée dans CRYPTOS_TO_TRACK")

print(f"✅ Configuration chargée:")
print(f"   - API: {COINCAP_API_URL}")
print(f"   - Kafka: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"   - Topic: {KAFKA_TOPIC_RAW}")
print(f"   - Cryptos: {len(CRYPTOS_TO_TRACK)} monnaies")
print(f"   - Intervalle: {DATA_FETCH_INTERVAL}s")
