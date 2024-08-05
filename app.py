import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.context_processor
def inject_google_maps_api_key():
    return dict(google_maps_api_key=app.config["GOOGLE_MAPS_API_KEY"])


db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    from models import User

    return User.query.get(int(user_id))


# route import after the app and db are initialized to avoid circular imports
from routes import (
    home,
    available_matches,
    full_matches,
    create_match,
    join_match,
    search_matches,
)

# auth routes import
from auth import login, logout, signup

# Register main routes
app.add_url_rule("/", "home", home)
app.add_url_rule("/available_matches", "available_matches", available_matches)
app.add_url_rule("/full_matches", "full_matches", full_matches)
app.add_url_rule("/create_match", "create_match", create_match, methods=["GET", "POST"])
app.add_url_rule(
    "/join_match/<int:match_id>", "join_match", join_match, methods=["POST"]
)
app.add_url_rule(
    "/search_matches", "search_matches", search_matches, methods=["GET", "POST"]
)

# Register auth routes
app.add_url_rule("/login", "auth.login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "auth.logout", logout)
app.add_url_rule("/signup", "auth.signup", signup, methods=["GET", "POST"])


@app.route("/check-api-key")
def check_api_key():
    api_key = app.config.get("GOOGLE_MAPS_API_KEY")
    return f"API Key: {api_key[:5]}...{api_key[-5:]}" if api_key else "API Key not set"


if __name__ == "__main__":
    app.run(debug=False)
