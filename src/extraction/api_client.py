
import time
from typing import Any

import requests


class APIClient:
    """
    Cliente HTTP reutilizável para consumo de APIs públicas.

    Implementa timeout, Rate Limiting, Retry,
    Backoff Exponencial e tratamento de erros.
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        min_interval: float = 1.0,
    ) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.min_interval = min_interval
        self.session = requests.Session()
        self.last_request_time = 0.0

    def get_json(
        self,
        url: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Executa uma requisição GET e retorna a resposta JSON.

        Repete a requisição em falhas temporárias,
        respeitando o limite de tentativas configurado.
        """

        for attempt in range(self.max_retries + 1):

            # Controla o intervalo entre requisições
            elapsed = time.monotonic() - self.last_request_time
            wait_time = self.min_interval - elapsed

            if wait_time > 0:
                time.sleep(wait_time)

            # Executa a requisição HTTP
            try:
                response = self.session.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                )

                self.last_request_time = time.monotonic()

            except requests.RequestException:
                if attempt == self.max_retries:
                    raise

                time.sleep(2 ** attempt)
                continue

            # Trata erros temporários: HTTP 429 e 5xx
            if response.status_code == 429 or response.status_code >= 500:

                if attempt == self.max_retries:
                    response.raise_for_status()

                retry_after = response.headers.get("Retry-After")

                if retry_after and retry_after.isdigit():
                    delay = int(retry_after)
                else:
                    delay = 2 ** attempt

                time.sleep(delay)
                continue

            # Interrompe erros HTTP permanentes
            response.raise_for_status()

            # Converte a resposta para JSON
            try:
                return response.json()

            except ValueError:
                if attempt == self.max_retries:
                    raise

                time.sleep(2 ** attempt)

        raise RuntimeError(
            "Não foi possível obter resposta da API."
        )
