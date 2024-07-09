import os
from flask import Flask
from bookish.models import db, migrate
from bookish.controllers import register_controllers
from bookish.services.error_handler import *


def create_app():
    app = Flask(__name__)

    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    register_controllers(app)

    app.register_error_handler(BadToken, lambda x: x)
    app.register_error_handler(Conflict, lambda x: x)
    app.register_error_handler(InternalServerError, lambda x: x)
    app.register_error_handler(NotFound, not_found)
    app.register_error_handler(BadRequest, lambda x: x)
    app.register_error_handler(Created, created)

    if __name__ == "__main__":
        app.run()

    return app
