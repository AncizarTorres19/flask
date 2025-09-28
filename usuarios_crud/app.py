from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'

# Configuración de base de datos - MySQL con PyMySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/usuarios_db'
# Para PostgreSQL: 'postgresql://username:password@localhost/usuarios_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# Rutas CRUD

@app.route('/')
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']

        # Verificar si el email ya existe
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El email ya está registrado', 'error')
            return render_template('crear.html')

        nuevo_usuario = Usuario(nombre=nombre, email=email, telefono=telefono)

        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear usuario', 'error')
            return render_template('crear.html')

    return render_template('crear.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        email_nuevo = request.form['email']
        usuario.telefono = request.form['telefono']

        # Verificar si el email ya existe (excepto el usuario actual)
        usuario_existente = Usuario.query.filter(Usuario.email == email_nuevo, Usuario.id != id).first()
        if usuario_existente:
            flash('El email ya está registrado por otro usuario', 'error')
            return render_template('editar.html', usuario=usuario)

        usuario.email = email_nuevo

        try:
            db.session.commit()
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar usuario', 'error')

    return render_template('editar.html', usuario=usuario)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)

    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar usuario', 'error')

    return redirect(url_for('index'))

@app.route('/ver/<int:id>')
def ver(id):
    usuario = Usuario.query.get_or_404(id)
    return render_template('ver.html', usuario=usuario)

# Crear tablas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)