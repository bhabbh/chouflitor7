# config.py
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///chouflitor7.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

    @staticmethod
    def init_app(app):
        if not Config.GOOGLE_MAPS_API_KEY:
            raise ValueError("No Google Maps API Key set for Flask application")
