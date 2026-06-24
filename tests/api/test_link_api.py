import pytest
from sqlmodel import Session, SQLModel

from app.db.session import engine
from app.main import create_app
from app.services.link_service import create_link_service


@pytest.fixture
def create_test_link(short_name="ex1"):
    with Session(engine) as session:
        link = create_link_service(
            session=session,
            original_url="https://example.com",
            short_name=short_name,
        )

        return link


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()


def test_create_link(client):
    response = client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["short_name"] == "ex1"
    assert data["short_url"] == "https://short.com/ex1"

def test_create_link_bad_body(client):
    response = client.post(
        "/api/links",
        data="null",
        content_type="application/json")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid JSON body"}

def test_create_link_already_exist(client):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    response_2 = client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    assert response_2.status_code == 409
    assert response_2.get_json() == {"error": "Link already exists"}

def test_get_all_links(client):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    response = client.get("/api/links?range=[0,10]")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 1
    assert data[0]["short_name"] == "ex1"
    assert data[0]["short_url"] == "https://short.com/ex1"

def test_get_link(client, monkeypatch):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    response = client.get("/api/links/1")
    assert response.status_code == 200
    # assert response["short_url"] == "https://short.com/ex1"

def test_get_all_link(client):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex2",
        },
    )

    response = client.get("/api/links")

    assert response.status_code == 200

def test_update_link(client):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    response_2 = client.put(
        "/api/links/1",
        json={
            "original_url": "https://short.com",
            "short_name": "ex2",
        },
    )

    get_response_2 = client.get("/api/links/1")

    assert response_2.status_code == 200
    assert get_response_2.get_json()["short_url"] == "https://short.com/ex2"

def test_delete_link(client):
    client.post(
        "/api/links",
        json={
            "original_url": "https://short.com",
            "short_name": "ex1",
        },
    )

    response = client.delete("/api/links/1")

    get_response_2 = client.get("/api/links/1")

    assert response.status_code == 204
    assert get_response_2.get_json() == {'error': 'Link not found'}
