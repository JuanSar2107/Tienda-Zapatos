from pathlib import Path

from flask import Flask

from config import Config


BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / config_class.TEMPLATE_FOLDER),
        static_folder=str(BASE_DIR / config_class.STATIC_FOLDER),
    )
    app.config.from_object(config_class)

    from routes.auth import auth_bp
    from routes.users_route import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app
