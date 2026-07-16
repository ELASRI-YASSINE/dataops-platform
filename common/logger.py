import logging
import os
from pathlib import Path

# Dossier des logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "dataops.log"

logger = logging.getLogger("dataops")
logger.setLevel(logging.INFO)

# Évite les handlers dupliqués
if not logger.handlers:

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Affichage terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Écriture dans un fichier
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
