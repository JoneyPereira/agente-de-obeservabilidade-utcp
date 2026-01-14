from kubernetes import client, config

def perform_k8s_rollback(deployment_name, namespace, reason):
    """
    Interage com a API do Kubernetes para reverter um deployment.
    """
    try:
        # Carrega a config do cluster (ou In-Cluster se rodar num Pod)
        config.load_kube_config()
        apps_v1 = client.AppsV1Api()

        # No K8s, o rollback é essencialmente um 'patch' para a revisão anterior
        # ou o uso da estratégia de 'undo'
        body = {
            "kind": "DeploymentRollback",
            "apiVersion": "extensions/v1beta1", # Dependendo da versão do cluster
            "name": deployment_name,
            "rollbackTo": {"revision": 0} # 0 indica a versão imediatamente anterior
        }
        
        # Simplificando via patch de anotação para forçar o rollout undo
        # Ou disparando via comando shell para fins de exemplo claro:
        import subprocess
        cmd = f"kubectl rollout undo deployment/{deployment_name} -n {namespace}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        return {
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout if result.returncode == 0 else result.stderr
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}