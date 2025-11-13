"""
Consumer Kafka pour le pipeline crypto streaming
Consomme les messages de Kafka et les stocke dans PostgreSQL
"""
import json
import logging
import signal
import sys
import time
from typing import List, Dict
from datetime import datetime

from kafka import KafkaConsumer
from kafka.errors import KafkaError

# Import de nos modules
import config
from db_manager import DatabaseManager

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('consumer.log')
    ]
)
logger = logging.getLogger(__name__)


class CryptoKafkaConsumer:
    """
    Consumer Kafka pour les données crypto
    """
    
    def __init__(self):
        """Initialise le consumer"""
        self.running = False
        self.consumer = None
        self.db_manager = None
        
        # Statistiques
        self.messages_consumed = 0
        self.messages_stored = 0
        self.errors = 0
        self.start_time = None
        
        # Buffer pour le batch processing
        self.message_buffer: List[Dict] = []
    
    def setup(self):
        """Configure le consumer Kafka et la base de données"""
        try:
            logger.info("🚀 Démarrage du Consumer Crypto Kafka")
            logger.info("=" * 60)
            
            # 1. Connexion à PostgreSQL
            logger.info("💾 Connexion à PostgreSQL...")
            self.db_manager = DatabaseManager(
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                database=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD
            )
            
            if not self.db_manager.connect():
                raise Exception("Impossible de se connecter à PostgreSQL")
            
            # 2. Initialiser le consumer Kafka
            logger.info("🔌 Connexion à Kafka...")
            self.consumer = KafkaConsumer(
                config.KAFKA_TOPIC_RAW,
                bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
                
                # Consumer group (pour la scalabilité)
                group_id=config.KAFKA_CONSUMER_GROUP,
                
                # Désérialisation
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                
                # Configuration de consommation
                auto_offset_reset='earliest',  # Commence au début si nouveau consumer
                enable_auto_commit=config.CONSUMER_ENABLE_AUTO_COMMIT,
                max_poll_records=config.CONSUMER_MAX_POLL_RECORDS,
                
                # Timeouts
                session_timeout_ms=30000,
                heartbeat_interval_ms=10000,
                max_poll_interval_ms=300000  # 5 minutes
            )
            
            logger.info("✅ Consumer Kafka initialisé")
            logger.info("=" * 60)
            logger.info(f"📊 Configuration:")
            logger.info(f"   • Kafka: {config.KAFKA_BOOTSTRAP_SERVERS}")
            logger.info(f"   • Topic: {config.KAFKA_TOPIC_RAW}")
            logger.info(f"   • Consumer Group: {config.KAFKA_CONSUMER_GROUP}")
            logger.info(f"   • Batch Size: {config.BATCH_SIZE}")
            logger.info(f"   • PostgreSQL: {config.POSTGRES_HOST}:{config.POSTGRES_PORT}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'initialisation: {e}")
            return False
    
    def process_message(self, message) -> bool:
        """
        Traite un message Kafka
        
        Args:
            message: Message Kafka
            
        Returns:
            True si traité avec succès
        """
        try:
            # Extraire les données
            data = message.value
            key = message.key
            
            logger.debug(
                f"📨 Message reçu: {key} "
                f"(partition {message.partition}, offset {message.offset})"
            )
            
            # Préparer les données pour PostgreSQL
            db_data = {
                'symbol': data.get('symbol', 'UNKNOWN'),
                'price_usd': float(data.get('price_usd', 0)),
                'volume_24h': float(data.get('volume_24h', 0)),
                'market_cap_usd': float(data.get('market_cap_usd', 0)),
                'change_percent_24h': float(data.get('change_percent_24h', 0)),
                'timestamp': int(data.get('timestamp', 0))
            }
            
            # Ajouter au buffer
            self.message_buffer.append(db_data)
            self.messages_consumed += 1
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur traitement message: {e}")
            self.errors += 1
            return False
    
    def flush_buffer(self) -> bool:
        """
        Vide le buffer en base de données (batch insert)
        
        Returns:
            True si succès
        """
        if not self.message_buffer:
            return True
        
        try:
            # Insertion en batch
            rows_inserted = self.db_manager.insert_crypto_data_batch(
                self.message_buffer
            )
            
            self.messages_stored += rows_inserted
            
            # Vider le buffer
            self.message_buffer.clear()
            
            # Commit Kafka (on a bien traité ces messages)
            if not config.CONSUMER_ENABLE_AUTO_COMMIT:
                self.consumer.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur flush buffer: {e}")
            self.errors += 1
            return False
    
    def run(self):
        """
        Boucle principale du consumer
        """
        if not self.setup():
            logger.error("❌ Échec de l'initialisation")
            return
        
        self.running = True
        self.start_time = time.time()
        
        logger.info("🏃 Démarrage de la consommation")
        logger.info("   Appuie sur Ctrl+C pour arrêter\n")
        
        try:
            # Boucle de consommation
            for message in self.consumer:
                if not self.running:
                    break
                
                # Traiter le message
                self.process_message(message)
                
                # Flush le buffer si on atteint la taille de batch
                if len(self.message_buffer) >= config.BATCH_SIZE:
                    self.flush_buffer()
                    
                    # Log des stats toutes les X insertions
                    if self.messages_stored % (config.BATCH_SIZE * 5) == 0:
                        self.print_stats()
        
        except KeyboardInterrupt:
            logger.info("\n\n⚠️  Interruption clavier détectée")
        except Exception as e:
            logger.error(f"❌ Erreur fatale: {e}")
        finally:
            # Flush les messages restants
            if self.message_buffer:
                logger.info(f"📤 Flush des {len(self.message_buffer)} messages restants...")
                self.flush_buffer()
            
            self.shutdown()
    
    def print_stats(self):
        """Affiche les statistiques"""
        if self.start_time:
            duration = time.time() - self.start_time
            rate_consumed = self.messages_consumed / duration if duration > 0 else 0
            rate_stored = self.messages_stored / duration if duration > 0 else 0
            
            logger.info("=" * 60)
            logger.info("📊 Statistiques temps réel:")
            logger.info(f"   • Messages consommés: {self.messages_consumed}")
            logger.info(f"   • Messages stockés: {self.messages_stored}")
            logger.info(f"   • Buffer actuel: {len(self.message_buffer)}")
            logger.info(f"   • Erreurs: {self.errors}")
            logger.info(f"   • Taux consommation: {rate_consumed:.2f} msg/s")
            logger.info(f"   • Taux stockage: {rate_stored:.2f} msg/s")
            logger.info(f"   • Durée: {duration:.2f}s")
            logger.info("=" * 60)
    
    def shutdown(self):
        """Arrêt propre du consumer"""
        logger.info("\n" + "=" * 60)
        logger.info("🛑 Arrêt du consumer...")
        
        self.running = False
        
        # Statistiques finales
        self.print_stats()
        
        # Statistiques base de données
        if self.db_manager:
            logger.info("\n📊 Statistiques base de données:")
            stats = self.db_manager.get_statistics()
            if stats:
                logger.info(f"   • Total lignes: {stats.get('total_rows', 0)}")
                logger.info(f"   • Cryptos uniques: {stats.get('total_cryptos', 0)}")
                logger.info(f"   • Première insertion: {stats.get('first_insert', 'N/A')}")
                logger.info(f"   • Dernière insertion: {stats.get('last_insert', 'N/A')}")
        
        # Fermer les connexions
        if self.consumer:
            logger.info("🔌 Fermeture du consumer Kafka...")
            self.consumer.close()
        
        if self.db_manager:
            self.db_manager.close()
        
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
    
    # Créer et lancer le consumer
    consumer = CryptoKafkaConsumer()
    consumer.run()


if __name__ == "__main__":
    main()
