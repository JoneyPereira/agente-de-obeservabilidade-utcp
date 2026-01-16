# Agente IA SRE — Arquitetura de Resposta a Incidentes com LLMs

![UTCP + AI SRE](Gemini_Generated_Image_f3gle5f3gle5f3gl.png)

## 📌 Visão Geral

Este repositório documenta a **arquitetura de um Agente de IA para SRE (Site Reliability Engineering)**, projetado para **investigar incidentes em produção**, correlacionar dados de observabilidade e **propor ações de remediação**, respeitando regras de segurança, SLA e aprovação humana.

O foco deste projeto **não é implementação**, mas sim **arquitetura, domínio e decisões técnicas**, aplicando boas práticas de:

- Arquitetura de Software
- Domain-Driven Design (DDD)
- C4 Model
- Architecture Decision Records (ADR)
- Observabilidade e SRE
- Uso responsável de LLMs em ambientes críticos

---

## 🎯 Objetivo do Projeto

Demonstrar como um **agente baseado em LLM** pode ser usado de forma **segura e governada** para:

- Apoiar engenheiros de plantão (on-call)
- Reduzir MTTR (Mean Time to Resolution)
- Automatizar investigação de incidentes
- Evitar alucinações por meio de dados reais
- Manter controle humano sobre decisões críticas

---

## 🧠 Escopo e Delimitação de Domínio

### Bounded Context: **Agente IA SRE**

Este projeto define **explicitamente** um único domínio central:

> **Agente IA SRE** — responsável por investigação, correlação e decisão.

### Dentro do escopo
- Raciocínio do agente
- Formulação de hipóteses
- Estratégia de investigação
- Correlação de métricas, eventos e logs
- Proposta de ações de remediação
- Aplicação de regras de negócio e políticas

### Fora do escopo (tratados como sistemas externos)
- Dynatrace, Elasticsearch, Kubernetes
- Slack ou outros canais de comunicação
- Execução direta de ações em produção
- Workflow completo de incidentes

Essa separação garante **clareza arquitetural e baixo acoplamento**.

---

## 🧩 Arquitetura — C4 Model

### C4 — Level 1: Context Diagram

Mostra como o **Agente IA SRE** se relaciona com pessoas e sistemas externos.

```mermaid
C4Context
    title Context Diagram - Agente IA SRE

    Person(oncall, "On-call Engineer", "Responsável por incidentes em produção")

    System(agent, "Agente IA SRE", "Investiga incidentes e propõe remediações")

    System_Ext(utcp, "UTCP Tool Registry", "Descoberta e invocação de ferramentas")
    System_Ext(obs, "Plataformas de Observabilidade", "Dynatrace, Elasticsearch, etc.")
    System_Ext(approval, "Sistema de Aprovação Humana", "Autoriza ações de remediação")
    System_Ext(slack, "Slack", "Comunicação e relatórios")

    Rel(oncall, agent, "Fornece contexto do incidente")
    Rel(agent, utcp, "Descobre e invoca tools")
    Rel(utcp, obs, "Executa consultas")
    Rel(agent, approval, "Solicita aprovação")
    Rel(agent, slack, "Publica relatórios")
```

### C4 — Level 2: Container Diagram

Detalha a organização interna do Agente.

```mermaid
C4Container
    title Container Diagram - Agente IA SRE

    Person(oncall, "On-call Engineer")

    System_Boundary(agent, "Agente IA SRE") {
        Container(api, "Incident Analysis API", "REST / Async", "Recebe contexto do incidente")
        Container(core, "Agent Core", "LLM + Policies", "Raciocínio e tomada de decisão")
        Container(orchestrator, "Tool Orchestrator", "UTCP Client", "Invocação de tools")
        Container(policy, "Policy Engine", "Rules Engine", "Aplica invariantes")
        Container(report, "Incident Reporter", "Markdown / JSON", "Geração de relatórios")
    }

    System_Ext(utcp, "UTCP Tool Registry")
    System_Ext(approval, "Sistema de Aprovação Humana")
    System_Ext(slack, "Slack")

    Rel(oncall, api, "Abre incidente")
    Rel(api, core, "Contexto do incidente")
    Rel(core, policy, "Valida decisões")
    Rel(core, orchestrator, "Solicita dados")
    Rel(orchestrator, utcp, "Invoca tools")
    Rel(core, approval, "Solicita aprovação")
    Rel(report, slack, "Publica relatório")
```

### C4 — Level 3: Component Diagram (Agent Core)

Mostra onde está o valor de negócio principal.

```mermaid
C4Component
    title Component Diagram - Agent Core

    Container(agent, "Agent Core") {
        Component(hypothesis, "Hypothesis Builder", "LLM Prompting", "Formula hipóteses")
        Component(strategy, "Investigation Strategy", "Decision Logic", "Define estratégia de investigação")
        Component(correlation, "Correlation Engine", "Business Logic", "Correlaciona dados")
        Component(decision, "Remediation Decision Engine", "Policy-aware", "Propõe ações")
    }

    Container(policy, "Policy Engine")
    Container(orchestrator, "Tool Orchestrator")

    Rel(hypothesis, strategy, "Gera hipóteses")
    Rel(strategy, orchestrator, "Solicita dados")
    Rel(correlation, decision, "Fornece evidências")
    Rel(decision, policy, "Valida ações")
```

## 📄 Architecture Decision Records (ADR)
### ADR-001 — Definição do Bounded Context “Agente IA SRE”

Status: Accepted
Decisão:
Definir o Agente IA SRE como um bounded context independente, responsável apenas por investigação, correlação e decisão.

Consequências:
- Clareza de domínio
- Menor acoplamento
- Evolução independente

### ADR-002 — Uso de UTCP para Acesso a Ferramentas

Status: Accepted
Decisão:
Todas as integrações com sistemas externos ocorrem via UTCP Tools, evitando dependências diretas.
Consequências:

- Padronização
- Segurança
- Reuso por múltiplos agentes

### ADR-003 — Human-in-the-Loop para Remediações

Status: Accepted
Decisão:
Nenhuma ação destrutiva pode ser executada sem aprovação humana explícita.
Consequências:

- Redução de risco
- Compliance
- O agente atua como advisor

### ADR-004 — SLA de Investigação como Regra de Domínio

Status: Accepted
Decisão:
O agente deve gerar um diagnóstico preliminar dentro de um SLA configurável.
Consequências:

- Limite de tempo para investigação
- Controle de chamadas externas
- Melhor suporte ao on-call

### ADR-005 — Restrição de Auto-Remediação por Metadata

Status: Accepted
Decisão:
Somente serviços marcados explicitamente como auto_remediation=true podem receber ações automáticas.
Consequências:

- Compliance by design
- Governança clara
- Prevenção de ações indevidas

### 🧠 Conclusão

Este projeto demonstra uma abordagem realista e responsável para o uso de LLMs em ambientes de produção críticos, com foco em:
Arquitetura sólida
Limites claros de domínio
Decisões explícitas e rastreáveis
Separação entre inteligência, infraestrutura e execução
