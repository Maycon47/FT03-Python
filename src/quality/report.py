
import json
from datetime import datetime, timezone
from pathlib import Path


def export_quality_report(
    quality_report: dict,
    output_dir: Path,
) -> Path:
    """
    Exporta o relatório de execução e auditoria de qualidade em JSON.

    Args:
        quality_report: Dicionário com os resultados da validação.
        output_dir: Diretório de destino do relatório.

    Returns:
        Caminho do arquivo JSON gerado.
    """

    # Registra a data e hora da execução em UTC.
    execution_timestamp = datetime.now(timezone.utc).isoformat()

    # Organiza as informações da execução e da qualidade dos dados.
    report = {
        "execution": {
            "timestamp": execution_timestamp,
            "total_records": quality_report["total_records"],
            "total_columns": quality_report["total_columns"],
        },
        "data_quality": quality_report,
    }

    # Garante que o diretório de destino exista.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define o caminho do arquivo JSON.
    report_path = output_dir / "quality_report.json"

    # Exporta o relatório com formatação e suporte a caracteres especiais.
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return report_path
