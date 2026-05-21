from api.client import APIClient
from utils.logger import configurar_logger
from database.redis_client import r
import json

from dotenv import load_dotenv
import os

load_dotenv()
logger = configurar_logger()

class GameAPI:
    def __init__(self):
        self.api = APIClient(base_url=os.getenv('CHEAPSHARK_URL'))
        self.loja = []
        self.redis_falhou = False

    
    def buscar_nome_jogo(self, nome_jogo):
        
        endpoint = f"games?title={nome_jogo}"
        dados = self.api.get(endpoint)

        try:
            if dados and len(dados) > 0:
                return {
                    "game_id": dados[0]['gameID'],
                    "nome": dados[0]['external'],
                    "preco_atual": float(dados[0]['cheapest']),
                    "deal_id": dados[0]['cheapestDealID']
                }
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar jogo: {e}")
            raise e
    
    def buscar_loja(self, deal_id):
        endpoint = f"deals?id={deal_id}"
        dados = self.api.get(endpoint)

        try:
            if dados:
                store_id = dados['gameInfo']['storeID']
                return self.get_nome_loja(store_id)
            return None
        except Exception as e:
            logger.error(f"Erro ao buscar loja: {e}")
            raise e
    
    def get_nome_loja(self, store_id):
        endpoint = "stores"
        
        if self.redis_falhou:
                return None 
        try:
            cache_key = "cheapshark:stores"
            stores_cache = r.get(cache_key)
            if stores_cache:
                stores = json.loads(stores_cache)
                for loja in stores:
                    if loja['storeID'] == store_id:
                        return loja['storeName']
                return "Desconhecida"    
            else:

                stores = self.loja = self.api.get(endpoint)
                r.setex(
                    cache_key,
                    60 * 60 * 24,
                    json.dumps(stores)
                )
                for loja in stores:
                    if loja['storeID'] == store_id:
                        return loja['storeName']
                return "Desconhecida"
        except Exception as e:
            endpoint = "stores"
            self.redis_falhou = True
            logger.error(f"Erro no redis {e}")

            if not self.loja:
                self.loja = self.api.get(endpoint)
                

            for loja in self.loja:
                if loja['storeID'] == store_id:
                    return loja['storeName']
                
            return "Desconhecida"
            
            
        