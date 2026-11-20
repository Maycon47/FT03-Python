# FT03: Matriz de Requisitos e Entregáveis

## 1. Extração de dados e APIs

  ---------------------------------------------------------------------------------------------
  ID                Requisito         Situação          Evidência
  ----------------- ----------------- ----------------- ---------------------------------------
  R01               Consumir no       Concluído         `src/extraction/usgs_client.py` e
                    mínimo duas APIs                    `src/extraction/open_meteo_client.py`
                    públicas de                         
                    domínios                            
                    distintos                           

  R02               Implementar       Concluído         `src/extraction/api_client.py`
                    controle de taxas                   
                    (Rate Limiting)                     

  R03               Implementar       Concluído         `src/extraction/api_client.py`
                    retentativas                        
                    (Retry) e                           
                    tratamento de                       
                    erros                               

  R04               Gerenciar         Não aplicável     As APIs públicas utilizadas, USGS e
                    credenciais por                     Open-Meteo, não exigem chaves de
                    variáveis de                        autenticação.
                    ambiente, sem                       
                    versionar chaves                    
  ---------------------------------------------------------------------------------------------

## 2. Transformação e SQL

  ----------------------------------------------------------------------------------------------------
  ID                Requisito         Situação          Evidência
  ----------------- ----------------- ----------------- ----------------------------------------------
  R05               Desenvolver       Concluído         Organização dos módulos em `src/` e execução
                    scripts modulares                   pelo `run.py`
                    em Python, com                      
                    funções e Type                      
                    Hints                               

  R06               Desaninhar arrays Concluído         Notebook
                    e estruturas JSON                   `notebooks/02_pipeline_implementacao.ipynb`,
                    utilizando SQL,                     seção de exploração de JSON com DuckDB
                    DuckDB, SQLite ou                   
                    PySpark                             

  R07               Padronizar tipos  Concluído         `src/transformation/transform.py`, função
                    e datas                             `standardize_data_types()`

  R08               Tratar valores    Concluído         `src/transformation/transform.py`, função
                    nulos                               `handle_null_values()`

  R09               Deduplicar        Concluído         `src/transformation/transform.py`, função
                    registros                           `remove_duplicates()`

  R10               Cruzar fontes de  Concluído         `src/transformation/transform.py`, função
                    dados utilizando                    `join_data_sources()`
                    JOIN                                

  R11               Enriquecer os     Concluído         `src/transformation/transform.py`, função
                    dados com                           `enrich_with_metrics()`
                    métricas                            
  ----------------------------------------------------------------------------------------------------

**Observação:** os requisitos R07 a R11 compõem as cinco transformações
obrigatórias.

## 3. Data Quality e persistência

  -----------------------------------------------------------------------------------------------------
  ID                Requisito         Situação          Evidência
  ----------------- ----------------- ----------------- -----------------------------------------------
  R12               Validar schema,   Concluído         `src/quality/validate.py`
                    null ratio,                         
                    unicidade e                         
                    intervalos                          

  R13               Exportar          Concluído         `src/quality/report.py` e
                    relatório de                        `output/quality_report.json`
                    execução e                          
                    auditoria de                        
                    qualidade em JSON                   
                    ou CSV                              

  R14               Persistir a       Concluído         `src/quality/storage.py` e
                    camada final em                     `output/dados_particionados/`
                    Parquet ou Delta                    
                    Lake                                

  R15               Aplicar           Concluído         `src/quality/storage.py`, função
                    compressão Snappy                   `save_partitioned_parquet()`

  R16               Implementar       Concluído         `src/quality/storage.py` e
                    particionamento                     `output/dados_particionados/ano=.../mes=.../`
                    temporal, como                      
                    ano e mês                           
  -----------------------------------------------------------------------------------------------------

## 4. Entregáveis obrigatórios

  -----------------------------------------------------------------------------------------------
  ID                Entregável        Situação          Evidência
  ----------------- ----------------- ----------------- -----------------------------------------
  E01               Repositório       Concluído         Repositório público:
                    público no GitHub                   https://github.com/Maycon47/FT03-Python
                    com código                          
                    modular em `src/`                   

  E02               README com        Concluído         `README.md`; a necessidade de credenciais
                    instruções,                         é esclarecida como não aplicável às APIs
                    variáveis de                        utilizadas
                    ambiente e                          
                    documentação das                    
                    APIs                                

  E03               Executável ponta  Concluído         `run.py`; execução pelo comando
                    a ponta (`run.sh`                   `python run.py`
                    ou comando único)                   

  E04               Dataset final     Concluído         `output/dados_particionados/`
                    limpo e                             
                    particionado em                     
                    `output/`                           

  E05               Relatório de Data Concluído         `output/quality_report.json`
                    Quality em JSON                     
                    ou CSV                              
  -----------------------------------------------------------------------------------------------

## 5. Diretriz de desenvolvimento

O desenvolvimento deve priorizar os requisitos técnicos e os entregáveis
obrigatórios definidos no enunciado original.

Cada implementação deverá conter documentação objetiva com objetivo,
implementação, resultado e conclusão.

O notebook `01_data_discovery_usgs.ipynb` preserva a exploração das
fontes.

O notebook `02_pipeline_implementacao.ipynb` será utilizado para
desenvolver e validar os componentes do pipeline, quando apropriado.

O código final deverá ser organizado de forma modular em `src/`.

Funcionalidades adicionais, como dashboards no Power BI, não fazem parte
dos entregáveis obrigatórios e poderão ser desenvolvidas posteriormente.

## 6. Observações sobre a avaliação

-   **R04:** classificado como não aplicável porque as APIs públicas
    utilizadas não exigem credenciais. Não foram criadas variáveis ou
    chaves artificiais apenas para atender ao requisito.
-   **R12:** a validação implementada contempla estrutura, valores
    nulos, unicidade e intervalos definidos no código. O status
    concluído indica que os critérios previstos no requisito foram
    implementados e testados, não que toda anomalia possível esteja
    descartada.
-   **E02:** as instruções de execução e a documentação das APIs estão
    no README. A seção de credenciais deve explicar que as fontes
    utilizadas não exigem autenticação.
-   Os status desta matriz refletem a implementação e os testes
    registrados durante o desenvolvimento do FT03-Python. A coluna de
    evidências indica os principais arquivos e artefatos relacionados a
    cada item.
