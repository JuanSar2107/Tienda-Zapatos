import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    TEMPLATE_FOLDER = "templates"
    STATIC_FOLDER = "static"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + str(BASE_DIR / "tienda.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
