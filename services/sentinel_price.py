from api.game_api_client import GameAPI
import time
from utils.logger import configurar_logger
import random
from requests.exceptions import HTTPError


def executar_monitor(db):
    time.sleep(5)
    service = GameAPI()
    logger = configurar_logger()

    jogos_para_monitorar = db.buscar_jogo()

    jogos_promocao = []

    logger.info("INICIO - Ciclo de monitoramento iniciado")

    for jogo in jogos_para_monitorar:
        time.sleep(random.uniform(2.0, 4.0))
        try:
            info = service.buscar_nome_jogo(jogo[1])

            if info:
                nome = info["nome"]
                preco_atual = info["preco_atual"]
                time.sleep(0.5)
                deal_id = info["deal_id"]
                loja = service.buscar_loja(deal_id)

                # Busca o preco antigo para comparar
                historico = db.buscar_historico(nome)

                if historico:
                    ultimo_preco = historico[0][0]

                    if preco_atual < ultimo_preco:
                        logger.info(
                            f"PROMOCAO - {nome}: US${ultimo_preco} -> US${preco_atual} na loja {loja}"
                        )
                        db.salvar_preco(nome, preco_atual, loja)
                        jogos_promocao.append(
                            {"nome": nome, "valor": preco_atual, "status": "promocao"}
                        )

                    elif preco_atual > ultimo_preco:
                        logger.info(
                            f"AVISO - {nome}: Preco subiu para US${preco_atual}. Atualizando base."
                        )
                        db.salvar_preco(nome, preco_atual, loja)

                    else:
                        # Preco igual: Mantemos o log limpo
                        pass
                else:
                    logger.info(f"NOVO - {nome} cadastrado com US${preco_atual}")
                    db.salvar_preco(nome, preco_atual, loja)
            else:
                logger.warning(
                    f"NAO ENCONTRADO - Jogo {jogo} nao retornou dados da API"
                )

        except Exception as e:
            if isinstance(e, HTTPError) and e.response.status_code == 429:
                logger.warning(
                    f"RATE LIMIT - Aguardando 60s devido a erro 429 em {jogo[1]}"
                )
                time.sleep(60)  # Pausa longa específica para o erro
            else:
                logger.error(f"FALHA - Erro inesperado em {jogo}: {str(e)}")

    logger.info("FIM - Monitoramento concluido")
    return jogos_promocao
