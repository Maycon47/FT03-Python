
import pandas as pd
from pathlib import Path


def save_parquet(
    df: pd.DataFrame,
    output_dir: Path,
    filename: str = "dados_integrados.parquet",
) -> Path:
    """
    Persiste o DataFrame em formato Parquet com compressão Snappy.

    Args:
        df: DataFrame final integrado e enriquecido.
        output_dir: Diretório de destino do arquivo.
        filename: Nome do arquivo Parquet.

    Returns:
        Caminho do arquivo Parquet gerado.
    """

    # Verifica se o DataFrame possui registros.
    if df.empty:
        raise ValueError(
            "Não é possível persistir um DataFrame vazio."
        )

    # Garante que o diretório de saída exista.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define o caminho do arquivo Parquet.
    output_path = output_dir / filename

    # Persiste os dados utilizando PyArrow e compressão Snappy.
    df.to_parquet(
        output_path,
        engine="pyarrow",
        compression="snappy",
        index=False,
    )

    return output_path


def save_partitioned_parquet(
    df: pd.DataFrame,
    output_dir: Path,
) -> Path:
    """
    Persiste os dados em Parquet particionados por ano e mês.

    Args:
        df: DataFrame final com os dados meteorológicos.
        output_dir: Diretório principal de saída do projeto.

    Returns:
        Caminho do diretório contendo os arquivos particionados.
    """

    # Verifica se o DataFrame possui registros.
    if df.empty:
        raise ValueError(
            "Não é possível particionar um DataFrame vazio."
        )

    # Verifica se a coluna temporal está disponível.
    if "time" not in df.columns:
        raise ValueError(
            "A coluna time é obrigatória para o particionamento."
        )

    # Verifica se a coluna temporal possui tipo datetime.
    if not pd.api.types.is_datetime64_any_dtype(df["time"]):
        raise TypeError(
            "A coluna time deve possuir tipo datetime."
        )

    # Cria uma cópia para preservar o DataFrame original.
    df_partitioned = df.copy()

    # Extrai o ano e o mês da coluna temporal.
    df_partitioned["ano"] = df_partitioned["time"].dt.year
    df_partitioned["mes"] = df_partitioned["time"].dt.month

    # Define o diretório de destino das partições.
    partition_dir = output_dir / "dados_particionados"

    # Evita sobrescrever uma estrutura de partições existente.
    if partition_dir.exists():
        raise FileExistsError(
            f"O diretório já existe: {partition_dir}. "
            "Remova ou renomeie o diretório antes de executar novamente."
        )

    # Garante que o diretório principal exista.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Grava os arquivos Parquet particionados por ano e mês.
    df_partitioned.to_parquet(
        partition_dir,
        engine="pyarrow",
        compression="snappy",
        partition_cols=["ano", "mes"],
        index=False,
    )

    return partition_dir
