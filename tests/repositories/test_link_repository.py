import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.repositories.link_repository import create_link, delete_link, get_all_links, get_link_by_id, update_link


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

def test_create_link(session):
    link = create_link(
            session,
            original_url="https://example.com/long-url",
            short_name="exmpl",
            short_url="https://short.io/r/exmpl"
        )

    assert link.id is not None
    assert link.original_url == "https://example.com/long-url"
    assert link.short_name == "exmpl"
    assert link.short_url == "https://short.io/r/exmpl"

def test_get_links_with_limit(session):
    create_link(session, "url1", "one", "short1")
    create_link(session, "url2", "two", "short2")
    create_link(session, "url3", "three", "short3")

    links = get_all_links(session, offset=0, limit=2)

    assert len(links) == 2

def test_get_links_with_offset(session):
    create_link(session, "url1", "one", "short1")
    create_link(session, "url2", "two", "short2")
    create_link(session, "url3", "three", "short3")

    links = get_all_links(session, offset=1, limit=2)

    assert len(links) == 2
    assert links[0].short_name == "two"

def test_get_all_links(session):
    create_link(
            session,
            original_url="https://example.com/long-url",
            short_name="exmpl",
            short_url="https://short.io/r/exmpl"
    )
    create_link(
            session,
            original_url="https://example.com/long-url-2",
            short_name="exmpl2",
            short_url="https://short.io/r/exmpl2"
    )

    links = get_all_links(session)

    assert len(links) == 2

def test_get_link_by_id(session):
    link = create_link(
            session,
            original_url="https://example.com/long-url",
            short_name="exmpl",
            short_url="https://short.io/r/exmpl"
    )

    link_res = get_link_by_id(session, link.id)

    assert link.id == link_res.id
    assert link.original_url == "https://example.com/long-url"
    assert link.short_name == "exmpl"
    assert link.short_url == "https://short.io/r/exmpl"

def test_get_link_by_id_none(session):
    link_res = get_link_by_id(session, 2)

    assert link_res is None

def test_update_link(session):
    link = create_link(
            session,
            original_url="https://example.com/long-url",
            short_name="exmpl",
            short_url="https://short.io/r/exmpl"
    )
    updated_link = update_link(
                session,
                id=link.id,
                original_url="https://example.com/long-url",
                short_name="newexmpl",
                short_url="https://short.io/r/newexmpl"
    )

    assert updated_link.id == link.id
    assert updated_link.original_url == "https://example.com/long-url"
    assert updated_link.short_name == "newexmpl"
    assert updated_link.short_url == "https://short.io/r/newexmpl"
    
def test_update_link_none(session):
    updated_link = update_link(
                session,
                id=2,
                original_url="https://example.com/long-url",
                short_name="newexmpl",
                short_url="https://short.io/r/newexmpl"
    )

    assert updated_link is None

def test_delete_link(session):
    link = create_link(
            session,
            original_url="https://example.com/long-url",
            short_name="exmpl",
            short_url="https://short.io/r/exmpl"
    )

    result = delete_link(session, link.id)

    assert result is True
    assert get_link_by_id(session, link.id) is None

def test_delete_link_none(session):
    result = delete_link(session, 2)

    assert result is False