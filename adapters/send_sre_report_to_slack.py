import requests
import json

def send_sre_report_to_slack(report_data):
    """
    Envia o relatório gerado pelo Agente IA para um canal do Slack
    usando Webhooks e Block Kit para formatação rica.
    """
    webhook_url = "https://hooks.slack.com/services/T00000/B00000/XXXXXXXX"

    # Montando a estrutura visual do Slack
    slack_payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 Incidente Resolvido pelo Agente IA: {report_data['incident_id']}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Serviço:*\n`{report_data['service']}`"},
                    {"type": "mrkdwn", "text": f"*Severidade:*\n`{report_data['severity']}`"}
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Causa Raiz:*\n{report_data['root_cause']}"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Ação Recomendada:*\n{report_data['action_plan']}"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "🛠️ *Tools UTCP consultadas:* Elasticsearch, Dynatrace, Historical Baseline."
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Aprovar Rollback ↩️"},
                        "style": "danger",
                        "value": "rollback_id_123"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Ver no Dynatrace 📊"},
                        "url": "https://dynatrace.com/..."
                    }
                ]
            }
        ]
    }

    response = requests.post(
        webhook_url, 
        data=json.dumps(slack_payload),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise ValueError(f"Erro no Slack: {response.status_code}, {response.text}")

# Exemplo de dados vindos da análise do LLM
data = {
    "incident_id": "INC-2026-0812",
    "service": "checkout-service",
    "severity": "CRITICAL (P1)",
    "root_cause": "Database Lock Contention detectado na tabela `stock_items` após deploy v2.4.1.",
    "action_plan": "Executar Rollback imediato para v2.4.0 e aplicar índices de banco sugeridos."
}

# Disparar envio
send_sre_report_to_slack(data)