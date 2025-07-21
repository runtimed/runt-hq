import pytest
from fastapi.testclient import TestClient
from runt_hq.main import app


@pytest.fixture
def client():
    """Test client for the FastAPI application."""
    return TestClient(app)


def test_root_endpoint_returns_hello_world(client):
    """Test that the root endpoint returns the expected hello world message."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_root_endpoint_response_format(client):
    """Test that the root endpoint returns a valid JSON response."""
    response = client.get("/")

    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_root_endpoint_http_methods(client):
    """Test that the root endpoint only accepts GET requests."""
    # GET should work
    response = client.get("/")
    assert response.status_code == 200

    # POST should not work
    response = client.post("/")
    assert response.status_code == 405

    # PUT should not work
    response = client.put("/")
    assert response.status_code == 405

    # DELETE should not work
    response = client.delete("/")
    assert response.status_code == 405
