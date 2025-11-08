from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Corregido: era app.secret 

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        port=3307,  # Puerto de Docker
        user="root",
        password="root123",  # Nueva contraseña de Docker
        database="hotel_reservas",
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci',
        use_unicode=True
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor, inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('rol') != 'admin':
            flash('Acceso restringido: debes iniciar sesión como administrador.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@admin_required
def admin_dashboard():
    # Consultas simples para mostrar estadísticas en el dashboard
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM habitaciones")
        total_habitaciones = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE disponible = TRUE")
        habitaciones_disponibles = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM reservas")
        total_reservas = cursor.fetchone()[0] or 0

    except Exception as e:
        # En caso de error con la base de datos, usar ceros y mostrar log en la consola
        print('Error consultando estadísticas admin:', e)
        total_habitaciones = 0
        habitaciones_disponibles = 0
        total_reservas = 0
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return render_template('admin.html',
                           total_habitaciones=total_habitaciones,
                           habitaciones_disponibles=habitaciones_disponibles,
                           total_reservas=total_reservas)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuarios WHERE usuario = %s', (usuario,))
        usuario_db = cursor.fetchone()
        conn.close()

        if usuario_db and usuario_db.get('password') == password:
            # Iniciar sesión
            session['user_id'] = usuario_db.get('id')
            session['usuario'] = usuario_db.get('usuario')
            # Usar rol desde la base de datos si está presente
            session['rol'] = usuario_db.get('rol') if usuario_db.get('rol') else 'user'
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Credenciales inválidas.', 'danger')

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('index'))

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
        "capacidad": resultado[2],  # Corregido: era cpacidad
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

    cursor.execute("""
        INSERT INTO clientes (nombre, cedula, telefono)
        VALUES (%s, %s, %s)
    """, (nombre, cedula, telefono))
    cliente_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO reservas (cliente_id, habitacion_id, fecha_entrada, fecha_salida, numero_huespedes)
        VALUES (%s, %s, %s, %s, %s)
    """, (cliente_id, habitacion_id, entrada, salida, huespedes))

    cursor.execute("""
        UPDATE habitaciones SET disponible = FALSE WHERE id = %s
    """, (habitacion_id,))
    conn.commit()
    conn.close()
    
    return render_template('confirmacion.html', entrada=entrada, salida=salida)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
