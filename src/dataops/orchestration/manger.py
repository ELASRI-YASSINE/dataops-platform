# src/dataops/orchestration/manager.py
"""
RÔLE : Gestionnaire des DAGs Airflow
       Permet de déclencher les DAGs depuis le code Python
       Utile pour les tests et le debugging
"""

import subprocess
from common.logger import get_logger

logger = get_logger(__name__)

class DAGManager:
    """Gère les opérations sur les DAGs Airflow"""

    def trigger(self, dag_id: str) -> bool:
        """Déclenche un DAG manuellement"""
        try:
            result = subprocess.run(
                ["airflow", "dags", "trigger", dag_id],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                logger.info(f"✅ DAG déclenché : {dag_id}")
                return True
            else:
                logger.error(f"❌ Erreur déclenchement {dag_id} : {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ {e}")
            return False

    def pause(self, dag_id: str) -> bool:
        """Met un DAG en pause"""
        try:
            subprocess.run(["airflow", "dags", "pause", dag_id])
            logger.info(f"⏸️  DAG mis en pause : {dag_id}")
            return True
        except Exception as e:
            logger.error(f"❌ {e}")
            return False

    def unpause(self, dag_id: str) -> bool:
        """Active un DAG"""
        try:
            subprocess.run(["airflow", "dags", "unpause", dag_id])
            logger.info(f"▶️  DAG activé : {dag_id}")
            return True
        except Exception as e:
            logger.error(f"❌ {e}")
            return False

    def list_dags(self) -> list:
        """Liste tous les DAGs"""
        try:
            result = subprocess.run(
                ["airflow", "dags", "list"],
                capture_output=True, text=True
            )
            return result.stdout
        except Exception as e:
            logger.error(f"❌ {e}")
            return []
