import pytest
from fastapi.testclient import TestClient
from runt_hq.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def app_instance():
    """FastAPI app instance for testing."""
    return app
