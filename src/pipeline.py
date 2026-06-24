import logging
from dataclasses import dataclass, field

from src.config import Settings
from src.db import complete_pipeline_run, start_pipeline_run, verify_connection

logger = logging.getLogger(__name__)


@dataclass
class Pipeline:
    """Orchestrates idempotent ETL stages for time-series ingestion."""

    settings: Settings
    run_id: str | None = field(default=None, init=False)

    def run(self) -> None:
        logger.info("Starting pipeline run")

        db_info = verify_connection(self.settings)
        logger.info("Connected to TimescaleDB %s", db_info["timescaledb_version"])

        self.run_id = start_pipeline_run(self.settings)
        logger.info("Pipeline run id: %s", self.run_id)

        try:
            self._extract()
            self._transform()
            self._load()
        except Exception:
            logger.exception("Pipeline run %s failed", self.run_id)
            raise
        else:
            complete_pipeline_run(self.settings, self.run_id)
            logger.info("Pipeline run completed")

    def _extract(self) -> None:
        logger.debug("Extract stage (not yet implemented)")

    def _transform(self) -> None:
        logger.debug("Transform stage (not yet implemented)")

    def _load(self) -> None:
        logger.debug("Load stage (not yet implemented)")
