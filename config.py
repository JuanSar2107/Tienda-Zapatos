import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    TEMPLATE_FOLDER = "templates"
    STATIC_FOLDER = "static"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///tienda.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
