import logging
from dataclasses import dataclass

from src.config import Settings

logger = logging.getLogger(__name__)


@dataclass
class Pipeline:
    """Orchestrates idempotent ETL stages for time-series ingestion."""

    settings: Settings

    def run(self) -> None:
        logger.info("Starting pipeline run")
        self._extract()
        self._transform()
        self._load()
        logger.info("Pipeline run completed")

    def _extract(self) -> None:
        logger.debug("Extract stage (not yet implemented)")

    def _transform(self) -> None:
        logger.debug("Transform stage (not yet implemented)")

    def _load(self) -> None:
        logger.debug("Load stage (not yet implemented)")
