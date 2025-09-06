from flask import Flask
from blueprints import users_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'actividad-05-09-2025-secret'

    # Redirigir la raíz a una ruta útil para la actividad
    @app.route('/')
    def root():
        from flask import redirect, url_for
        return redirect(url_for('users.profile', username='usuario'))

    # Registrar blueprints
    app.register_blueprint(users_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
