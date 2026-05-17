from fastapi import FastAPI, Header, HTTPException, status
from services.sentinel_price import executar_monitor 
from utils.logger import configurar_logger
from pydantic import BaseModel
from database.db_manager import DBManager
from psycopg2.errors import UniqueViolation
import os

logger = configurar_logger()
db = DBManager()

app = FastAPI()

API_KEY = os.getenv("INTERNAL_API_KEY")

class Jogos(BaseModel):
    nome_jogo: str
    



@app.get("/")
def home():
    return {"status": "API rodando"}

@app.post("/executar")
def rodar_script(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Não autorizado")
    try:
        jogos_promocao = executar_monitor(db) 
        logger.info("Sucesso")
        return {"status": "ok", "Promoçoes": jogos_promocao}
    except Exception as e:
        logger.error(f"erro: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no Servidor")


@app.post("/jogos",status_code=status.HTTP_201_CREATED)
def salvar_jogos(jogo: Jogos, x_api_key: str = Header()):
    if x_api_key != API_KEY:
       raise HTTPException(status_code=401, detail="Não autorizado")
    
    try:
        id_jogo = db.salvar_jogo(jogo.nome_jogo)
        return {
            "mensagem": "Jogo salvo com sucesso", 
            "id_jogo": id_jogo,
            "nome_jogo": jogo.nome_jogo
        }
        
    except UniqueViolation as e:
        logger.error(f"Valor duplicado: {e}")
        raise HTTPException(status_code=409, detail="Conflict: Valor duplicado")
    except Exception as e:
        logger.error(f"Erro interno no Servidor: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no Servidor")
    
@app.get("/jogos")
def buscar_jogo(x_api_key: str = Header()):
    
    if x_api_key != API_KEY:
       raise HTTPException(status_code=401, detail="Não autorizado")
    db_jogos = db.buscar_jogo()
    resultado = [
        {
            "id": jogo[0],
            "nome": jogo[1]
        }
        for jogo in db_jogos
    ]

    return resultado