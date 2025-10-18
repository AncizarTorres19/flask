from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hotel-reservas-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:1234@localhost:3306/hotel_reservas')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== MODELOS ==========

class Habitacion(db.Model):
    __tablename__ = 'habitaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # Simple, Doble, Suite
    capacidad = db.Column(db.Integer, nullable=False)
    precio_noche = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    disponible = db.Column(db.Boolean, default=True)
    
    # Relación con reservas
    reservas = db.relationship('Reserva', backref='habitacion', lazy=True)
    
    def __repr__(self):
        return f'<Habitacion {self.numero} - {self.tipo}>'

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitaciones.id'), nullable=False)
    nombre_huesped = db.Column(db.String(100), nullable=False)
    email_huesped = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20))
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    num_huespedes = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='confirmada')  # confirmada, cancelada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reserva #{self.id} - Habitación {self.habitacion_id}>'

# ========== FUNCIONES AUXILIARES ==========

def verificar_disponibilidad(habitacion_id, check_in, check_out, reserva_id=None):
    """Verifica si una habitación está disponible en las fechas dadas."""
    query = Reserva.query.filter(
        Reserva.habitacion_id == habitacion_id,
        Reserva.estado == 'confirmada',
        Reserva.check_out > check_in,
        Reserva.check_in < check_out
    )
    
    # Si estamos editando, excluir la reserva actual
    if reserva_id:
        query = query.filter(Reserva.id != reserva_id)
    
    conflictos = query.all()
    return len(conflictos) == 0

def calcular_total(precio_noche, check_in, check_out):
    """Calcula el total de la reserva."""
    noches = (check_out - check_in).days
    return precio_noche * noches

# ========== RUTAS ==========

@app.route('/')
def index():
    """Página principal - muestra habitaciones disponibles."""
    habitaciones = Habitacion.query.filter_by(disponible=True).all()
    return render_template('index.html', habitaciones=habitaciones)

@app.route('/habitacion/<int:id>')
def ver_habitacion(id):
    """Ver detalles de una habitación."""
    habitacion = Habitacion.query.get_or_404(id)
    return render_template('ver_habitacion.html', habitacion=habitacion)

