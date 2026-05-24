from services.sentinel_price import executar_monitor
from unittest.mock import patch
from unittest.mock import MagicMock


@patch("services.sentinel_price.GameAPI")
@patch("services.sentinel_price.time")
def test_preco_caiu(mock_time, mock_api):
    mock_db = MagicMock()
    mock_api.return_value.buscar_nome_jogo.return_value = {
        "nome": "Cyberpunk 2077",
        "preco_atual": 102.1,
        "deal_id": "",
    }
    mock_db.buscar_jogo.return_value = [(1, "Cyberpunk 2077")]
    mock_db.buscar_historico.return_value = [(150.0, "19/05/2026", "Steam")]
    resultado = executar_monitor(mock_db)
    assert resultado == [
        {"nome": "Cyberpunk 2077", "valor": 102.1, "status": "promocao"}
    ]
    mock_db.salvar_preco.assert_called_once()


@patch("services.sentinel_price.GameAPI")
@patch("services.sentinel_price.time")
def test_preco_igual(mock_time, mock_api):
    mock_db = MagicMock()
    mock_api.return_value.buscar_nome_jogo.return_value = {
        "nome": "Cyberpunk 2077",
        "preco_atual": 102.1,
        "deal_id": "",
    }
    mock_db.buscar_jogo.return_value = [(1, "Cyberpunk 2077")]
    mock_db.buscar_historico.return_value = [(102.1, "19/05/2026", "Steam")]
    resultado = executar_monitor(mock_db)
    assert resultado == []

    mock_db.salvar_preco.assert_not_called()


@patch("services.sentinel_price.GameAPI")
@patch("services.sentinel_price.time")
def test_preco_maior(mock_time, mock_api):
    mock_db = MagicMock()
    mock_api.return_value.buscar_nome_jogo.return_value = {
        "nome": "Cyberpunk 2077",
        "preco_atual": 175.9,
        "deal_id": "",
    }
    mock_db.buscar_jogo.return_value = [(1, "Cyberpunk 2077")]
    mock_db.buscar_historico.return_value = [(102.1, "19/05/2026", "Steam")]
    resultado = executar_monitor(mock_db)
    assert resultado == []

    mock_db.salvar_preco.assert_called_once()


@patch("services.sentinel_price.GameAPI")
@patch("services.sentinel_price.time")
def test_sem_historico(mock_time, mock_api):
    mock_db = MagicMock()
    mock_api.return_value.buscar_nome_jogo.return_value = {
        "nome": "Cyberpunk 2077",
        "preco_atual": 175.9,
        "deal_id": "",
    }
    mock_db.buscar_jogo.return_value = [(1, "Cyberpunk 2077")]
    mock_db.buscar_historico.return_value = []
    resultado = executar_monitor(mock_db)
    assert resultado == []

    mock_db.salvar_preco.assert_called_once()


@patch("services.sentinel_price.GameAPI")
@patch("services.sentinel_price.time")
def test_return_none(mock_time, mock_api):
    mock_db = MagicMock()
    mock_api.return_value.buscar_nome_jogo.return_value = None
    mock_db.buscar_jogo.return_value = [(1, "Cyberpunk 2077")]
    mock_db.buscar_historico.return_value = []
    resultado = executar_monitor(mock_db)
    assert resultado == []

    mock_db.salvar_preco.assert_not_called()
