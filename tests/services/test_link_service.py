import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.services.link_service import (
    LinkAlreadyExistsError,
    LinkNotFoundError,
    create_link_service,
    delete_link_service,
    get_all_links_service,
    get_link_by_id_service,
    update_link_service,
)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session



def test_create_link_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    link = create_link_service(
        session=session,
        original_url="https://short.com",
        short_name="ex"
    )

    assert link.short_url == "https://short.com/ex"

def test_create_link_service_no_base_url(session, monkeypatch):
    monkeypatch.delenv("BASE_URL", raising=False)

    with pytest.raises(ValueError):
        create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex"
        )

def test_create_link_service_duplicate(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex"
        )

    with pytest.raises(LinkAlreadyExistsError):
        create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex"
        )

def test_get_all_links_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    link_1 = create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex1"
        )

    link_2 = create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex2"
        )

    links, total = get_all_links_service(session, 0, 0)

    assert len(links) == 1
    assert total == 2
    assert link_1 in links
    assert link_2 not in links

def test_get_link_by_id_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    link_1 = create_link_service(
            session=session,
            original_url="https://short.com",
            short_name="ex1"
        )

    result = get_link_by_id_service(session, link_1.id)

    assert result.id == link_1.id
    assert result.original_url == link_1.original_url
    assert result.short_name == link_1.short_name
    assert result.short_url == link_1.short_url

def test_get_link_by_id_not_found(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    create_link_service(
        session=session,
        original_url="https://short.com",
        short_name="ex1"
    )

    with pytest.raises(LinkNotFoundError):
        get_link_by_id_service(session, "link_1.id")

def test_delete_link_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    link = create_link_service(
        session=session,
        original_url="https://short.com",
        short_name="ex"
    )

    delete_link_service(session, link.id)

    with pytest.raises(LinkNotFoundError):
        get_link_by_id_service(session, link.id)

def test_delete_link_not_found_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    create_link_service(
        session=session,
        original_url="https://short.com",
        short_name="ex"
    )

    with pytest.raises(LinkNotFoundError):
        delete_link_service(session, "link.id")

def test_update_link_service(session, monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://short.com")

    link = create_link_service(
        session=session,
        original_url="https://short.com",
        short_name="ex"
    )

    update_link_service(
        session,
        id = link.id,
        original_url=link.original_url,
        short_name = "new"
    )

    assert link.short_url == "https://short.com/new"
