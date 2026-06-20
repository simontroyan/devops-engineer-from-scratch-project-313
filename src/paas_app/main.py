import os

import sentry_sdk
from flask import Flask

sentry_dsn = os.getenv("SENTRY_DSN")

if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        send_default_pii=True
    )

def create_app():
    app = Flask(__name__)

    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'

    @app.errorhandler(404)
    def page_not_found(e):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal server error"}, 500


    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
