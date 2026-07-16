from abc import ABC, abstractmethod

from common.logger import logger


class BaseConnector(ABC):
    """
    Classe abstraite pour toutes les sources de données.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def extract(self):
        """
        Récupère les données.
        """
        pass

    @abstractmethod
    def upload(self, data):
        """
        Envoie les données.
        """
        pass

    def run(self):
        """
        Pipeline générique.
        """

        logger.info(f"🚀 {self.name} started")

        data = self.extract()

        self.upload(data)

        logger.info(f"✅ {self.name} finished")
