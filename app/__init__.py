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

    from auth import db, login_manager

    db.init_app(app)
    login_manager.init_app(app)

    from auth.models import User
    from roles import ADMIN_ROLE

    from auth.routes import auth_bp
    from routes.users_route import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

        if not User.query.filter_by(email="admin@sena").first():
            admin = User(nombre="Administrador", email="admin@sena", role=ADMIN_ROLE)
            admin.set_password("12345")
            db.session.add(admin)
            db.session.commit()

    return app
