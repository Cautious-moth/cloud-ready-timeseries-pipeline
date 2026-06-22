from src.pipeline import Pipeline


def test_pipeline_run_completes_without_error(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")

    from src.config import Settings

    pipeline = Pipeline(settings=Settings.from_env())
    pipeline.run()
