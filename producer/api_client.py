"""
Client pour l'API CoinCap
Gère les appels HTTP et les transformations de données
"""
import requests
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CoinCapAPIClient:
    """
    Client pour interagir avec l'API CoinCap
    
    Documentation API: https://docs.coincap.io/
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialise le client API
        
        Args:
            base_url: URL de base de l'API CoinCap
            api_key: Clé API (optionnel, augmente les limites de rate)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Headers pour toutes les requêtes
        self.session.headers.update({
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip'
        })
        
        if self.api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {self.api_key}'
            })
            logger.info("✅ API Key configurée")
        else:
            logger.info("ℹ️  Mode sans API Key (limité à 200 req/min)")
    
    def get_asset(self, asset_id: str) -> Optional[Dict]:
        """
        Récupère les informations d'une crypto spécifique
        
        Args:
            asset_id: Identifiant de la crypto (ex: 'bitcoin')
            
        Returns:
            Dict avec les données de la crypto ou None en cas d'erreur
        """
        url = f"{self.base_url}/assets/{asset_id}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data:
                return data['data']
            else:
                logger.warning(f"⚠️  Pas de données pour {asset_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur API pour {asset_id}: {e}")
            return None
    
    def get_multiple_assets(self, asset_ids: List[str]) -> List[Dict]:
        """
        Récupère les données de plusieurs cryptos
        
        Args:
            asset_ids: Liste d'identifiants de cryptos
            
        Returns:
            Liste de dictionnaires avec les données
        """
        results = []
        
        # Récupérer chaque crypto individuellement
        # Note: L'API CoinCap n'a pas d'endpoint batch, 
        # donc on fait plusieurs appels
        for asset_id in asset_ids:
            data = self.get_asset(asset_id)
            if data:
                # Ajouter un timestamp pour savoir quand on a récupéré la donnée
                data['fetched_at'] = int(time.time() * 1000)  # milliseconds
                results.append(data)
                logger.debug(f"✅ {asset_id}: ${data.get('priceUsd', 'N/A')}")
            
            # Petit délai pour ne pas surcharger l'API
            time.sleep(0.1)
        
        logger.info(f"📊 Récupéré {len(results)}/{len(asset_ids)} cryptos")
        return results
    
    def format_for_kafka(self, raw_data: Dict) -> Dict:
        """
        Formate les données brutes de l'API pour Kafka
        
        Args:
            raw_data: Données brutes de l'API
            
        Returns:
            Dict formaté pour Kafka
        """
        try:
            return {
                'symbol': raw_data.get('symbol', 'UNKNOWN'),
                'name': raw_data.get('name', 'Unknown'),
                'price_usd': float(raw_data.get('priceUsd', 0)),
                'volume_24h': float(raw_data.get('volumeUsd24Hr', 0)),
                'market_cap_usd': float(raw_data.get('marketCapUsd', 0)),
                'change_percent_24h': float(raw_data.get('changePercent24Hr', 0)),
                'supply': float(raw_data.get('supply', 0)),
                'max_supply': float(raw_data.get('maxSupply', 0)) if raw_data.get('maxSupply') else None,
                'rank': int(raw_data.get('rank', 0)),
                'timestamp': raw_data.get('fetched_at', int(time.time() * 1000)),
                'source': 'coincap'
            }
        except (ValueError, TypeError) as e:
            logger.error(f"❌ Erreur de formatage: {e}")
            return None
    
    def close(self):
        """Ferme la session HTTP"""
        self.session.close()
        logger.info("🔌 Session API fermée")


# Fonction utilitaire pour tester le client
def test_api_client():
    """Fonction de test du client API"""
    from config import COINCAP_API_URL, COINCAP_API_KEY
    
    client = CoinCapAPIClient(COINCAP_API_URL, COINCAP_API_KEY)
    
    print("\n🧪 Test du client API CoinCap\n")
    print("=" * 50)
    
    # Test 1: Récupérer Bitcoin
    print("\n1️⃣ Test: Récupérer Bitcoin")
    btc = client.get_asset('bitcoin')
    if btc:
        print(f"   ✅ Bitcoin: ${btc.get('priceUsd', 'N/A')}")
        print(f"   📊 Market Cap: ${btc.get('marketCapUsd', 'N/A')}")
    else:
        print("   ❌ Échec")
    
    # Test 2: Récupérer plusieurs cryptos
    print("\n2️⃣ Test: Récupérer plusieurs cryptos")
    cryptos = ['bitcoin', 'ethereum', 'ripple']
    results = client.get_multiple_assets(cryptos)
    print(f"   ✅ Récupéré: {len(results)}/{len(cryptos)} cryptos")
    
    # Test 3: Formatage pour Kafka
    if results:
        print("\n3️⃣ Test: Formatage pour Kafka")
        formatted = client.format_for_kafka(results[0])
        if formatted:
            print(f"   ✅ Formaté: {formatted['symbol']} @ ${formatted['price_usd']}")
    
    client.close()
    print("\n" + "=" * 50)
    print("✅ Tests terminés\n")


if __name__ == "__main__":
    # Configuration du logging pour les tests
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    test_api_client()
