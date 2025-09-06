from flask import Flask
from blueprints import main_bp, contact_bp, auth_bp

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    # Clave de ejemplo para sesiones/flash. En producción use una variable de entorno segura.
    app.config['SECRET_KEY'] = 'cambiar-esta-clave-por-una-segura'
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
