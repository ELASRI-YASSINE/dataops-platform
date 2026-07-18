# common/exceptions.py
"""
Exceptions personnalisées du projet
Permet de distinguer les erreurs métier des erreurs système
"""

class DataOpsException(Exception):
    """Exception de base du projet"""
    pass

class IngestionError(DataOpsException):
    """Erreur lors de l'ingestion des données"""
    pass

class StorageError(DataOpsException):
    """Erreur lors du stockage dans GCS"""
    pass

class ValidationError(DataOpsException):
    """Erreur de validation des données"""
    pass

class TransformationError(DataOpsException):
    """Erreur lors de la transformation"""
    pass

class APIError(DataOpsException):
    """Erreur lors d'un appel API externe"""
    def __init__(self, api_name: str, status_code: int, message: str):
        self.api_name    = api_name
        self.status_code = status_code
        super().__init__(f"{api_name} API error {status_code}: {message}")
