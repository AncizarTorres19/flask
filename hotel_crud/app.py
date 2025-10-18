from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from functools import wraps

app = Flask(_name_)
app.secret = 'your_secret_key' 

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel_reservas"
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    entrada = request.args.get('entrada')
    salida = request.args.get('salida')
    huespedes = int(request.args.get('huespedes'))

    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM habitaciones
        WHERE capacidad >= %s AND disponible = TRUE
    """, (huespedes,))

    habitaciones = cursor.fetchall()
    conn.close()

    return render_template('disponibles.html', habitaciones=habitaciones, entrada=entrada, salida=salida)

@app.route('/reservar/<int:habitacion_id>')
def mostrar_formulario_cliente(habitacion_id):
    entrada = request.args.get('entrada')
    salida = request.args.get('salida')
    huespedes = int(request.args.get('huespedes'))

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habitaciones WHERE id = %s", (habitacion_id,))
    resultado = cursor.fetchone()

    if resultado is None:
        return "Habitación no encontrada", 404
        
    habitacion = {
        'id': resultado[0],
        "nombre": resultado[1],
        "cpacidad": resultado[2],
       }
    
    conn.close()

    return render_template("reservar.html", habitacion=habitacion, entrada=entrada, salida=salida, huespedes=huespedes)

@app.route('/confirmar_reserva', methods=['POST'])
def confirmar_reserva():
    habitacion_id = int(request.form['habitacion_id'])
    entrada = request.form['entrada']
    salida = request.form['salida']
    huespedes = int(request.form['huespedes'])
    nombre = request.form['nombre']
    cedula = request.form['cédula']
    telefono = request.form['telefono']

    conn = conectar_bd()
    cursor = conn.cursor()

    # Insertar cliente
    cursor.execute("""
        INSERT INTO clientes (nombre, cedula, telefono)
        VALUES (%s, %s, %s)
    """, (nombre, cedula, telefono))
    cliente_id = cursor.lastrowid

    # Insertar reserva
    cursor.execute("""
        INSERT INTO reservas (habitacion_id, entrada, salida, huespedes, cliente_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (habitacion_id, entrada, salida, huespedes, cliente_id))
    
    # Marcar habitación como no disponible
    cursor.execute("""
        UPDATE habitaciones SET disponible = FALSE WHERE id = %s
    """, (habitacion_id,))

    conn.commit()
    conn.close()

    flash('Reserva confirmada con éxito.', 'success')
    return redirect(url_for('index'))