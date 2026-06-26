from sqlmodel import Session, func, select

from app.models.link import Link


def get_links_count(session: Session):
    statement = select(func.count()).select_from(Link)
    return session.exec(statement).one()

def get_all_links(session: Session, offset: int = 0, limit: int = 10):
    statement = select(Link).offset(offset).limit(limit)
    return session.exec(statement).all()


def get_link_by_id(session: Session, id: int):
    return session.get(Link, id)


def get_link_by_name(session: Session, short_name: str):
    statement = select(Link).where(Link.short_name == short_name)

    return session.exec(statement).first()


def create_link(session: Session, original_url: str, short_name: str, short_url: str):
    link = Link(original_url=original_url, short_name=short_name, short_url=short_url)
    session.add(link)
    session.commit()
    session.refresh(link)

    return link


def update_link(session: Session, id: int, original_url: str, short_name: str, short_url: str):
    link = session.get(Link, id)

    if link is None:
        return None

    link.original_url = original_url
    link.short_name = short_name
    link.short_url = short_url

    session.add(link)
    session.commit()
    session.refresh(link)

    return link


def delete_link(session: Session, id: int):
    link = session.get(Link, id)

    if link is None:
        return False

    session.delete(link)
    session.commit()

    return True
