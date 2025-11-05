from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'


@app.route('/')
def index():
    # Inicializa el contador de intentos si no existe
    if 'intentos' not in session:
        session['intentos'] = 0
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']

    # Si ya superó el límite de intentos
    if session.get('intentos', 0) >= 3:
        error = "Has superado el número máximo de intentos. Inténtalo más tarde."
        return render_template('index.html', error=error)

    # Validar usuario y contraseña
    if usuario == 'pepe' and password == '123':
        session['usuario'] = usuario
        session['intentos'] = 0  # Reiniciar intentos al iniciar correctamente
        return redirect(url_for('dashboard'))
    else:
        session['intentos'] = session.get('intentos', 0) + 1
        intentos_restantes = 3 - session['intentos']

        if intentos_restantes > 0:
            error = f"Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}"
        else:
            error = "Has superado el número máximo de intentos."

        return render_template('index.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return render_template('dashboard.html', usuario=session['usuario'])
    return redirect(url_for('index'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    session['intentos'] = 0
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
