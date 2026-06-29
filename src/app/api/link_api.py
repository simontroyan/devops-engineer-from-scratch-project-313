import json

from flask import Blueprint, make_response, request
from sqlmodel import Session

from app.db.session import engine
from app.services.link_service import (
    LinkAlreadyExistsError,
    LinkNotFoundError,
    create_link_service,
    delete_link_service,
    get_all_links_service,
    get_link_by_id_service,
    update_link_service,
)

link_api = Blueprint("link_api", __name__)


@link_api.post("/api/links")
def links_post():
    data = request.get_json()

    if data is None:
        return {"error": "Invalid JSON body"}, 400

    if not isinstance(data, dict) or "original_url" not in data or "short_name" not in data:
        return {"detail": {"error": "Missing required fields"}}, 422

    try:
        with Session(engine) as session:
            link = create_link_service(
                session=session, original_url=data["original_url"], short_name=data["short_name"]
            )

        response = make_response(
            {
            "id": link.id,
            "original_url": link.original_url,
            "short_name": link.short_name,
            "short_url": link.short_url
            }
        , 201)

        return response
    except LinkAlreadyExistsError:
        return {"error": "Link already exists"}, 409

@link_api.get("/api/links")
def links_get():
    range_raw = request.args.get("range", "[0,10]")

    try:
        range_values = json.loads(range_raw)
    except json.JSONDecodeError:
        return {"error": "Invalid range"}, 400

    if (
        not isinstance(range_values, list)
        or len(range_values) != 2
        or not all(isinstance(value, int) for value in range_values)
    ):
        return {"error": "Range must be [offset, limit]"}, 400

    start = range_values[0]
    end = range_values[1]

    with Session(engine) as session:
        links, total = get_all_links_service(session, start, end)

    response = make_response([
        {
            "id": link.id,
            "original_url": link.original_url,
            "short_name": link.short_name,
            "short_url": link.short_url,
        }
        for link in links
    ], 200)

    response.headers["Content-Range"] = f'links {start}-{end}/{total}'
    return response

@link_api.get("/api/links/<int:link_id>")
def link_get(link_id):
    try:
        with Session(engine) as session:
            link = get_link_by_id_service(session, link_id)
    except LinkNotFoundError:
        return {"detail": "Link not found"}, 404

    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": link.short_url,
    }, 200


@link_api.delete("/api/links/<int:link_id>")
def link_delete(link_id):
    try:
        with Session(engine) as session:
            delete_link_service(session, link_id)
    except LinkNotFoundError:
        return {"detail": "Link not found"}, 404

    return "", 204


@link_api.put("/api/links/<int:link_id>")
def link_update(link_id):
    data = request.get_json()

    if data is None:
        return {"error": "Invalid JSON body"}, 400

    if not isinstance(data, dict) or "original_url" not in data or "short_name" not in data:
        return {"detail": {"error": "Missing required fields"}}, 422


    try:
        with Session(engine) as session:
            link = update_link_service(
                session=session, id=link_id, original_url=data["original_url"], short_name=data["short_name"]
            )

    except LinkNotFoundError:
        return {"detail": "Link not found"}, 404
    except LinkAlreadyExistsError:
        return {"error": "Link already exists"}, 409
    except KeyError:
        return {"error": "Missing required field"}, 400
    except ValueError:
        return {"error": "Server configuration error"}, 500

    return {
        "id": link.id,
        "original_url": link.original_url,
        "short_name": link.short_name,
        "short_url": link.short_url,
    }, 200
