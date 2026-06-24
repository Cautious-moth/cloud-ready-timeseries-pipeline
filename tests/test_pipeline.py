from unittest.mock import patch

import pytest

from src.config import Settings
from src.pipeline import Pipeline


def test_pipeline_run_completes_without_error(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    settings = Settings.from_env()

    with (
        patch("src.pipeline.verify_connection", return_value={"timescaledb_version": "2.17.0"}),
        patch("src.pipeline.start_pipeline_run", return_value="run-1"),
        patch("src.pipeline.complete_pipeline_run") as mock_complete,
    ):
        pipeline = Pipeline(settings=settings)
        pipeline.run()

    mock_complete.assert_called_once_with(settings, "run-1")


@pytest.mark.integration
def test_pipeline_run_against_live_database():
    settings = Settings.from_env()
    Pipeline(settings=settings).run()
