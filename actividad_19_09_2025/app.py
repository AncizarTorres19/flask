from flask import Flask
from blueprints import main_bp


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'actividad-19-09-2025-secret'

    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
