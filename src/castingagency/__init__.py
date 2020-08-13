import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
cors = CORS()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    from src.castingagency.api import api

    api.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
