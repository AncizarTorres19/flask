# Blueprint para autenticación con url_prefix
from flask import Blueprint, render_template, request, redirect, url_for, flash

# Creamos un Blueprint llamado "auth" con prefijo "/auth"
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el formulario de login. En esta demo validamos contra credenciales ficticias."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Validación simple de ejemplo
        if email.lower() == 'admin@example.com' and password == 'password':
            flash('Bienvenido, has iniciado sesión correctamente')
            return redirect(url_for('main.index'))
        else:
            flash('Credenciales incorrectas — usa admin@example.com / password para la demo')
            return redirect(url_for('auth.login'))

    return render_template("auth/login.html")
