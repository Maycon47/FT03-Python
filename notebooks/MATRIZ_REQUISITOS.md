# FT03: Matriz de Requisitos e Entregáveis

## 1. Extração de dados e APIs

| ID | Requisito | Situação | Evidência |
|---|---|---|---|
| R01 | Consumir no mínimo duas APIs públicas de domínios distintos | Concluído | `src/extraction/usgs_client.py` e `src/extraction/open_meteo_client.py` |
| R02 | Implementar controle de taxas (Rate Limiting) | Concluído | `src/extraction/api_client.py` |
| R03 | Implementar retentativas (Retry) e tratamento de erros | Concluído | `src/extraction/api_client.py` |
| R04 | Gerenciar credenciais por variáveis de ambiente, sem versionar chaves | Não aplicável | As APIs públicas utilizadas, USGS e Open-Meteo, não exigem chaves de autenticação. |

## 2. Transformação e SQL

| ID | Requisito | Situação | Evidência |
|---|---|---|---|
| R05 | Desenvolver scripts modulares em Python, com funções e Type Hints | Concluído | Módulos organizados em `src/` e execução pelo `run.py` |
| R06 | Desaninhar arrays e estruturas JSON utilizando SQL, DuckDB, SQLite ou PySpark | Concluído | `notebooks/02_pipeline_implementacao.ipynb`: seção de exploração de JSON com DuckDB |
| R07 | Padronizar tipos e datas | Concluído | `src/transformation/transform.py`: `standardize_data_types()` |
| R08 | Tratar valores nulos | Concluído | `src/transformation/transform.py`: `handle_null_values()` |
| R09 | Deduplicar registros | Concluído | `src/transformation/transform.py`: `remove_duplicates()` |
| R10 | Cruzar fontes de dados utilizando JOIN | Concluído | `src/transformation/transform.py`: `join_data_sources()` |
| R11 | Enriquecer os dados com métricas | Concluído | `src/transformation/transform.py`: `enrich_with_metrics()` |

**Observação:** os requisitos R07 a R11 compõem as cinco transformações obrigatórias.

## 3. Data Quality e persistência

| ID | Requisito | Situação | Evidência |
|---|---|---|---|
| R12 | Validar schema, null ratio, unicidade e intervalos | Concluído | `src/quality/validate.py` |
| R13 | Exportar relatório de execução e auditoria de qualidade em JSON ou CSV | Concluído | `src/quality/report.py` e `output/quality_report.json` |
| R14 | Persistir a camada final em Parquet ou Delta Lake | Concluído | `src/quality/storage.py` e `output/dados_particionados/` |
| R15 | Aplicar compressão Snappy | Concluído | `src/quality/storage.py`: `save_partitioned_parquet()` |
| R16 | Implementar particionamento temporal, como ano e mês | Concluído | `src/quality/storage.py` e `output/dados_particionados/ano=.../mes=.../` |

## 4. Entregáveis obrigatórios

| ID | Entregável | Situação | Evidência |
|---|---|---|---|
| E01 | Repositório público no GitHub com código modular em `src/` | Concluído | [Repositório FT03-Python](https://github.com/Maycon47/FT03-Python) |
| E02 | README com instruções, variáveis de ambiente e documentação das APIs | Concluído | `README.md`: instruções de execução, documentação das APIs e esclarecimento sobre autenticação não exigida |
| E03 | Executável ponta a ponta (`run.sh` ou comando único) | Concluído | `run.py`: execução pelo comando `python run.py` |
| E04 | Dataset final limpo e particionado em `output/` | Concluído | `output/dados_particionados/` |
| E05 | Relatório de Data Quality em JSON ou CSV | Concluído | `output/quality_report.json` |

## 5. Diretriz de desenvolvimento

O desenvolvimento deve priorizar os requisitos técnicos e os entregáveis obrigatórios definidos no enunciado original.

Cada implementação deverá conter documentação objetiva com objetivo, implementação, resultado e conclusão.

O notebook `01_data_discovery_usgs.ipynb` preserva a exploração das fontes.

O notebook `02_pipeline_implementacao.ipynb` será utilizado para desenvolver e validar os componentes do pipeline, quando apropriado.

O código final deverá ser organizado de forma modular em `src/`.

Funcionalidades adicionais, como dashboards no Power BI, não fazem parte dos entregáveis obrigatórios e poderão ser desenvolvidas posteriormente.

## 6. Observações sobre a avaliação

- **R04:** classificado como não aplicável porque as APIs públicas utilizadas não exigem credenciais. Não foram criadas variáveis ou chaves artificiais apenas para atender ao requisito.
- **R12:** a validação implementada contempla estrutura, valores nulos, unicidade e intervalos definidos no código. O status concluído indica que os critérios previstos no requisito foram implementados e testados, não que toda anomalia possível esteja descartada.
- **E02:** as instruções de execução e a documentação das APIs estão no README. A documentação deve esclarecer que as fontes utilizadas não exigem autenticação.
- Os status desta matriz refletem a implementação e os testes registrados durante o desenvolvimento do FT03-Python. A coluna de evidências indica os principais arquivos e artefatos relacionados a cada item.