@app.route('/reservar/<int:habitacion_id>', methods=['GET', 'POST'])
def crear_reserva(habitacion_id):
    """Crear una nueva reserva."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form.get('telefono', '')
        check_in_str = request.form['check_in']
        check_out_str = request.form['check_out']
        num_huespedes = int(request.form['num_huespedes'])
        
        # Convertir fechas
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de fecha inválido', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
        
        # Validaciones
        if check_in >= check_out:
            flash('La fecha de salida debe ser posterior a la de entrada', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
        
        if check_in < datetime.now().date():
            flash('No se pueden hacer reservas en fechas pasadas', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
        
        if num_huespedes > habitacion.capacidad:
            flash(f'La habitación solo tiene capacidad para {habitacion.capacidad} personas', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
        
        # Verificar disponibilidad
        if not verificar_disponibilidad(habitacion_id, check_in, check_out):
            flash('La habitación no está disponible en esas fechas', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
        
        # Calcular total
        total = calcular_total(habitacion.precio_noche, check_in, check_out)
        
        # Crear reserva
        nueva_reserva = Reserva(
            habitacion_id=habitacion_id,
            nombre_huesped=nombre,
            email_huesped=email,
            telefono=telefono,
            check_in=check_in,
            check_out=check_out,
            num_huespedes=num_huespedes,
            total=total
        )
        
        try:
            db.session.add(nueva_reserva)
            db.session.commit()
            flash(f'¡Reserva confirmada! Total: ${total:.2f}', 'success')
            return redirect(url_for('ver_reserva', id=nueva_reserva.id))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la reserva', 'error')
            return redirect(url_for('crear_reserva', habitacion_id=habitacion_id))
    
    # GET - mostrar formulario
    return render_template('crear_reserva.html', habitacion=habitacion)

@app.route('/reserva/<int:id>')
def ver_reserva(id):
    """Ver detalles de una reserva."""
    reserva = Reserva.query.get_or_404(id)
    noches = (reserva.check_out - reserva.check_in).days
    return render_template('ver_reserva.html', reserva=reserva, noches=noches)

@app.route('/mis-reservas')
def mis_reservas():
    """Listar todas las reservas."""
    reservas = Reserva.query.order_by(Reserva.fecha_creacion.desc()).all()
    return render_template('mis_reservas.html', reservas=reservas)

@app.route('/cancelar-reserva/<int:id>')
def cancelar_reserva(id):
    """Cancelar una reserva."""
    reserva = Reserva.query.get_or_404(id)
    
    if reserva.estado == 'cancelada':
        flash('Esta reserva ya está cancelada', 'error')
        return redirect(url_for('mis_reservas'))
    
    reserva.estado = 'cancelada'
    
    try:
        db.session.commit()
        flash('Reserva cancelada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al cancelar la reserva', 'error')
    
    return redirect(url_for('mis_reservas'))

# ========== ADMIN (Gestión de habitaciones) ==========

@app.route('/admin')
def admin():
    """Panel de administración."""
    habitaciones = Habitacion.query.all()
    reservas = Reserva.query.order_by(Reserva.fecha_creacion.desc()).limit(10).all()
    return render_template('admin.html', habitaciones=habitaciones, reservas=reservas)

@app.route('/admin/habitacion/nueva', methods=['GET', 'POST'])
def nueva_habitacion():
    """Crear nueva habitación."""
    if request.method == 'POST':
        numero = request.form['numero']
        tipo = request.form['tipo']
        capacidad = int(request.form['capacidad'])
        precio = float(request.form['precio'])
        descripcion = request.form.get('descripcion', '')
        
        # Verificar que el número no exista
        if Habitacion.query.filter_by(numero=numero).first():
            flash('Ya existe una habitación con ese número', 'error')
            return redirect(url_for('nueva_habitacion'))
        
        nueva = Habitacion(
            numero=numero,
            tipo=tipo,
            capacidad=capacidad,
            precio_noche=precio,
            descripcion=descripcion
        )
        
        try:
            db.session.add(nueva)
            db.session.commit()
            flash('Habitación creada exitosamente', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la habitación', 'error')
    
    return render_template('nueva_habitacion.html')

@app.route('/admin/habitacion/editar/<int:id>', methods=['GET', 'POST'])
def editar_habitacion(id):
    """Editar habitación existente."""
    habitacion = Habitacion.query.get_or_404(id)
    
    if request.method == 'POST':
        habitacion.numero = request.form['numero']
        habitacion.tipo = request.form['tipo']
        habitacion.capacidad = int(request.form['capacidad'])
        habitacion.precio_noche = float(request.form['precio'])
        habitacion.descripcion = request.form.get('descripcion', '')
        habitacion.disponible = 'disponible' in request.form
        
        try:
            db.session.commit()
            flash('Habitación actualizada exitosamente', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            flash('Error al actualizar la habitación', 'error')
    
    return render_template('editar_habitacion.html', habitacion=habitacion)

# ========== INICIALIZACIÓN ==========

with app.app_context():
    db.create_all()
    
    # Crear habitaciones de ejemplo si no existen
    if Habitacion.query.count() == 0:
        habitaciones_ejemplo = [
            Habitacion(numero='101', tipo='Simple', capacidad=1, precio_noche=50, descripcion='Habitación simple con cama individual'),
            Habitacion(numero='102', tipo='Simple', capacidad=1, precio_noche=50, descripcion='Habitación simple con cama individual'),
            Habitacion(numero='201', tipo='Doble', capacidad=2, precio_noche=80, descripcion='Habitación doble con cama matrimonial'),
            Habitacion(numero='202', tipo='Doble', capacidad=2, precio_noche=80, descripcion='Habitación doble con cama matrimonial'),
            Habitacion(numero='301', tipo='Suite', capacidad=4, precio_noche=150, descripcion='Suite de lujo con sala y jacuzzi'),
        ]
        db.session.add_all(habitaciones_ejemplo)
        db.session.commit()
        print('✅ Habitaciones de ejemplo creadas')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
