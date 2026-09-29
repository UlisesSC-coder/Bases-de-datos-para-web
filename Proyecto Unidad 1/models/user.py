from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column("usuario", db.String(50), unique=True, nullable=False)
    email = db.Column("correo", db.String(100), unique=True, nullable=False)
    password_hash = db.Column("contrasena", db.String(255), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    telefono = db.Column(db.String(15))
    created_at = db.Column("fecha_registro", db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)