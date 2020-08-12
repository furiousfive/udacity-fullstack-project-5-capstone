import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

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



    # register blueprints
    from src.castingagency.api.routes.ping import ping_blueprint
    from src.castingagency.api.routes.actors import actors_blueprint
    from src.castingagency.api.routes.movies import movies_blueprint
    from src.castingagency.api.routes.casting import casts_blueprint
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(actors_blueprint)
    app.register_blueprint(movies_blueprint)
    app.register_blueprint(casts_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app