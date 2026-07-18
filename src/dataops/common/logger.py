# common/logger.py
"""
Logger centralisé — utilisé par tous les modules
Format uniforme avec timestamp, niveau, module
"""
import logging
import os
import sys
from datetime import datetime

def get_logger(name: str) -> logging.Logger:
    """
    Retourne un logger configuré pour le module donné
    Usage : logger = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Format : 2025-06-15 10:23:01 | INFO | ingestion.olist | message
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    os.makedirs("logs", exist_ok=True)
    today     = datetime.now().strftime("%Y-%m-%d")
    file_h    = logging.FileHandler(f"logs/pipeline_{today}.log")
    file_h.setFormatter(formatter)
    logger.addHandler(file_h)

    return logger
