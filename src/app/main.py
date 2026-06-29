import os

import sentry_sdk
from flask import Flask
from flask_cors import CORS

from app.api.link_api import link_api
from app.db.session import create_db_and_tables

sentry_dsn = os.getenv("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(dsn=sentry_dsn, send_default_pii=True)


def create_app():
    app = Flask(__name__)
    create_db_and_tables()
    app.register_blueprint(link_api)

    @app.get("/ping")
    def ping():
        return "pong", 200

    return app


app = create_app()
CORS(app, resources={
    r"/api/*": {
        "origins": "http://localhost:5173",
        "expose_headers": ["Content-Range"]
        }
    },
     )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
