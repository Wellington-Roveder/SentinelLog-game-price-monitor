from api.game_api_client import *
from database.db_manager import DBManager
import time
from utils.logger import configurar_logger
import json



def executar_monitor():
    db = DBManager()
    service = GameAPI()
    logger = configurar_logger()

    try:
        with open('jogos.json', 'r') as f:
            dados = json.load(f)
            jogos_para_monitorar = dados['jogos']
    except Exception as e:
        logger.error(f"Erro na conexao json {e}")
        return None

    
    jogos_promocao = []
    
    logger.info("INICIO - Ciclo de monitoramento iniciado")
    
    for jogo in jogos_para_monitorar:
        try:
            info = service.buscar_nome_jogo(jogo)
        
            if info:
                nome = info['nome']
                preco_atual = info['preco_atual']
                deal_id = info['deal_id']
                loja = service.buscar_loja(deal_id)
            
                # Busca o preco antigo para comparar
                historico = db.buscar_historico(nome)
            
                if historico:
                    ultimo_preco = historico[0][0]
                    
                    if preco_atual < ultimo_preco:
                        logger.info(f"PROMOCAO - {nome}: R${ultimo_preco} -> R${preco_atual} na loja {loja}")
                        db.salvar_preco(nome, preco_atual, loja)
                        jogos_promocao.append({"nome": nome, "valor": preco_atual, "status": "promocao"})
                        
                    
                    elif preco_atual > ultimo_preco:
                        logger.info(f"AVISO - {nome}: Preco subiu para R${preco_atual}. Atualizando base.")
                        db.salvar_preco(nome, preco_atual, loja)
                    
                    else:
                        # Preco igual: Mantemos o log limpo
                        pass
                else:
                    logger.info(f"NOVO - {nome} cadastrado com R${preco_atual}")
                    db.salvar_preco(nome, preco_atual, loja)
            else:
                logger.warning(f"NAO ENCONTRADO - Jogo {jogo} nao retornou dados da API")
                    
        except Exception as e:
            logger.error(f"FALHA - Erro inesperado em {jogo}: {str(e)}")  
                   
        time.sleep(1)
        
    logger.info("FIM - Monitoramento concluido")
    db.fechar_conexao()
    return jogos_promocao