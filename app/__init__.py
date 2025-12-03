import os

from flask import Flask

from .models import db
from .routes import bp as main_blueprint


def create_app():
    root_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(os.path.dirname(root_dir), "templates")
    static_dir = os.path.join(os.path.dirname(root_dir), "static")
    data_dir = os.path.join(os.path.dirname(root_dir), "data")
    os.makedirs(data_dir, exist_ok=True)

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir,
    )
    app.config["SECRET_KEY"] = os.getenv(
        "FLASK_SECRET_KEY", "change-me-for-production"
    )
    database_path = os.path.join(data_dir, "app.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{database_path}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
