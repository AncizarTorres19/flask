from flask import Blueprint, render_template, request, redirect, url_for, flash

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/profile/<username>')
def profile(username):
    # Datos de ejemplo
    user = {'username': username, 'email': f'{username}@example.com'}
    return render_template('users/profile.html', user=user)


@users_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        # En una app real aquí validarías y guardarías en la base de datos
        flash('Configuración actualizada correctamente')
        return redirect(url_for('users.settings'))

    # Datos ficticios para precargar el formulario
    current = {'email': 'usuario@example.com'}
    return render_template('users/settings.html', current=current)
