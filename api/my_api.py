from fastapi import FastAPI, Header, HTTPException
from services.sentinel_price import executar_monitor 
from utils.logger import configurar_logger
import os

logger = configurar_logger()

app = FastAPI()

API_KEY = os.getenv("INTERNAL_API_KEY")


@app.get("/")
def home():
    return {"status": "API rodando"}

@app.post("/executar")
def rodar_script(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Não autorizado")
    try:
        jogos_promocao = executar_monitor() 
        logger.info("Sucesso")
        return {"status": "ok", "Promoçoes": jogos_promocao}
    except Exception as e:
        logger.error(f"erro: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no Servidor")