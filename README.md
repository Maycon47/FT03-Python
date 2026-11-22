# FT03-Python: Pipeline de Engenharia de Dados

## 1. Sobre o projeto

Projeto desenvolvido como parte da formação em Engenharia de Dados, com o objetivo de construir um pipeline de dados utilizando Python, APIs públicas, SQL e tecnologias de armazenamento analítico.

A solução realiza a extração de dados de diferentes fontes, transformação, integração, enriquecimento, validação de qualidade e persistência em formato Parquet.

O projeto utiliza dados de localizações de monitoramento disponibilizados pela USGS e informações meteorológicas fornecidas pela Open-Meteo.

## 2. Objetivos

- Consumir dados de pelo menos duas APIs públicas de domínios distintos.
- Desenvolver uma arquitetura modular utilizando Python.
- Aplicar técnicas de transformação e integração de dados.
- Utilizar SQL para relacionar diferentes fontes.
- Implementar verificações de qualidade dos dados.
- Gerar relatórios de execução e auditoria.
- Persistir os dados em formato Parquet.
- Aplicar compressão Snappy e particionamento temporal.
- Desenvolver um fluxo de execução automatizado.

## 3. Arquitetura do projeto

O pipeline foi organizado em módulos independentes, coordenados por um único ponto de entrada.

```text

APIs Públicas
     |
     v
Extração de dados
     |
     v
Padronização de tipos
     |
     v
Tratamento de valores nulos
     |
     v
Remoção de duplicidades
     |
     v
Integração SQL com DuckDB
     |
     v
Enriquecimento com métricas
     |
     v
Validação da qualidade
     |
     +-------------------+
     |                   |
     v                   v
Relatório JSON      Persistência Parquet
                         |
                         v
                  Compressão Snappy
                         |
                         v
                 Particionamento
                    Ano / Mês

```


O arquivo `run.py` coordena a execução das etapas do pipeline.

## 4. Fontes de dados

### 4.1 USGS

**United States Geological Survey**

API utilizada para consultar localizações de monitoramento, incluindo identificadores, nomes, estados e coordenadas geográficas.

Endpoint:

https://api.waterdata.usgs.gov/ogcapi/v1/collections/monitoring-locations/items

### 4.2 Open-Meteo

API pública utilizada para consultar informações meteorológicas por coordenadas geográficas.

Endpoint:

https://api.open-meteo.com/v1/forecast

Variáveis meteorológicas utilizadas:

- Temperatura a 2 metros.
- Umidade relativa do ar.
- Precipitação.
- Velocidade do vento a 10 metros.

**Autenticação:** as APIs utilizadas nas consultas implementadas não exigem chaves de autenticação.

## 5. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python 3.13 | Linguagem principal |
| Pandas | Manipulação e transformação de dados |
| Requests | Consumo das APIs |
| DuckDB | Processamento SQL e integração |
| PyArrow | Persistência em Parquet |
| Jupyter Notebook | Exploração e documentação técnica |
| VS Code | Ambiente de desenvolvimento |
| Git | Controle de versão |
| GitHub | Hospedagem do projeto |

### 5.1 Cliente HTTP e confiabilidade das requisições

O módulo `APIClient` centraliza as requisições HTTP e implementa:

- Timeout para requisições.
- Rate Limiting para controlar a frequência das chamadas.
- Retry para falhas temporárias.
- Backoff exponencial entre tentativas.
- Tratamento de erros HTTP e respostas inválidas.

Essa implementação permite reutilizar o mesmo cliente HTTP nos módulos de extração.

## 6. Estrutura de diretórios

```text
FT03-Python/
│
├── config/
├── data/
├── docs/
│
├── notebooks/
│   ├── 01_data_discovery_usgs.ipynb
│   ├── 02_pipeline_implementacao.ipynb
│   └── MATRIZ_REQUISITOS.md
│
├── output/
│   ├── quality_report.json
│   └── dados_particionados/
│       └── ano=2026/
│           └── mes=11/
│               └── *.parquet
│
├── reports/
├── sql/
│
├── src/
│   ├── extraction/
│   │   ├── api_client.py
│   │   ├── open_meteo_client.py
│   │   ├── pipeline.py
│   │   └── usgs_client.py
│   │
│   ├── quality/
│   │   ├── report.py
│   │   ├── storage.py
│   │   └── validate.py
│   │
│   └── transformation/
│       └── transform.py
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
├── run.py

```

Organização dos diretórios:

- `notebooks/`: exploração, desenvolvimento e documentação dos experimentos.
- `src/extraction/`: clientes HTTP e extração das APIs.
- `src/transformation/`: padronização, tratamento, integração e enriquecimento.
- `src/quality/`: validação, auditoria e persistência dos dados.
- `output/`: arquivos gerados pelo pipeline.
- `config/`, `data/`, `docs/`, `reports/`, `sql/` e `tests/`: diretórios reservados para organização e evolução do projeto.


Os diretórios reservados ainda não possuem funcionalidades implementadas.

## 7. Configuração do ambiente

