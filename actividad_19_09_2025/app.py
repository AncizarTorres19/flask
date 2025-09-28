from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Cargar variables de entorno (.env)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración básica
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mi-clave-secreta-desarrollo')
# Ejemplos para DATABASE_URL:
# - SQLite (por defecto): sqlite:///mi_proyecto.db
# - MySQL: mysql+pymysql://usuario:password@localhost:3306/mi_db
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///mi_proyecto.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar DB
db = SQLAlchemy(app)

# -----------------------------
# Modelos
# -----------------------------
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email
        }

# -----------------------------
# Rutas de vistas
# -----------------------------
@app.route('/')
def index():
    # Asume que tienes templates/index.html
    return render_template('index.html')

# -----------------------------
# API
# -----------------------------
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@app.route('/usuario', methods=['POST'])
def crear_usuario():
    data = request.get_json() or {}
    nombre = data.get('nombre')
    email = data.get('email')

    if not nombre or not email:
        return jsonify({'error': 'nombre y email son requeridos'}), 400

    # Opcional: validar duplicado de email con mensaje claro
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'el email ya existe'}), 409

    nuevo_usuario = Usuario(nombre=nombre, email=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.to_dict()), 201

@app.route('/test')
def test():
    return jsonify({
        'mensaje': '¡Servidor Flask funcionando correctamente!',
        'status': 'OK',
        'servidor': 'Flask en Windows'
    })

# -----------------------------
# Crear tablas al iniciar (dev)
# -----------------------------
with app.app_context():
    db.create_all()

# -----------------------------
# Arranque
# -----------------------------
if __name__ == '__main__':
    print('> Servidor Flask iniciando...')
    print('> Disponible en: http://localhost:5000')
    print('> Modo desarrollo activado')
    app.run(host='127.0.0.1', port=5000, debug=True)
