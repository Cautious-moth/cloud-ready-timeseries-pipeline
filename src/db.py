from contextlib import contextmanager
from typing import Iterator

import psycopg

from src.config import Settings


@contextmanager
def connect(settings: Settings) -> Iterator[psycopg.Connection]:
    with psycopg.connect(settings.database_url) as conn:
        yield conn


def verify_connection(settings: Settings) -> dict[str, str]:
    with connect(settings) as conn:
        row = conn.execute(
            """
            SELECT extversion
            FROM pg_extension
            WHERE extname = 'timescaledb'
            """
        ).fetchone()

        if row is None:
            raise RuntimeError("TimescaleDB extension is not installed")

        return {"timescaledb_version": row[0]}


def start_pipeline_run(settings: Settings) -> str:
    with connect(settings) as conn:
        row = conn.execute(
            """
            INSERT INTO pipeline_runs (status)
            VALUES ('running')
            RETURNING run_id::text
            """
        ).fetchone()
        conn.commit()

    if row is None:
        raise RuntimeError("Failed to create pipeline run record")

    return row[0]


def complete_pipeline_run(settings: Settings, run_id: str) -> None:
    with connect(settings) as conn:
        conn.execute(
            """
            UPDATE pipeline_runs
            SET status = 'completed', completed_at = NOW()
            WHERE run_id = %s::uuid
            """,
            (run_id,),
        )
        conn.commit()
