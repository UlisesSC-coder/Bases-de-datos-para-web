from flask import Flask, render_template
from flask_wtf import CSRFProtect
from config import Config
from extensions import db, login_manager
from routes.user import users_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CSRFProtect(app)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    login_manager.login_message = "Debes iniciar sesión para ver esa página"
    login_manager.login_message_category = "error"

    app.register_blueprint(users_bp)

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template("401.html"), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("403.html"), 403

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run(debug=True)