import os
import sys  # Certifique-se de importar o módulo sys
import requests

# Triggered by an HTTP request
def get_gcp_service():
    # Verifica se está rodando no Google Colab
    if "google.colab" in sys.modules:
        return "colab-etl"

    # Verifica se está no Cloud Functions
    if "K_SERVICE" in os.environ:
        return "function-etl"

    # Verifica se está em uma VM do Compute Engine
    if os.path.exists("/sys/class/dmi/id/product_name"):
        with open("/sys/class/dmi/id/product_name") as f:
            if "Google" in f.read():
                return "Google Compute Engine (VM)"
            
    # Verifica se está no Dataflow
    if "DATAFLOW_JOB_ID" in os.environ:
        return "Google Dataflow"

    # Verifica se está no Dataproc
    if os.path.exists("/etc/dataproc"):
        return "Google Dataproc"

    # Verifica se está no Kubernetes Engine (GKE)
    if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount"):
        return "Google Kubernetes Engine (GKE)"

    # Tenta obter metadados da GCP
    try:
        response = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/name",
            headers={"Metadata-Flavor": "Google"},
            timeout=2,
        )
        if response.status_code == 200:
            return "Google Compute Engine (VM)"
    except requests.exceptions.RequestException:
        pass

    return "Serviço desconhecido ou ambiente local"



def get_source_bucket():
    # Verifica se está rodando no Google Colab
    if "google.colab" in sys.modules:
        return "colab-etl"