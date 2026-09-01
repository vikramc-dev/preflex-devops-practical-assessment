import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "projects.db"))
    # Import after changing the environment, then run the app lifespan.
    import app.database
    app.database.DATABASE_PATH = str(tmp_path / "projects.db")
    from app.main import app
    with TestClient(app) as test_client:
        yield test_client
