# FT03 — Matriz de Requisitos e Entregáveis

## 1. Extração de dados e APIs

| ID | Requisito | Situação |
|---|---|---|
| R01 | Consumir no mínimo duas APIs públicas de domínios distintos | Parcial |
| R02 | Implementar controle de taxas (Rate Limiting) | Pendente |
| R03 | Implementar retentativas (Retry) e tratamento de erros | Pendente |
| R04 | Gerenciar credenciais por variáveis de ambiente, sem versionar chaves | Pendente de validação |

## 2. Transformação e SQL

| ID | Requisito | Situação |
|---|---|---|
| R05 | Desenvolver scripts modulares em Python, com funções e Type Hints | Pendente |
| R06 | Desaninhar arrays e estruturas JSON utilizando SQL, DuckDB, SQLite ou PySpark | Pendente |
| R07 | Padronizar tipos e datas | Parcial |
| R08 | Tratar valores nulos | Parcial |
| R09 | Deduplicar registros | Parcial |
| R10 | Cruzar fontes de dados utilizando JOIN | Pendente |
| R11 | Enriquecer os dados com métricas | Pendente |

**Observação:** os requisitos R07 a R11 compõem as cinco transformações obrigatórias.

## 3. Data Quality e persistência

| ID | Requisito | Situação |
|---|---|---|
| R12 | Validar schema, null ratio, unicidade e intervalos | Parcial |
| R13 | Exportar relatório de execução e auditoria de qualidade em JSON ou CSV | Pendente |
| R14 | Persistir a camada final em Parquet ou Delta Lake | Pendente |
| R15 | Aplicar compressão Snappy | Pendente |
| R16 | Implementar particionamento temporal, como ano e mês | Pendente |

## 4. Entregáveis obrigatórios

| ID | Entregável | Situação |
|---|---|---|
| E01 | Repositório público no GitHub com código modular em `src/` | Parcial |
| E02 | README com instruções, variáveis de ambiente e documentação das APIs | Pendente |
| E03 | Executável ponta a ponta (`run.sh` ou comando único) | Pendente |
| E04 | Dataset final limpo e particionado em `output/` | Pendente |
| E05 | Relatório de Data Quality em JSON ou CSV | Pendente |

## 5. Diretriz de desenvolvimento

O desenvolvimento deve priorizar os requisitos técnicos e os entregáveis obrigatórios definidos no enunciado original.

Cada implementação deverá conter documentação objetiva com objetivo, implementação, resultado e conclusão.

O notebook `01_data_discovery_usgs.ipynb` preserva a exploração das fontes.

O notebook `02_pipeline_implementacao.ipynb` será utilizado para desenvolver e validar os componentes do pipeline, quando apropriado.

O código final deverá ser organizado de forma modular em `src/`.

Funcionalidades adicionais, como dashboards no Power BI, não fazem parte dos entregáveis obrigatórios e poderão ser desenvolvidas posteriormente.