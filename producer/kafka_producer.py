"""
Producer Kafka pour le pipeline crypto streaming
Récupère les données de l'API CoinCap et les envoie dans Kafka
"""
import json
import time
import logging
import signal
import sys
from typing import Optional
from datetime import datetime

from kafka import KafkaProducer
from kafka.errors import KafkaError

# Import de nos modules
import config
from api_client import CoinCapAPIClient

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('producer.log', encoding='utf-8')
    ]
)
# Force UTF-8 pour stdout sur Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
logger = logging.getLogger(__name__)


class CryptoKafkaProducer:
    """
    Producer Kafka pour les données crypto
    """
    
    def __init__(self):
        """Initialise le producer Kafka et le client API"""
        self.running = False
        self.producer: Optional[KafkaProducer] = None
        self.api_client: Optional[CoinCapAPIClient] = None
        
        # Statistiques
        self.messages_sent = 0
        self.errors = 0
        self.start_time = None
        
    def setup(self):
        """Configure le producer Kafka et le client API"""
        try:
            logger.info("🚀 Démarrage du Producer Crypto Kafka")
            logger.info("=" * 60)
            
            # 1. Initialiser le client API
            logger.info("📡 Connexion à l'API CoinCap...")
            self.api_client = CoinCapAPIClient(
                base_url=config.COINCAP_API_URL,
                api_key=config.COINCAP_API_KEY
            )
            
            # 2. Initialiser le producer Kafka
            logger.info("🔌 Connexion à Kafka...")
            self.producer = KafkaProducer(
                bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                
                # Sérialisation en JSON
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                
                # Configuration de performance
                acks='all',  # Attend confirmation de tous les replicas
                retries=3,   # Retry automatique
                max_in_flight_requests_per_connection=5,
                
                # Compression pour économiser la bande passante
                compression_type='gzip',
                
                # Batching pour meilleures performances
                linger_ms=10,
                batch_size=16384
            )
            
            logger.info("✅ Producer Kafka initialisé")
            logger.info("=" * 60)
            logger.info(f"📊 Configuration:")
            logger.info(f"   • Kafka: {config.KAFKA_BOOTSTRAP_SERVERS}")
            logger.info(f"   • Topic: {config.KAFKA_TOPIC_RAW}")
            logger.info(f"   • Cryptos: {len(config.CRYPTOS_TO_TRACK)}")
            logger.info(f"   • Intervalle: {config.DATA_FETCH_INTERVAL}s")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation: {e}")
            return False
    
    def send_to_kafka(self, data: dict) -> bool:
        """
        Envoie un message à Kafka
        
        Args:
            data: Données à envoyer
            
        Returns:
            True si succès, False sinon
        """
        try:
            # Utiliser le symbol comme clé pour le partitioning
            key = data.get('symbol', 'UNKNOWN')
            
            # Envoyer le message
            future = self.producer.send(
                config.KAFKA_TOPIC_RAW,
                key=key,
                value=data
            )
            
            # Attendre la confirmation (avec timeout)
            record_metadata = future.get(timeout=10)
            
            logger.debug(
                f"📤 Message envoyé: {key} "
                f"→ partition {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )
            
            self.messages_sent += 1
            return True
            
        except KafkaError as e:
            logger.error(f"❌ Erreur Kafka: {e}")
            self.errors += 1
            return False
        except Exception as e:
            logger.error(f"❌ Erreur inattendue: {e}")
            self.errors += 1
            return False
    
    def fetch_and_send(self):
        """
        Récupère les données de l'API et les envoie à Kafka
        """
        try:
            logger.info(f"📊 Récupération de {len(config.CRYPTOS_TO_TRACK)} cryptos...")
            
            # Récupérer les données
            raw_data = self.api_client.get_multiple_assets(config.CRYPTOS_TO_TRACK)
            
            if not raw_data:
                logger.warning("⚠️  Aucune donnée récupérée")
                return
            
            # Envoyer chaque crypto à Kafka
            success_count = 0
            for item in raw_data:
                formatted = self.api_client.format_for_kafka(item)
                if formatted and self.send_to_kafka(formatted):
                    success_count += 1
            
            # Log du résultat
            logger.info(
                f"✅ Envoyé {success_count}/{len(raw_data)} messages | "
                f"Total: {self.messages_sent} | Erreurs: {self.errors}"
            )
            
        except Exception as e:
            logger.error(f"❌ Erreur dans fetch_and_send: {e}")
            self.errors += 1
    
    def run(self):
        """
        Boucle principale du producer
        """
        if not self.setup():
            logger.error("❌ Échec de l'initialisation")
            return
        
        self.running = True
        self.start_time = time.time()
        
        logger.info("🏃 Démarrage de la boucle principale")
        logger.info("   Appuie sur Ctrl+C pour arrêter\n")
        
        iteration = 0
        
        try:
            while self.running:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"🔄 Itération #{iteration}")
                logger.info(f"{'='*60}")
                
                # Récupérer et envoyer les données
                self.fetch_and_send()
                
                # Attendre avant la prochaine itération
                logger.info(f"⏳ Pause de {config.DATA_FETCH_INTERVAL}s...\n")
                time.sleep(config.DATA_FETCH_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("\n\n⚠️  Interruption clavier détectée")
        except Exception as e:
            logger.error(f"❌ Erreur fatale: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Arrêt propre du producer"""
        logger.info("\n" + "=" * 60)
        logger.info("🛑 Arrêt du producer...")
        
        self.running = False
        
        # Statistiques finales
        if self.start_time:
            duration = time.time() - self.start_time
            rate = self.messages_sent / duration if duration > 0 else 0
            
            logger.info("📊 Statistiques finales:")
            logger.info(f"   • Durée: {duration:.2f}s")
            logger.info(f"   • Messages envoyés: {self.messages_sent}")
            logger.info(f"   • Erreurs: {self.errors}")
            logger.info(f"   • Taux: {rate:.2f} msg/s")
        
        # Fermer les connexions
        if self.producer:
            logger.info("🔌 Fermeture du producer Kafka...")
            self.producer.flush()
            self.producer.close()
        
        if self.api_client:
            self.api_client.close()
        
        logger.info("✅ Arrêt terminé")
        logger.info("=" * 60)


def signal_handler(sig, frame):
    """Gestion des signaux système (Ctrl+C)"""
    logger.info("\n⚠️  Signal reçu, arrêt en cours...")
    sys.exit(0)


def main():
    """Point d'entrée principal"""
    # Gérer Ctrl+C proprement
    signal.signal(signal.SIGINT, signal_handler)
    
    # Créer et lancer le producer
    producer = CryptoKafkaProducer()
    producer.run()


if __name__ == "__main__":
    main()
