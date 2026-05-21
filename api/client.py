import requests
import time
from requests.exceptions import RequestException,HTTPError
import functools
from utils.logger import configurar_logger

logger = configurar_logger()

def retry(max_retries=3,backoff_factor=2,status_forcelist=(500,502,504)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args ,**kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                
                    
                except (RequestException, ConnectionError) as e:
                    retries += 1
                    logger.warning(f"Tentando novamente, Tentativa: {retries} Motivo {e}")


                    if isinstance(e, HTTPError) and e.response.status_code not in status_forcelist:
                        logger.error(f"Erro na Execuçao {e}")
                        raise e
                        
                        
                        
                    if retries >= max_retries:
                        logger.error("Tentativas Excedeu os Limites")
                        raise e
                        

                    sleep_time = backoff_factor ** retries
                    time.sleep(sleep_time)
        return wrapper
    return decorator





class APIClient:
    def __init__(self, base_url):
       self.base_url = base_url
       self.session = requests.Session() # reutiliza conexao http mais rapido menos consumo

    @retry(max_retries=3, backoff_factor=2)
    def get(self, endpoint):
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", timeout= 10) #reutiliza sessao, timeout para nao dar trava para sempre
            response.raise_for_status()
            return response.json() # trasforma o json em dicionario python
            
           
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na Api: {e}") # mostra mensagem de erro 404,500
            raise e
       

    
