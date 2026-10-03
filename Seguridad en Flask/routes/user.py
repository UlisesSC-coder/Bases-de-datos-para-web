from markupsafe import escape
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User
from forms import RegisterForm, LoginForm, EditProfileForm

users_bp = Blueprint("users", __name__)


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
        if current_user.is_authenticated:
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
            login_user(user)
            flash(f"Bienvenido, {user.username}", "success")
            return redirect(url_for("users.index"))
        flash("Credenciales inválidas", "error")
    return render_template("login.html", form=form)

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for("users.index"))


@users_bp.route("/logout")
@login_required
def saludo():
    return f"<h1>Hola, {escape(current_user.username)}</h1>"


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
            flash("Usuario actualizado", "success")
            return redirect(url_for("users.index"))
    return render_template("edit_profile.html", form=form, user=user)


@users_bp.route("/profile/<int:id>/delete", methods=["POST"])
@login_required
def delete_profile(id):
    user = User.query.get_or_404(id)
    username = user.username
    es_propio = (id == current_user.id)

    db.session.delete(user)
    db.session.commit()

    if es_propio:
        logout_user()
        flash("Tu cuenta fue eliminada", "success")
    else:
        flash(f"Usuario {username} eliminado", "success")
    return redirect(url_for("users.index"))