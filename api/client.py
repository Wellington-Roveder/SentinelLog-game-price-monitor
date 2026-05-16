import requests
from utils.logger import configurar_logger

logger = configurar_logger()

class APIClient:
    def __init__(self, base_url):
       self.base_url = base_url
       self.session = requests.Session() # reutiliza conexao http mais rapido menos consumo


    def get(self, endpoint):
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", timeout= 10) #reutiliza sessao, timeout para nao dar trava para sempre
            response.raise_for_status()
            return response.json() # trasforma o json em dicionario python
            
           
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na Api: {e}") # mostra mensagem de erro 404,500
            return None
       