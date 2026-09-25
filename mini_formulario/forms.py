from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class RegistroForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(min=3, max=50)]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(), Email()]
    )

    enviar = SubmitField('Registrar')

#Comprobación 2: explica en una oración qué valida DataRequired, Length y Email.
#DataRequired valida que el campo no esté vacío, 
# Length valida que la longitud del texto esté dentro de un rango específico, 
# y Email valida que el formato del correo electrónico sea correcto.