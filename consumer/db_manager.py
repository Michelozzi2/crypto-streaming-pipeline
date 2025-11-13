"""
Gestionnaire de base de données PostgreSQL
Gère les connexions et les insertions dans la base
"""
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import sql
import logging
from typing import List, Dict, Optional
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gestionnaire de connexion et d'opérations PostgreSQL
    """
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            host: Hôte PostgreSQL
            port: Port PostgreSQL
            database: Nom de la base de données
            user: Utilisateur
            password: Mot de passe
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        
    def connect(self):
        """Établit la connexion à PostgreSQL"""
        try:
            logger.info(f"🔌 Connexion à PostgreSQL {self.host}:{self.port}/{self.database}...")
            
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                # Options de connexion
                connect_timeout=10,
                options='-c statement_timeout=30000'  # 30 secondes timeout
            )
            
            # Configurer l'autocommit à False (on commit manuellement)
            self.connection.autocommit = False
            
            logger.info("✅ Connexion PostgreSQL établie")
            
            # Tester la connexion
            self.test_connection()
            
            return True
            
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur de connexion PostgreSQL: {e}")
            return False
    
    def test_connection(self):
        """Teste la connexion et affiche les infos"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                logger.info(f"📊 PostgreSQL version: {version.split(',')[0]}")
                
                # Vérifier que la table existe
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'crypto_raw'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    logger.info("✅ Table 'crypto_raw' trouvée")
                else:
                    logger.warning("⚠️  Table 'crypto_raw' n'existe pas!")
                    
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur lors du test de connexion: {e}")
    
    @contextmanager
    def get_cursor(self):
        """
        Context manager pour obtenir un curseur
        Gère automatiquement la fermeture
        """
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    
    def insert_crypto_data(self, data: Dict) -> bool:
        """
        Insère une donnée crypto dans la table crypto_raw
        
        Args:
            data: Dictionnaire avec les données crypto
            
        Returns:
            True si succès, False sinon
        """
        query = """
            INSERT INTO crypto_raw (
                symbol, price_usd, volume_24h, market_cap_usd,
                change_percent_24h, timestamp
            ) VALUES (
                %(symbol)s, %(price_usd)s, %(volume_24h)s, %(market_cap_usd)s,
                %(change_percent_24h)s, %(timestamp)s
            )
            ON CONFLICT (symbol, timestamp) DO NOTHING;
        """
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, data)
                self.connection.commit()
                return True
                
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur insertion: {e}")
            self.connection.rollback()
            return False
    
    def insert_crypto_data_batch(self, data_list: List[Dict]) -> int:
        """
        Insère plusieurs données crypto en batch (plus performant)
        
        Args:
            data_list: Liste de dictionnaires avec les données
            
        Returns:
            Nombre de lignes insérées
        """
        if not data_list:
            return 0
        
        query = """
            INSERT INTO crypto_raw (
                symbol, price_usd, volume_24h, market_cap_usd,
                change_percent_24h, timestamp
            ) VALUES (
                %(symbol)s, %(price_usd)s, %(volume_24h)s, %(market_cap_usd)s,
                %(change_percent_24h)s, %(timestamp)s
            )
            ON CONFLICT (symbol, timestamp) DO NOTHING;
        """
        
        try:
            with self.get_cursor() as cursor:
                # execute_batch est plus performant que des INSERT individuels
                execute_batch(cursor, query, data_list, page_size=100)
                self.connection.commit()
                
                rows_inserted = cursor.rowcount
                logger.info(f"✅ Inséré {rows_inserted} lignes (sur {len(data_list)} messages)")
                return rows_inserted
                
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur insertion batch: {e}")
            self.connection.rollback()
            return 0
    
    def get_latest_prices(self, limit: int = 10) -> List[Dict]:
        """
        Récupère les derniers prix enregistrés
        
        Args:
            limit: Nombre de résultats
            
        Returns:
            Liste de dictionnaires avec les données
        """
        query = """
            SELECT 
                symbol, 
                price_usd, 
                volume_24h,
                market_cap_usd,
                change_percent_24h,
                to_timestamp(timestamp/1000) as datetime,
                created_at
            FROM crypto_raw
            ORDER BY created_at DESC
            LIMIT %s;
        """
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, (limit,))
                columns = [desc[0] for desc in cursor.description]
                results = []
                
                for row in cursor.fetchall():
                    results.append(dict(zip(columns, row)))
                
                return results
                
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur requête: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Récupère des statistiques sur les données stockées
        
        Returns:
            Dictionnaire avec les stats
        """
        query = """
            SELECT 
                COUNT(*) as total_rows,
                COUNT(DISTINCT symbol) as total_cryptos,
                MIN(created_at) as first_insert,
                MAX(created_at) as last_insert
            FROM crypto_raw;
        """
        
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                row = cursor.fetchone()
                
                return dict(zip(columns, row))
                
        except psycopg2.Error as e:
            logger.error(f"❌ Erreur requête stats: {e}")
            return {}
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            logger.info("🔌 Connexion PostgreSQL fermée")


# Fonction de test
def test_database():
    """Fonction de test du gestionnaire de base de données"""
    from config import (
        POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,
        POSTGRES_USER, POSTGRES_PASSWORD
    )
    
    print("\n🧪 Test du gestionnaire de base de données\n")
    print("=" * 60)
    
    # Créer le gestionnaire
    db = DatabaseManager(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    
    # Test 1: Connexion
    print("\n1️⃣ Test: Connexion à PostgreSQL")
    if db.connect():
        print("   ✅ Connexion réussie")
    else:
        print("   ❌ Échec de connexion")
        return
    
    # Test 2: Insertion d'une donnée test
    print("\n2️⃣ Test: Insertion d'une donnée")
    test_data = {
        'symbol': 'TEST',
        'price_usd': 42000.50,
        'volume_24h': 1000000.0,
        'market_cap_usd': 800000000000.0,
        'change_percent_24h': 2.5,
        'timestamp': 1699876543000
    }
    
    if db.insert_crypto_data(test_data):
        print("   ✅ Insertion réussie")
    else:
        print("   ❌ Échec d'insertion")
    
    # Test 3: Récupérer les statistiques
    print("\n3️⃣ Test: Statistiques")
    stats = db.get_statistics()
    if stats:
        print(f"   ✅ Total lignes: {stats.get('total_rows', 0)}")
        print(f"   📊 Cryptos uniques: {stats.get('total_cryptos', 0)}")
    
    # Test 4: Récupérer les derniers prix
    print("\n4️⃣ Test: Derniers prix")
    latest = db.get_latest_prices(5)
    if latest:
        print(f"   ✅ Récupéré {len(latest)} lignes")
        for row in latest[:3]:
            print(f"      • {row['symbol']}: ${row['price_usd']}")
    
    # Fermeture
    db.close()
    print("\n" + "=" * 60)
    print("✅ Tests terminés\n")


if __name__ == "__main__":
    # Configuration du logging pour les tests
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_database()
