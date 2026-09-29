from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, session
from extensions import db
from models import User
from forms import RegisterForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Debes iniciar sesión para ver esa página", "error")
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return wrapper


@users_bp.route("/")
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("user_list.html", users=users)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        if "user_id" in session:
            flash("Usuario creado", "success")
            return redirect(url_for("users.index"))
        flash("Registro exitoso, ya puedes iniciar sesión", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Bienvenido, {user.username}", "success")
            return redirect(url_for("users.index"))
        flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html", form=form)


@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("users.index"))


@users_bp.route("/profile/<int:id>")
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template("profile.html", user=user)


@users_bp.route("/profile/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditProfileForm(obj=user)
    if form.validate_on_submit():
        repetido = User.query.filter(
            ((User.username == form.username.data) | (User.email == form.email.data))
            & (User.id != user.id)
        ).first()
        if repetido:
            flash("Ese usuario o correo ya está en uso", "error")
        else:
            user.username = form.username.data
            user.nombre = form.nombre.data
            user.apellido = form.apellido.data
            user.email = form.email.data
            db.session.commit()
            if session["user_id"] == user.id:
                session["username"] = user.username
            flash("Usuario actualizado", "success")
            return redirect(url_for("users.index"))
    return render_template("edit_profile.html", form=form, user=user)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    user = User.query.get_or_404(id)
    username = user.username
    db.session.delete(user)
    db.session.commit()

    if session["user_id"] == id:
        session.clear()
        flash("Tu cuenta fue eliminada", "success")
    else:
        flash(f"Usuario {username} eliminado", "success")
    return redirect(url_for("users.index"))