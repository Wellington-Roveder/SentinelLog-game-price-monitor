from fastapi import FastAPI
from services.sentinel_price import executar_monitor 
from utils.logger import configurar_logger

app = FastAPI()

@app.get("/")
def home():
    return {"status": "API rodando"}

@app.post("/executar")
def rodar_script():
    logger = configurar_logger()
    try:
        jogos_promocao = executar_monitor() 
        logger.info("Sucesso")
        return {"status": "ok", "Promoçoes": jogos_promocao}
    except Exception as e:
        logger.error(f"erro: {e}")
        return {"status": "erro", "detail": str(e)}