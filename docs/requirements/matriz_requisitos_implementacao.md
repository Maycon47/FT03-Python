# FT03 — Matriz de Requisitos e Implementação

**Projeto:** FT03 — Engenharia de Dados com Python
**Documento:** Matriz de Requisitos e Implementação
**Versão:** 1.0
**Status:** Aprovado para planejamento
**Repositório:** FT03-Python

---

## 1. Objetivo

Este documento estabelece a matriz de requisitos técnicos e as respectivas estratégias de implementação do projeto FT03.

Seu objetivo é garantir rastreabilidade entre as exigências do desafio, as decisões técnicas, os componentes desenvolvidos e os critérios utilizados para validar a solução.

A implementação deverá priorizar modularidade, qualidade de código, resiliência, segurança e reprodutibilidade.

## 2. Fontes de dados selecionadas

O projeto utilizará duas APIs públicas de domínios distintos:

| Fonte | Domínio | Finalidade |
|---|---|---|
| USGS Water Data API | Recursos hídricos | Obtenção de dados relacionados à qualidade da água |
| Open-Meteo API | Meteorologia | Obtenção de dados meteorológicos |

A integração dessas fontes permitirá explorar relacionamentos entre informações ambientais e meteorológicas.

A disponibilidade dos campos, os formatos de resposta e as possibilidades de cruzamento serão confirmados durante a etapa de Data Discovery.

## 3. Matriz de requisitos técnicos

### 3.1 Extração de dados e APIs

| ID | Requisito | Estratégia de implementação | Critério de aceite |
|---|---|---|---|
| R01 | Consumir no mínimo duas APIs públicas de domínios distintos | Desenvolver conectores independentes para USGS e Open-Meteo | Dados obtidos das duas fontes |
| R02 | Controle de taxa de requisições (Rate Limiting) | Implementar controle de frequência das chamadas HTTP | Requisições respeitam os limites das fontes |
| R03 | Retry e tratamento de erros | Implementar novas tentativas para falhas transitórias, com backoff | Falhas HTTP e indisponibilidade tratadas adequadamente |
| R04 | Segurança das credenciais | Utilizar variáveis de ambiente e arquivo .env | Nenhuma credencial publicada no GitHub |

### 3.2 Transformação e SQL

| ID | Requisito | Estratégia de implementação | Critério de aceite |
|---|---|---|---|
| R05 | Código modular em Python | Separar extração, transformação e qualidade em módulos | Código organizado e reutilizável |
| R06 | Type Hints e funções limpas | Aplicar tipagem estática e responsabilidades bem definidas | Funções documentadas e tipadas |
| R07 | Manipulação de coleções complexas via SQL | Utilizar DuckDB para consultar JSONs e estruturas aninhadas | Consultas demonstrando operações sobre arrays e JSON |
| R08 | Transformações estruturadas | Implementar no mínimo cinco transformações | Cinco operações documentadas e testadas |

As transformações previstas são:

1. Padronização de tipos e datas.
2. Tratamento de valores nulos.
3. Deduplicação de registros.
4. Cruzamento de fontes utilizando JOIN.
5. Enriquecimento de dados com métricas adicionais.

### 3.3 Qualidade e persistência

| ID | Requisito | Estratégia de implementação | Critério de aceite |
|---|---|---|---|
| R09 | Validação de schema | Verificar estrutura e tipos dos dados | Schema validado automaticamente |
| R10 | Cálculo de null ratio | Medir proporção de valores nulos por campo | Métricas calculadas e registradas |
| R11 | Unicidade | Verificar duplicidade nas chaves definidas | Testes de unicidade executados |
| R12 | Testes de intervalo | Validar limites e intervalos dos campos aplicáveis | Registros inválidos identificados |
| R13 | Relatório de Data Quality | Exportar resultados em JSON ou CSV | Relatório disponível em reports/ |
| R14 | Persistência dos dados finais | Gravar dataset em formato Parquet | Arquivo Parquet gerado |
| R15 | Particionamento temporal | Organizar os arquivos por ano e mês, quando aplicável | Estrutura temporal validada |
| R16 | Compressão | Utilizar compressão Parquet, preferencialmente Snappy | Arquivo final comprimido e legível |

## 4. Arquitetura de implementação

O fluxo lógico previsto será:

```text
USGS API ──────────┐
                   │
                   ▼
              EXTRAÇÃO
              (Python)
                   │
                   ▼
              DADOS RAW
              (JSON)
                   │
                   ▼
          TRANSFORMAÇÃO
          (Python + DuckDB)
                   │
                   ▼
             DATA QUALITY
              (Python)
                   │
                   ▼
          PERSISTÊNCIA FINAL
              (Parquet)
                   │
             ┌─────┴─────┐
             ▼           ▼
          OUTPUT      REPORTS
          Parquet     JSON/CSV

Open-Meteo API ─────┘
```

A arquitetura será refinada após a inspeção das respostas reais das APIs.

## 5. Organização dos componentes

| Componente | Responsabilidade |
|---|---|
| src/extraction/ | Conectores e coleta das APIs |
| src/transformation/ | Padronização, limpeza e cruzamento |
| src/quality/ | Validações e métricas de qualidade |
| sql/ | Consultas SQL e manipulação de JSON |
| config/ | Configurações do projeto |
| data/raw/ | Dados originais extraídos |
| data/processed/ | Dados intermediários |
| output/ | Dataset final em Parquet |
| reports/ | Relatórios de qualidade |
| tests/ | Testes automatizados |

## 6. Entregáveis obrigatórios

| Entregável | Localização | Situação |
|---|---|---|
| Repositório Git público | GitHub | Concluído |
| Código-fonte modular | src/ | Pendente |
| Documentação de execução | README.md | Pendente de complementação |
| Dependências | requirements.txt | Pendente de definição |
| Script executável | run.sh ou comando equivalente | Pendente |
| Dataset final | output/ | Pendente |
| Relatório de Data Quality | reports/ | Pendente |

## 7. Critérios gerais de qualidade

A solução será considerada concluída quando:

- As duas fontes públicas forem consumidas corretamente.
- O pipeline tratar falhas de comunicação e limites de requisição.
- As transformações forem reproduzíveis.
- As operações SQL sobre estruturas complexas estiverem demonstradas.
- As validações de qualidade forem executadas automaticamente.
- O dataset final estiver disponível em Parquet, com particionamento e compressão.
- O relatório de qualidade for exportado.
- O projeto puder ser executado seguindo as instruções do README.

## 8. Decisões e pontos pendentes

Os seguintes pontos serão definidos durante o Data Discovery:

- Endpoints específicos de cada API.
- Parâmetros e períodos de consulta.
- Campos e schemas efetivamente disponíveis.
- Chaves de relacionamento entre as fontes.
- Estratégia de tratamento de dados ausentes.
- Regras específicas de unicidade e intervalos.
- Volume de dados esperado.
- Estratégia de particionamento final.

Nenhuma dessas definições deverá ser presumida sem inspeção dos dados.

## 9. Histórico de versões

| Versão | Descrição |
|---|---|
| 1.0 | Criação da matriz de requisitos e estratégias iniciais de implementação |

---

**Responsável:** Projeto FT03 — Engenharia de Dados com Python

**Princípio de desenvolvimento:** cada requisito deverá possuir implementação verificável, documentação e evidência de execução.
