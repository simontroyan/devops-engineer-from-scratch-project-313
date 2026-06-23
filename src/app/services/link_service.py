import os

from app.repositories.link_repository import (
    create_link,
    delete_link,
    get_all_links,
    get_link_by_id,
    get_link_by_name,
    update_link,
)


class LinkAlreadyExistsError(Exception):
    pass


class LinkNotFoundError(Exception):
    pass


class NotAllowedToUpdate(Exception):
    pass


def create_link_service(session, original_url: str, short_name: str):
    base_url = os.getenv("BASE_URL")

    if not base_url:
        raise ValueError("BASE_URL is empty")

    if _is_link_duplicate(session, short_name):
        raise LinkAlreadyExistsError()

    short_url = f"{base_url}/{short_name}"

    return create_link(session, original_url, short_name, short_url)


def get_all_links_service(session, range):
    offset = range[0]
    limit = range[1]

    return get_all_links(session, offset, limit)


def get_link_by_id_service(session, id: int):
    link = get_link_by_id(session, id)

    if link is None:
        raise LinkNotFoundError()

    return link


def delete_link_service(session, id: int):
    deleted_link = delete_link(session, id)

    if not deleted_link:
        raise LinkNotFoundError()

    return deleted_link


def update_link_service(session, id: int, original_url: str, short_name: str):
    base_url = os.getenv("BASE_URL")

    if not base_url:
        raise ValueError("BASE_URL is empty")

    existing_link = get_link_by_id(session, id)

    if existing_link is None:
        raise LinkNotFoundError()

    link_with_same_name = get_link_by_name(session, short_name)

    if link_with_same_name is not None and link_with_same_name.id != id:
        raise LinkAlreadyExistsError()

    short_url = f"{base_url}/{short_name}"

    return update_link(session, id, original_url, short_name, short_url)


def _is_link_duplicate(session, short_name: str) -> bool:
    return get_link_by_name(session, short_name) is not None
