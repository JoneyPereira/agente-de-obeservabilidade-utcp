import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Configurações do Dynatrace
DT_TENANT_URL = "https://abc12345.live.dynatrace.com"
DT_API_TOKEN = "dt0c01.XXXXX.YYYYY"

class BottleneckParams(BaseModel):
    entity_id: str
    time_window: str = "now-15m"
    min_duration_ms: int = 1000

@app.post("/utcp/dynatrace/bottlenecks")
async def handle_dynatrace_tool(params: BottleneckParams):
    """
    Este endpoint é o que o UTCP Registry chama fisicamente.
    """
    
    # 1. Traduzindo para a Query do Dynatrace (DQL ou API v2)
    # Exemplo simples usando a API de Metrics/Problems
    url = f"{DT_TENANT_URL}/api/v2/problems"
    headers = {"Authorization": f"Api-Token {DT_API_TOKEN}"}
    
    query_params = {
        "entitySelector": f"type(SERVICE),entityId({params.entity_id})",
        "from": params.time_window
    }

    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()
        raw_data = response.json()

        # 2. Filtragem e Limpeza (Crucial para o LLM não se perder)
        # Transformamos um JSON gigante em algo legível
        insights = []
        for problem in raw_data.get('problems', []):
            if problem.get('severityLevel') == 'PERFORMANCE':
                insights.append({
                    "id": problem.get("displayId"),
                    "title": problem.get("title"),
                    "start_time": problem.get("startTime"),
                    "status": "Aberto" if problem.get("status") == "OPEN" else "Resolvido"
                })

        return {
            "status": "success",
            "data_summary": insights,
            "instruction": "Analise os problemas de performance acima e correlacione com os logs de banco de dados."
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))