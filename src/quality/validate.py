
import pandas as pd


def validate_data_quality(df: pd.DataFrame) -> dict:
    """
    Avalia a qualidade dos dados considerando estrutura,
    valores nulos, duplicidade e intervalos numéricos.

    Args:
        df: DataFrame integrado e enriquecido.

    Returns:
        Dicionário com os resultados das verificações.
    """

    # Define as colunas obrigatórias para a análise.
    required_columns = [
        "time",
        "codigo_localizacao",
        "nome_localizacao",
        "estado",
        "latitude",
        "longitude",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "wind_speed_10m",
        "temperatura_media_localizacao",
        "precipitacao_acumulada_localizacao",
        "velocidade_media_vento_localizacao",
    ]

    # Identifica as colunas ausentes no DataFrame.
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    # Calcula a quantidade e a proporção de valores nulos.
    null_counts = df.isnull().sum()

    null_ratio = (
        df.isnull().mean() * 100
    ).round(2)

    # Verifica a duplicidade pela chave composta.
    duplicate_count = (
        df.duplicated(
            subset=["codigo_localizacao", "time"]
        ).sum()
        if not {"codigo_localizacao", "time"}.intersection(
            missing_columns
        )
        else None
    )

    # Define os intervalos válidos para as variáveis numéricas.
    valid_ranges = {
        "latitude": (-90, 90),
        "longitude": (-180, 180),
        "temperature_2m": (-90, 60),
        "relative_humidity_2m": (0, 100),
        "precipitation": (0, None),
        "wind_speed_10m": (0, None),
    }

    # Inicializa o resultado das verificações de intervalo.
    range_results = {}

    # Avalia os valores de cada variável numérica.
    for column, (minimum, maximum) in valid_ranges.items():

        # Verifica se a coluna existe antes da análise.
        if column not in df.columns:
            range_results[column] = {
                "status": "coluna ausente",
                "invalid_count": None,
            }
            continue

        # Identifica valores abaixo do mínimo permitido.
        invalid = df[column] < minimum

        # Identifica valores acima do máximo, quando aplicável.
        if maximum is not None:
            invalid = invalid | (df[column] > maximum)

        # Registra a quantidade de valores fora do intervalo.
        range_results[column] = {
            "status": "válido" if not invalid.any() else "inválido",
            "invalid_count": int(invalid.sum()),
        }

    # Organiza os resultados em um relatório estruturado.
    report = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "structure": {
            "missing_columns": missing_columns,
            "status": "válido" if not missing_columns else "inválido",
        },
        "completeness": {
            "null_counts": {
                column: int(value)
                for column, value in null_counts.items()
            },
            "null_ratio_percent": {
                column: float(value)
                for column, value in null_ratio.items()
            },
            "total_null_values": int(null_counts.sum()),
        },
        "uniqueness": {
            "duplicate_records": (
                int(duplicate_count)
                if duplicate_count is not None
                else None
            ),
        },
        "validity": range_results,
    }

    return report
