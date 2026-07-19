# src/dataops/orchestration/registry.py
"""
RÔLE : Registre central de tous les DAGs
       Définit les métadonnées de chaque DAG
"""

DAGS_REGISTRY = {
    "dataops_master": {
        "description" : "DAG Master — orchestre tout le pipeline",
        "schedule"    : "0 4 * * *",
        "tags"        : ["master", "dataops"],
        "owner"       : "dataops-team",
    },
    "ingestion_pipeline": {
        "description" : "Ingestion Olist + Exchange + Weather → GCS",
        "schedule"    : "0 5 * * *",
        "tags"        : ["ingestion"],
        "owner"       : "data-engineering",
    },
    "transformation_pipeline": {
        "description" : "Spark → BigQuery Bronze → dbt Silver/Gold",
        "schedule"    : "0 6 * * *",
        "tags"        : ["transformation", "dbt"],
        "owner"       : "data-engineering",
    },
}

def get_dag_info(dag_id: str) -> dict:
    """Retourne les infos d'un DAG"""
    return DAGS_REGISTRY.get(dag_id, {})

def list_all_dags() -> list:
    """Retourne la liste de tous les DAGs"""
    return list(DAGS_REGISTRY.keys())
