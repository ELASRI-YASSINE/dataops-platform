# pipeline.py
"""
Point d'entrée principal de la plateforme DataOps
Lance tous les connecteurs dans l'ordre
C'est ce qu'Airflow appellera via un BashOperator
"""
import sys
from datetime import datetime
from common.logger import get_logger
from ingestion.olist.ingest    import OlistConnector
from ingestion.exchange.ingest import ExchangeConnector
from ingestion.weather.ingest  import WeatherConnector

logger = get_logger("pipeline")

def run():
    start = datetime.utcnow()

    logger.info("=" * 60)
    logger.info("🚀 DATAOPS PLATFORM — PIPELINE PRINCIPAL")
    logger.info(f"   Démarrage : {start.isoformat()}")
    logger.info("=" * 60)

    # Définition des connecteurs dans l'ordre d'exécution
    connectors = [
        ("📦 Olist Dataset",  OlistConnector()),
        ("💱 Exchange Rates", ExchangeConnector()),
        ("🌤️  Weather Data",  WeatherConnector()),
    ]

    results = {}
    for name, connector in connectors:
        logger.info(f"\n{'─' * 50}")
        logger.info(f"▶  {name}")
        logger.info(f"{'─' * 50}")
        results[name] = connector.run()

    # Rapport final
    duration = (datetime.utcnow() - start).seconds
    logger.info("\n" + "=" * 60)
    logger.info("📊 RAPPORT FINAL")
    logger.info("=" * 60)
    for name, ok in results.items():
        status = "✅ SUCCESS" if ok else "❌ FAILED"
        logger.info(f"  {status}  {name}")
    logger.info(f"\n⏱️  Durée totale : {duration}s")
    logger.info("=" * 60)

    if not all(results.values()):
        logger.error("💥 Pipeline terminé avec des erreurs !")
        sys.exit(1)

    logger.info("🎉 Pipeline terminé avec succès !")

if __name__ == "__main__":
    run()
