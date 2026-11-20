
from pathlib import Path
import shutil

import pandas as pd

# Importa os módulos de extração.
from src.extraction.pipeline import run_pipeline

# Importa as funções de transformação.
from src.transformation.transform import (
    standardize_data_types,
    handle_null_values,
    remove_duplicates,
    join_data_sources,
    enrich_with_metrics,
)

# Importa as funções de qualidade e persistência.
from src.quality.validate import validate_data_quality
from src.quality.report import export_quality_report
from src.quality.storage import save_partitioned_parquet


# Define a raiz do projeto e o diretório de saída.
PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"


def main() -> None:
    """
    Executa o pipeline completo de Engenharia de Dados.
    """

    # Garante que o diretório de saída exista.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("INICIANDO PIPELINE USGS + OPEN-METEO")
    print("=" * 50)

    # 1. EXTRAÇÃO
    print("\n[1/9] Extraindo dados das APIs...")

    df_origem = run_pipeline(
        limit=1000,
        max_locations=5,
    )

    if df_origem.empty:
        raise RuntimeError(
            "O pipeline de extração não retornou registros."
        )

    print("Registros extraídos:", len(df_origem))

    # 2. PADRONIZAÇÃO
    print("\n[2/9] Padronizando tipos de dados...")

    df_padronizado = standardize_data_types(df_origem)

    # 3. TRATAMENTO DE VALORES NULOS
    print("\n[3/9] Tratando valores nulos...")

    df_tratado = handle_null_values(df_padronizado)

    # 4. DEDUPLICAÇÃO
    print("\n[4/9] Removendo registros duplicados...")

    df_sem_duplicados = remove_duplicates(df_tratado)

    if df_sem_duplicados.empty:
        raise RuntimeError(
            "Nenhum registro permaneceu após as transformações."
        )

    # 5. INTEGRAÇÃO COM SQL JOIN
    print("\n[5/9] Integrando fontes com DuckDB...")

    # Separa as medições meteorológicas.
    df_weather = df_sem_duplicados[
        [
            "time",
            "codigo_localizacao",
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
        ]
    ].copy()

    # Separa os metadados das localizações.
    df_locations = (
        df_sem_duplicados[
            [
                "codigo_localizacao",
                "nome_localizacao",
                "estado",
                "latitude",
                "longitude",
            ]
        ]
        .drop_duplicates(subset=["codigo_localizacao"])
        .copy()
    )

    # Executa o relacionamento SQL entre as fontes.
    df_integrado = join_data_sources(
        df_weather=df_weather,
        df_locations=df_locations,
    )

    print("Registros integrados:", len(df_integrado))

    # 6. ENRIQUECIMENTO
    print("\n[6/9] Calculando métricas meteorológicas...")

    df_enriquecido = enrich_with_metrics(df_integrado)

    # 7. VALIDAÇÃO DA QUALIDADE
    print("\n[7/9] Validando a qualidade dos dados...")

    quality_report = validate_data_quality(df_enriquecido)

    # Interrompe a execução caso existam problemas estruturais.
    if quality_report["structure"]["status"] != "válido":
        raise RuntimeError(
            "Foram identificadas colunas obrigatórias ausentes."
        )

    if quality_report["uniqueness"]["duplicate_records"] != 0:
        raise RuntimeError(
            "Foram identificados registros duplicados."
        )

    if any(
        item["invalid_count"] != 0
        for item in quality_report["validity"].values()
        if item["invalid_count"] is not None
    ):
        raise RuntimeError(
            "Foram identificados valores fora dos intervalos definidos."
        )

    # 8. AUDITORIA
    print("\n[8/9] Gerando relatório de auditoria...")

    report_path = export_quality_report(
        quality_report=quality_report,
        output_dir=OUTPUT_DIR,
    )

    # 9. PERSISTÊNCIA
    print("\n[9/9] Persistindo dados em Parquet...")

    # Remove somente a estrutura de partições gerada anteriormente.
    partition_dir = OUTPUT_DIR / "dados_particionados"

    if partition_dir.exists():
        shutil.rmtree(partition_dir)

    # Persiste os dados com Snappy e partições temporais.
    parquet_dir = save_partitioned_parquet(
        df=df_enriquecido,
        output_dir=OUTPUT_DIR,
    )

    # Exporta os dados persistidos em Parquet para CSV.
    print("\nExportando dados para CSV...")

    df_csv = pd.read_parquet(parquet_dir)

    # Remove as colunas utilizadas exclusivamente no particionamento.
    df_csv = df_csv.drop(columns=["ano", "mes"], errors="ignore")

    csv_path = OUTPUT_DIR / "dados_meteorologicos.csv"

    df_csv.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
    )

    print("Dados CSV:", csv_path)

    # Apresenta o resumo final da execução.
    print("\n" + "=" * 50)
    print("PIPELINE CONCLUÍDO COM SUCESSO")
    print("=" * 50)

    print("Registros processados:", len(df_enriquecido))
    print(
        "Localizações:",
        df_enriquecido["codigo_localizacao"].nunique(),
    )
    print("Colunas finais:", len(df_enriquecido.columns))
    print("Relatório JSON:", report_path)
    print("Dados Parquet:", parquet_dir)
    print("Dados CSV:", csv_path)


# Executa o pipeline quando o arquivo é chamado diretamente.
if __name__ == "__main__":
    main()
