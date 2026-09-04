import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
    TEMPLATE_FOLDER = "templates"
    STATIC_FOLDER = "static"
