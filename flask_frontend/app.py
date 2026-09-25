from flask import Flask, render_template, redirect, url_for, flash
from forms import ContactForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '041202'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        flash(f'Mensaje enviado por {form.name.data}!')
        return redirect(url_for('index'))
    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)