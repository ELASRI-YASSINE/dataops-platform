# ingestion/base/connector.py
"""
Classe abstraite BaseConnector
Tous les connecteurs d'ingestion héritent de cette classe
Garantit une interface uniforme pour tous les sources de données
"""
from abc import ABC, abstractmethod
from common.logger import get_logger

class BaseConnector(ABC):
    """
    Interface commune pour tous les connecteurs d'ingestion
    Chaque source (Olist, Weather, Exchange) implémente cette classe
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    def extract(self) -> any:
        """Extrait les données depuis la source"""
        pass

    @abstractmethod
    def validate(self, data: any) -> bool:
        """Valide les données extraites"""
        pass

    @abstractmethod
    def load(self, data: any) -> bool:
        """Charge les données dans GCS"""
        pass

    def run(self) -> bool:
        """
        Exécute le pipeline complet : Extract → Validate → Load
        Méthode principale appelée par Airflow
        """
        self.logger.info(f"🚀 Démarrage {self.__class__.__name__}")
        try:
            data = self.extract()
            if not self.validate(data):
                raise ValueError("Validation échouée")
            self.load(data)
            self.logger.info(f"✅ {self.__class__.__name__} terminé")
            return True
        except Exception as e:
            self.logger.error(f"❌ {self.__class__.__name__} échoué : {e}")
            return False
