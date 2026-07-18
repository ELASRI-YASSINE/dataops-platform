# common/utils.py
"""
Fonctions utilitaires réutilisables dans tout le projet
"""
import os
import json
from datetime import datetime
from common.logger import get_logger

logger = get_logger(__name__)

def get_timestamp(fmt: str = "%Y-%m-%d_%H-%M") -> str:
    """Retourne le timestamp actuel formaté"""
    return datetime.utcnow().strftime(fmt)

def ensure_dir(path: str) -> None:
    """Crée un dossier s'il n'existe pas"""
    os.makedirs(path, exist_ok=True)

def file_size_mb(path: str) -> float:
    """Retourne la taille d'un fichier en MB"""
    return round(os.path.getsize(path) / (1024 * 1024), 2)

def save_json(data: dict, path: str) -> None:
    """Sauvegarde un dict en JSON localement"""
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"💾 Sauvegardé localement : {path}")

def load_json(path: str) -> dict:
    """Charge un fichier JSON"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