### 7.1 Pré-requisitos

- Python 3.13.0, versão utilizada durante o desenvolvimento e validação.
- Git.
- Visual Studio Code, recomendado.
- Ambiente virtual Python.

### 7.2 Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd FT03-Python
```

### 7.3 Criar o ambiente virtual

Windows PowerShell:

```powershell
python -m venv .venv
```

### 7.4 Ativar o ambiente virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 7.5 Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

## 8. Execução do pipeline

Com o ambiente virtual ativado e estando na raiz do projeto, execute:

```powershell
python run.py
```

O arquivo `run.py` coordena todas as etapas do processamento:

1. **Extração:** consumo das APIs USGS e Open-Meteo.
2. **Padronização:** ajuste dos tipos de dados e formatos das colunas.
3. **Tratamento de valores nulos:** remoção de registros sem informações obrigatórias.
4. **Deduplicação:** identificação e remoção de registros duplicados.
5. **Integração:** relacionamento das fontes utilizando SQL INNER JOIN no DuckDB.
6. **Enriquecimento:** cálculo de métricas meteorológicas por localização.
7. **Validação:** verificação da estrutura, completude, unicidade e validade.
8. **Auditoria:** geração do relatório de execução e qualidade em JSON.
9. **Persistência:** armazenamento em Parquet com compressão Snappy e particionamento temporal.

## 9. Transformações e métricas

O projeto implementa as seguintes transformações:

- Padronização de tipos de dados e datas.
- Tratamento de valores nulos em campos obrigatórios.
- Remoção de registros duplicados.
- Integração das fontes utilizando INNER JOIN no DuckDB.
- Cálculo da temperatura média por localização.
- Cálculo da precipitação acumulada por localização.
- Cálculo da velocidade média do vento por localização.

### 9.1 Integração das fontes

O relacionamento entre os dados meteorológicos e os metadados das localizações utiliza a chave `codigo_localizacao`.

A operação SQL utilizada é o `INNER JOIN`, permitindo associar as medições meteorológicas às respectivas informações geográficas.

### 9.2 Enriquecimento dos dados

São calculadas três métricas agrupadas por localização:

| Métrica | Cálculo |
|---|---|
| Temperatura média | Média de `temperature_2m` |
| Precipitação acumulada | Soma de `precipitation` |
| Velocidade média do vento | Média de `wind_speed_10m` |

## 10. Qualidade dos dados

A validação contempla quatro dimensões:

| Dimensão | Verificação |
|---|---|
| Estrutura | Presença das colunas obrigatórias |
| Completude | Quantidade e proporção de valores nulos |
| Unicidade | Identificação de registros duplicados |
| Validade | Verificação dos intervalos numéricos |

Os resultados são organizados em um relatório estruturado e exportados em formato JSON para auditoria.

## 11. Armazenamento dos dados

A camada final utiliza o formato Apache Parquet.

Características implementadas:

- Armazenamento colunar.
- Compressão Snappy.
- Particionamento temporal por ano e mês.
- Preservação dos tipos de dados.

### 11.1 Estrutura de saída

```text
output/
│
├── quality_report.json
│
└── dados_particionados/
    └── ano=2026/
        └── mes=11/
            └── *.parquet
```

O particionamento permite organizar os dados temporalmente e facilita a leitura de períodos específicos.

## 12. Resultados da execução validada

Na execução de referência do pipeline completo foram obtidos:

| Indicador | Resultado |
|---|---:|
| Fontes de dados | 2 APIs |
| Localizações processadas | 5 |
| Registros meteorológicos | 120 |
| Colunas originais enriquecidas | 13 |
| Valores nulos | 0 |
| Registros duplicados | 0 |
| Arquivos Parquet particionados | 1 |
| Compressão | Snappy |
| Particionamento | Ano / Mês |

Os resultados representam a execução realizada durante o desenvolvimento. A quantidade de registros pode variar conforme as respostas das APIs.

## 13. Credenciais e variáveis de ambiente

As APIs utilizadas nas consultas implementadas são públicas e não exigem chaves de autenticação.

Portanto, não existem credenciais obrigatórias para executar o pipeline atual.


## 14. Documentação técnica

Os notebooks disponíveis em `notebooks/` preservam o processo de exploração, desenvolvimento e validação das etapas do projeto.

- `01_data_discovery_usgs.ipynb`: exploração inicial dos dados da USGS.
- `02_pipeline_implementacao.ipynb`: implementação e validação dos componentes do pipeline.
- `MATRIZ_REQUISITOS.md`: acompanhamento dos requisitos técnicos e entregáveis.

O notebook de implementação também documenta experimentos técnicos com DuckDB, incluindo a exploração e normalização de estruturas JSON utilizando consultas SQL.

Esses experimentos fazem parte da documentação de desenvolvimento e não são etapas executadas pelo `run.py`.

## 15. Licença

A licença de distribuição será definida antes da publicação pública do repositório.

## 16. Autor

Projeto desenvolvido como exercício prático de aprendizagem em Engenharia de Dados.
