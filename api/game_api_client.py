from api.client import APIClient
from utils.logger import configurar_logger


from dotenv import load_dotenv
import os

load_dotenv()
logger = configurar_logger()

class GameAPI:
    def __init__(self):
        self.api = APIClient(base_url=os.getenv('CHEAPSHARK_URL'))
        self.loja = []

    
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

        if not self.loja:
            self.loja = self.api.get(endpoint)

        for loja in self.loja:
            if loja['storeID'] == store_id:
                return loja['storeName']

        return "Desconhecida"