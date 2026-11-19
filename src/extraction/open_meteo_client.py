
import pandas as pd

from src.extraction.api_client import APIClient


# Endpoint público da API Open-Meteo.
# O recurso "forecast" permite consultar previsões meteorológicas.
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather_data(
    client: APIClient,
    latitude: float,
    longitude: float,
) -> pd.DataFrame:
    """
    Consulta dados meteorológicos horários na API Open-Meteo.

    Args:
        client: Instância do cliente HTTP responsável pela requisição.
        latitude: Coordenada geográfica de latitude do local.
        longitude: Coordenada geográfica de longitude do local.

    Returns:
        DataFrame contendo os dados meteorológicos horários.
        Caso a API não retorne dados horários, devolve um DataFrame vazio.
    """

    # Define os parâmetros enviados à API.
    # Latitude e longitude identificam a localização da consulta.
    params = {
        "latitude": latitude,
        "longitude": longitude,

        # Variáveis meteorológicas solicitadas:
        # temperature_2m: temperatura a 2 metros de altura.
        # relative_humidity_2m: umidade relativa a 2 metros.
        # precipitation: precipitação horária.
        # wind_speed_10m: velocidade do vento a 10 metros.
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ],

        # Define o horizonte da previsão em um dia.
        "forecast_days": 1,

        # Solicita que a API utilize o fuso horário
        # correspondente à localização consultada.
        "timezone": "auto",
    }

    # Executa a requisição GET utilizando o cliente HTTP compartilhado.
    # O cliente centraliza timeout, Rate Limiting e Retry.
    response = client.get_json(
        OPEN_METEO_URL,
        params=params,
    )

    # Recupera o bloco "hourly" da resposta JSON.
    # Caso essa chave não exista, utiliza um dicionário vazio.
    hourly_data = response.get("hourly", {})

    # Verifica se a resposta contém dados meteorológicos horários.
    # Se não houver dados, interrompe o processamento.
    if not hourly_data:
        return pd.DataFrame()

    # Converte os dados horários do JSON em um DataFrame Pandas.
    # Cada variável meteorológica será representada por uma coluna.
    return pd.DataFrame(hourly_data)
