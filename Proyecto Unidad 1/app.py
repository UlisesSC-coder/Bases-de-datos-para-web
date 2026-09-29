from flask import Flask
from flask_wtf import CSRFProtect
from config import Config
from extensions import db
from routes.user import users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CSRFProtect(app)
    app.register_blueprint(users_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)