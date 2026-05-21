from unittest.mock import patch
from requests.exceptions import RequestException
import pytest

from api.client import retry


def test_requisicao_retentada_ate_3_vezes():
    chamadas = {"n": 0}

    @retry(max_retries=3)
    def func():
        chamadas["n"] += 1
        raise RequestException("falha")

    with patch("time.sleep"), pytest.raises(RequestException):
        func()

    assert chamadas["n"] == 3


def test_apos_3_falhas_levanta_exception_e_loga_erro():
    @retry(max_retries=3)
    def func():
        raise RequestException("falha")

    with patch("time.sleep"), patch("api.client.logger") as mock_logger:
        with pytest.raises(RequestException):
            func()

    mock_logger.error.assert_called()


def test_sucesso_na_primeira_tentativa_sem_sleep():
    @retry(max_retries=3)
    def func():
        return "OK"

    with patch("time.sleep") as mock_sleep:
        result = func()

    assert result == "OK"
    mock_sleep.assert_not_called()