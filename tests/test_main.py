import pytest

from src.app.main import create_app


@pytest.fixture
def client():
    app = create_app()
    client = app.test_client()

    return client


def test_get_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200


def test_page_not_found(client):
    response = client.get("/not_found")

    assert response.status_code == 404


def test_internal_error(client):
    @client.application.route("/error")
    def error():
        raise RuntimeError("Test error")

    response = client.get("/error")

    assert response.status_code == 500
