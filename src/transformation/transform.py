
import pandas as pd

def standardize_data_types(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Padroniza os tipos de dados do conjunto integrado.

    Args:
        df: DataFrame contendo os dados extraídos das APIs.

    Returns:
        DataFrame com datas, identificadores e valores numéricos
        padronizados.
    """

    # Cria uma cópia para preservar o DataFrame original.
    df = df.copy()

    # Define as colunas que devem representar datas e horários.
    # errors="coerce" converte valores inválidos para NaT.
    if "time" in df.columns:
        df["time"] = pd.to_datetime(
            df["time"],
            errors="coerce",
        )

    # Define os identificadores que devem permanecer como texto.
    # Isso evita perder zeros à esquerda ou alterar códigos.
    colunas_texto = [
        "codigo_localizacao",
        "nome_localizacao",
        "estado",
    ]

    for coluna in colunas_texto:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype("string")

    # Define as coordenadas e variáveis meteorológicas numéricas.
    colunas_numericas = [
        "latitude",
        "longitude",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ]

    for coluna in colunas_numericas:

        # Converte os valores para números.
        # Valores inválidos são representados como NaN.
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(
                df[coluna],
                errors="coerce",
            )

    # Retorna o DataFrame com os tipos padronizados.
    return df


def handle_null_values(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Trata registros com valores nulos nos campos essenciais.

    Args:
        df: DataFrame contendo os dados integrados.

    Returns:
        DataFrame sem registros que não possuem data ou
        identificador da localização.

    Observação:
        Valores ausentes em campos descritivos e meteorológicos
        são preservados para evitar distorções nos dados.
    """

    # Cria uma cópia para preservar o DataFrame original.
    df = df.copy()

    # Define os campos obrigatórios para identificar um registro.
    colunas_obrigatorias = [
        "time",
        "codigo_localizacao",
    ]

    # Verifica se todas as colunas obrigatórias existem.
    # Caso alguma esteja ausente, interrompe a execução.
    colunas_ausentes = [
        coluna
        for coluna in colunas_obrigatorias
        if coluna not in df.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"Colunas obrigatórias não encontradas: {colunas_ausentes}"
        )

    # Registra a quantidade de linhas antes do tratamento.
    registros_antes = len(df)

    # Remove somente registros sem data ou identificação.
    # Os demais valores nulos são preservados.
    df = df.dropna(
        subset=colunas_obrigatorias
    ).copy()

    # Calcula quantos registros foram removidos.
    registros_removidos = registros_antes - len(df)

    # Apresenta um resumo da operação.
    print("Registros antes do tratamento:", registros_antes)
    print("Registros removidos:", registros_removidos)
    print("Registros após o tratamento:", len(df))

    # Retorna o DataFrame tratado.
    return df


def remove_duplicates(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove registros duplicados considerando localização e horário.

    Args:
        df: DataFrame contendo os dados integrados.

    Returns:
        DataFrame sem registros duplicados pela chave definida.

    Observação:
        A primeira ocorrência de cada combinação de localização
        e horário é preservada.
    """

    # Cria uma cópia para preservar o DataFrame original.
    df = df.copy()

    # Define as colunas utilizadas para identificar cada registro.
    colunas_chave = [
        "codigo_localizacao",
        "time",
    ]

    # Verifica se todas as colunas da chave existem no DataFrame.
    colunas_ausentes = [
        coluna
        for coluna in colunas_chave
        if coluna not in df.columns
    ]

    # Interrompe a execução caso alguma coluna obrigatória não exista.
    if colunas_ausentes:
        raise ValueError(
            f"Colunas obrigatórias não encontradas: {colunas_ausentes}"
        )

    # Registra a quantidade de registros antes da remoção.
    registros_antes = len(df)

    # Conta quantos registros são duplicados considerando a chave.
    duplicados = df.duplicated(
        subset=colunas_chave
    ).sum()

    # Remove as duplicidades, preservando a primeira ocorrência.
    df = df.drop_duplicates(
        subset=colunas_chave,
        keep="first",
    ).copy()

    # Calcula a quantidade de registros removidos.
    registros_removidos = registros_antes - len(df)

    # Apresenta o resumo da operação.
    print("Registros antes da transformação:", registros_antes)
    print("Duplicidades identificadas:", duplicados)
    print("Registros removidos:", registros_removidos)
    print("Registros após a transformação:", len(df))

    # Retorna o DataFrame sem duplicidades.
    return df


def join_data_sources(
    df_weather: pd.DataFrame,
    df_locations: pd.DataFrame,
) -> pd.DataFrame:
    """
    Integra dados meteorológicos e metadados das localizações
    utilizando SQL INNER JOIN no DuckDB.

    Args:
        df_weather: DataFrame com as medições meteorológicas.
        df_locations: DataFrame com os dados das localizações.

    Returns:
        DataFrame contendo os dados das duas fontes integrados.
    """

    # Importa o DuckDB para executar a consulta SQL.
    import duckdb

    # Define as colunas necessárias para executar o relacionamento.
    weather_columns = [
        "time",
        "codigo_localizacao",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
    ]

    location_columns = [
        "codigo_localizacao",
        "nome_localizacao",
        "estado",
        "latitude",
        "longitude",
    ]

    # Verifica se os DataFrames possuem todas as colunas necessárias.
    missing_weather = set(weather_columns) - set(df_weather.columns)
    missing_locations = set(location_columns) - set(df_locations.columns)

    if missing_weather:
        raise ValueError(
            f"Colunas ausentes nos dados meteorológicos: {missing_weather}"
        )

    if missing_locations:
        raise ValueError(
            f"Colunas ausentes nos dados das localizações: {missing_locations}"
        )

    # Cria uma conexão DuckDB em memória.
    connection = duckdb.connect(database=":memory:")

    try:
        # Registra os DataFrames como tabelas temporárias.
        connection.register(
            "weather",
            df_weather[weather_columns],
        )

        connection.register(
            "locations",
            df_locations[location_columns].drop_duplicates(
                subset=["codigo_localizacao"]
            ),
        )

        # Executa o INNER JOIN utilizando a chave de localização.
        query = """
            SELECT
                weather.time,
                weather.codigo_localizacao,
                locations.nome_localizacao,
                locations.estado,
                locations.latitude,
                locations.longitude,
                weather.temperature_2m,
                weather.relative_humidity_2m,
                weather.precipitation,
                weather.wind_speed_10m
            FROM weather
            INNER JOIN locations
                ON weather.codigo_localizacao =
                   locations.codigo_localizacao
            ORDER BY
                weather.codigo_localizacao,
                weather.time
        """

        # Executa a consulta e converte o resultado em DataFrame.
        df_integrado = connection.execute(query).fetchdf()

    finally:
        # Encerra a conexão após a execução.
        connection.close()

    return df_integrado


def enrich_with_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enriquece os dados meteorológicos com métricas calculadas
    por localização.

    Args:
        df: DataFrame contendo os dados meteorológicos integrados.

    Returns:
        DataFrame original enriquecido com três métricas adicionais.
    """

    # Define as colunas necessárias para os cálculos.
    required_columns = [
        "codigo_localizacao",
        "temperature_2m",
        "precipitation",
        "wind_speed_10m",
    ]

    # Verifica se todas as colunas necessárias estão disponíveis.
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas necessárias ausentes: {missing_columns}"
        )

    # Cria uma cópia para preservar o DataFrame original.
    df_enriched = df.copy()

    # Agrupa os registros por localização e calcula as métricas.
    df_metrics = (
        df_enriched
        .groupby("codigo_localizacao")
        .agg(
            temperatura_media_localizacao=(
                "temperature_2m",
                "mean",
            ),
            precipitacao_acumulada_localizacao=(
                "precipitation",
                lambda values: values.sum(min_count=1),
            ),
            velocidade_media_vento_localizacao=(
                "wind_speed_10m",
                "mean",
            ),
        )
        .reset_index()
    )

    # Incorpora as métricas aos registros originais.
    df_enriched = df_enriched.merge(
        df_metrics,
        on="codigo_localizacao",
        how="left",
        validate="many_to_one",
        sort=False,
    )

    return df_enriched

