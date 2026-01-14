# Agentic Observability com UTCP (Universal Tool Calling Protocol)

Este documento descreve a arquitetura de observabilidade baseada em agentes, onde um LLM atua como um SRE (Site Reliability Engineer) automatizado, utilizando o protocolo **UTCP** para investigar incidentes em fontes de dados como Elasticsearch, Dynatrace e sistemas de métricas.

---

## 1. Visão Geral do Fluxo Arquitetural

A arquitetura separa a inteligência (LLM) da execução técnica (UTCP Tools). O agente não recebe apenas logs, ele "decide" quais dados consultar com base na evolução da investigação.

```mermaid
graph TD
    A[Alerta/Incidente Trigger] --> B{AI SRE Agent / LLM}
    B -->|1. Escolhe Ferramenta| C[UTCP Registry / utcp.io]
    
    subgraph "Camada de Execução (UTCP)"
        C --> D[Tool: ElasticSearch Logs]
        C --> E[Tool: Dynatrace Traces]
        C --> F[Tool: Metric Dashboards]
    end

    D --> G[Data Sources]
    E --> G
    F --> G

    G -->|Dados Filtrados| H[UTCP Adapter]
    H -->|Contexto Enriquecido| B
    
    B -->|2. Nova Hipótese| C
    B -->|3. Diagnóstico Final| I[Análise & Recomendação]