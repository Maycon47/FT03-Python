
from typing import Any

import pandas as pd

from src.extraction.api_client import APIClient


# Endpoint público da API da USGS.
# Esse endereço permite consultar locais de monitoramento.
USGS_URL = (
    "https://api.waterdata.usgs.gov/ogcapi/v1/"
    "collections/monitoring-locations/items"
)


def get_monitoring_locations(
    client: APIClient,
    limit: int = 100,
) -> pd.DataFrame:
    """
    Consulta localizações de monitoramento disponibilizadas pela USGS.

    Args:
        client: Instância do cliente HTTP responsável pela requisição.
        limit: Quantidade máxima de registros solicitados à API.

    Returns:
        DataFrame contendo os dados das localizações e suas coordenadas.
        Caso a API não retorne registros, devolve um DataFrame vazio.
    """

    # Envia uma requisição GET ao endpoint da USGS.
    # O parâmetro limit controla a quantidade máxima de registros retornados.
    response: dict[str, Any] = client.get_json(
        USGS_URL,
        params={"limit": limit},
    )

    # Recupera a lista de elementos GeoJSON retornada pela API.
    # Se a chave "features" não existir, utiliza uma lista vazia.
    features = response.get("features", [])

    # Interrompe o processamento quando não existem registros.
    if not features:
        return pd.DataFrame()

    # Converte os registros JSON em uma estrutura tabular.
    # json_normalize expande propriedades aninhadas em colunas.
    df = pd.json_normalize(features)

    # Extrai as coordenadas geográficas de cada elemento.
    # No formato GeoJSON Point, a ordem é:
    # [longitude, latitude].
    coordinates = [
        (feature.get("geometry") or {}).get("coordinates")
        for feature in features
    ]

    # Cria a coluna longitude utilizando a primeira posição
    # da lista de coordenadas, quando disponível.
    # Caso não existam coordenadas válidas, atribui None.
    df["longitude"] = [
        coord[0]
        if isinstance(coord, (list, tuple)) and len(coord) >= 2
        else None
        for coord in coordinates
    ]

    # Cria a coluna latitude utilizando a segunda posição
    # da lista de coordenadas, quando disponível.
    # Caso não existam coordenadas válidas, atribui None.
    df["latitude"] = [
        coord[1]
        if isinstance(coord, (list, tuple)) and len(coord) >= 2
        else None
        for coord in coordinates
    ]

    # Retorna os dados tabulares com longitude e latitude separadas.
    return df
