from flask import Flask, render_template, redirect, url_for, session, flash
from forms import RegistroForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '041202'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroForm()

    if form.validate_on_submit():
        session['nombre'] = form.nombre.data
        flash('Registro realizado correctamente.')
        return redirect(url_for('index'))

    return render_template(
        'index.html',
        form=form,
        nombre=session.get('nombre')
    )

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)














#Comprobación 3: explica por qué Flask-WTF necesita una SECRET_KEY.
#Flask-WTF necesita una SECRET_KEY para proteger los formularios 
# contra ataques de falsificación de solicitudes entre sitios (CSRF). 
# Esta clave se utiliza para generar y validar tokens CSRF que aseguran que 
# los formularios sean enviados por el usuario autenticado y no por un atacante.

#La instrucción que crea el formulario.
#form = RegistroForm()
#La instrucción que valida los datos.
#form.validate_on_submit()
#La instrucción que guarda el nombre en la sesión.
#session['nombre'] = form.nombre.data
#La instrucción que crea el mensaje de confirmación.
#flash('Registro realizado correctamente.')
#La instrucción que realiza la redirección.
#return redirect(url_for('index'))
#La instrucción que envía los datos a la plantilla.
#return render_template('index.html', form=form, nombre=session.get('nombre'))

#Comprobación 4: explica con tus propias palabras cómo este código aplica el 
# patrón Post/Redirect/Get y evita el envío duplicado del formulario.
#El patrón Post/Redirect/Get se aplica cuando el formulario es enviado (POST) y 
# luego se redirige a la misma página (REDIRECT) para mostrar los resultados (GET).
#  Esto evita que al refrescar la página se vuelva a enviar el formulario, 
# lo cual podría causar envíos duplicados.



