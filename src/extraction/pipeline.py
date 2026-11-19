
import pandas as pd

# Importa o cliente HTTP responsável pelas requisições às APIs.
from src.extraction.api_client import APIClient

# Importa a função que consulta as localizações de monitoramento da USGS.
from src.extraction.usgs_client import get_monitoring_locations

# Importa a função que consulta os dados meteorológicos da Open-Meteo.
from src.extraction.open_meteo_client import get_weather_data


def run_pipeline(
    limit: int = 1000,
    max_locations: int = 5,
) -> pd.DataFrame:
    """
    Executa a extração e integração dos dados da USGS e Open-Meteo.

    Args:
        limit: Quantidade máxima de localizações solicitadas à USGS.
        max_locations: Quantidade máxima de localizações processadas.

    Returns:
        DataFrame com os dados meteorológicos associados às localizações.
        Retorna um DataFrame vazio caso não existam resultados.
    """

    # Inicializa o cliente HTTP compartilhado pelas duas APIs.
    # Isso centraliza as configurações de timeout, Rate Limiting e Retry.
    client = APIClient()

    # Consulta as localizações de monitoramento disponibilizadas pela USGS.
    # O parâmetro limit controla a quantidade de registros solicitados.
    df_usgs: pd.DataFrame = get_monitoring_locations(
        client,
        limit=limit,
    )

    # Verifica se a consulta retornou registros.
    # Evita tentar acessar colunas inexistentes em um DataFrame vazio.
    if df_usgs.empty:
        return pd.DataFrame()

    # Remove localizações que não possuem latitude ou longitude.
    # Sem essas coordenadas, não é possível consultar o clima do local.
    # O método head limita a quantidade de locais processados.
    df_validos: pd.DataFrame = (
        df_usgs
        .dropna(subset=["latitude", "longitude"])
        .head(max_locations)
    )

    # Cria uma lista para armazenar os DataFrames meteorológicos.
    # Cada elemento representará os dados de uma localização.
    resultados: list[pd.DataFrame] = []

    # Percorre as localizações selecionadas.
    # O índice da linha não é necessário, por isso utilizamos "_".
    for _, local in df_validos.iterrows():

        # Consulta os dados meteorológicos utilizando as coordenadas
        # geográficas da localização atual.
        df_clima: pd.DataFrame = get_weather_data(
            client,
            latitude=local["latitude"],
            longitude=local["longitude"],
        )

        # Verifica se a API retornou dados meteorológicos.
        # Se o DataFrame estiver vazio, passa para a próxima localização.
        if df_clima.empty:
            continue

        # Adiciona o código identificador da localização da USGS.
        # Essa informação permite relacionar os dados meteorológicos
        # ao respectivo local de monitoramento.
        df_clima["codigo_localizacao"] = (
            local["properties.monitoring_location_number"]
        )

        # Adiciona o nome da localização de monitoramento.
        df_clima["nome_localizacao"] = (
            local["properties.monitoring_location_name"]
        )

        # Adiciona o estado onde está localizado o ponto de monitoramento.
        df_clima["estado"] = local["properties.state_name"]

        # Adiciona as coordenadas geográficas ao resultado meteorológico.
        df_clima["latitude"] = local["latitude"]
        df_clima["longitude"] = local["longitude"]

        # Armazena o DataFrame da localização na lista de resultados.
        resultados.append(df_clima)

    # Verifica se alguma localização produziu dados meteorológicos.
    # Se a lista estiver vazia, retorna um DataFrame vazio.
    if not resultados:
        return pd.DataFrame()

    # Concatena os DataFrames armazenados em uma única tabela.
    # ignore_index=True recria o índice sequencial do resultado final.
    return pd.concat(resultados, ignore_index=True)
