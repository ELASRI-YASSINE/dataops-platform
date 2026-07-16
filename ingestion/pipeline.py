import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def run_step(name: str, func, *args) -> bool:
    logger.info(f"\n{'─'*50}")
    logger.info(f"▶  {name}")
    logger.info(f"{'─'*50}")
    try:
        func(*args)
        logger.info(f"✅ {name} — SUCCÈS")
        return True
    except Exception as e:
        logger.error(f"❌ {name} — ÉCHEC : {e}")
        return False


def run():
    from upload_to_gcs         import upload_olist
    from ingest_exchange_rates import run as run_exchange
    from ingest_weather        import run as run_weather

    start   = datetime.utcnow()
    results = {}

    logger.info("=" * 55)
    logger.info("🚀 PIPELINE D'INGESTION COMPLET")
    logger.info("=" * 55)

    results["Olist Dataset"]   = run_step("📦 Olist Dataset",  upload_olist, "data/")
    results["Exchange Rates"]  = run_step("💱 Exchange Rates", run_exchange)
    results["Weather Data"]    = run_step("🌤️  Weather Data",  run_weather)

    duration = (datetime.utcnow() - start).seconds

    logger.info("\n" + "=" * 55)
    logger.info("📊 RAPPORT FINAL")
    logger.info("=" * 55)
    for name, ok in results.items():
        status = "✅ SUCCESS" if ok else "❌ FAILED"
        logger.info(f"  {status}  {name}")
    logger.info(f"\n⏱️  Durée : {duration}s")

    if not all(results.values()):
        sys.exit(1)
    logger.info("🎉 Pipeline terminé avec succès !")


if __name__ == "__main__":
    run()