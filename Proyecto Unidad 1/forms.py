from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User


class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=50)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(max=50)])
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden")],
    )
    submit = SubmitField("Registrarme")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ese usuario ya existe")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Ese correo ya está registrado")


class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class EditProfileForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=50)])
    apellido = StringField("Apellido", validators=[DataRequired(), Length(max=50)])
    email = StringField("Correo", validators=[DataRequired(), Email(), Length(max=100)])
    submit = SubmitField("Guardar cambios")