from unittest.mock import MagicMock, patch

import pytest

from src.config import Settings
from src.db import complete_pipeline_run, start_pipeline_run, verify_connection


@pytest.fixture
def settings() -> Settings:
    return Settings(database_url="postgresql://postgres:postgres@localhost:5432/timeseries")


def test_verify_connection_returns_timescaledb_version(settings: Settings) -> None:
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = ("2.17.0",)

    with patch("src.db.psycopg.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        result = verify_connection(settings)

    assert result == {"timescaledb_version": "2.17.0"}


def test_verify_connection_raises_when_extension_missing(settings: Settings) -> None:
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = None

    with patch("src.db.psycopg.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        with pytest.raises(RuntimeError, match="TimescaleDB extension"):
            verify_connection(settings)


def test_start_pipeline_run_returns_run_id(settings: Settings) -> None:
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = ("abc-123",)

    with patch("src.db.psycopg.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        run_id = start_pipeline_run(settings)

    assert run_id == "abc-123"
    mock_conn.commit.assert_called_once()


def test_complete_pipeline_run_commits(settings: Settings) -> None:
    mock_conn = MagicMock()

    with patch("src.db.psycopg.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        complete_pipeline_run(settings, "abc-123")

    mock_conn.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
