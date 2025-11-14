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
@app.route('/admin/dashboard')
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

        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0] or 0

        # Ingresos totales (suma de todas las reservas completadas)
        cursor.execute("SELECT SUM(h.precio) FROM reservas r JOIN habitaciones h ON r.habitacion_id = h.id")
        ingresos_result = cursor.fetchone()[0]
        ingresos_totales = float(ingresos_result) if ingresos_result else 0

    except Exception as e:
        # En caso de error con la base de datos, usar ceros y mostrar log en la consola
        print('Error consultando estadísticas admin:', e)
        total_habitaciones = 0
        habitaciones_disponibles = 0
        total_reservas = 0
        total_clientes = 0
        ingresos_totales = 0
    finally:
        try:
            cursor.close()
            conn.close()
        except Exception:
            pass

    return render_template('admin.html',
                           total_habitaciones=total_habitaciones,
                           habitaciones_disponibles=habitaciones_disponibles,
                           total_reservas=total_reservas,
                           total_clientes=total_clientes,
                           ingresos_totales=ingresos_totales)


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

# ==================== RUTAS ADMINISTRATIVAS ====================

@app.route('/admin/habitaciones')
@admin_required
def admin_habitaciones():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM habitaciones ORDER BY id DESC")
        habitaciones = cursor.fetchall()
        conn.close()
        return render_template('admin_habitaciones.html', habitaciones=habitaciones)
    except Exception as e:
        print('Error al obtener habitaciones:', e)
        flash('Error al cargar habitaciones', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/habitaciones/crear', methods=['GET', 'POST'])
@admin_required
def admin_crear_habitacion():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        capacidad = request.form.get('capacidad')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO habitaciones (nombre, capacidad, precio, descripcion, disponible)
                VALUES (%s, %s, %s, %s, TRUE)
            """, (nombre, capacidad, precio, descripcion))
            conn.commit()
            conn.close()
            flash('Habitación creada exitosamente', 'success')
            return redirect(url_for('admin_habitaciones'))
        except Exception as e:
            print('Error al crear habitación:', e)
            flash('Error al crear habitación', 'danger')
    
    return render_template('admin_crear_habitacion.html')

@app.route('/admin/habitaciones/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_editar_habitacion(id):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        capacidad = request.form.get('capacidad')
        precio = request.form.get('precio')
        descripcion = request.form.get('descripcion')
        disponible = request.form.get('disponible') == 'on'
        
        try:
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE habitaciones 
                SET nombre = %s, capacidad = %s, precio = %s, descripcion = %s, disponible = %s
                WHERE id = %s
            """, (nombre, capacidad, precio, descripcion, disponible, id))
            conn.commit()
            conn.close()
            flash('Habitación actualizada exitosamente', 'success')
            return redirect(url_for('admin_habitaciones'))
        except Exception as e:
            print('Error al editar habitación:', e)
            flash('Error al editar habitación', 'danger')
    
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM habitaciones WHERE id = %s", (id,))
        habitacion = cursor.fetchone()
        conn.close()
        return render_template('admin_editar_habitacion.html', habitacion=habitacion)
    except Exception as e:
        print('Error al cargar habitación:', e)
        flash('Error al cargar habitación', 'danger')
        return redirect(url_for('admin_habitaciones'))

@app.route('/admin/habitaciones/eliminar/<int:id>')
@admin_required
def admin_eliminar_habitacion(id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM habitaciones WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        flash('Habitación eliminada exitosamente', 'success')
    except Exception as e:
        print('Error al eliminar habitación:', e)
        flash('Error al eliminar habitación', 'danger')
    
    return redirect(url_for('admin_habitaciones'))

@app.route('/admin/reservas')
@admin_required
def admin_reservas():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT r.*, c.nombre as cliente_nombre, c.cedula, c.telefono, 
                   h.nombre as habitacion_nombre, h.precio
            FROM reservas r
            JOIN clientes c ON r.cliente_id = c.id
            JOIN habitaciones h ON r.habitacion_id = h.id
            ORDER BY r.fecha_entrada DESC
        """)
        reservas = cursor.fetchall()
        conn.close()
        return render_template('admin_reservas.html', reservas=reservas)
    except Exception as e:
        print('Error al obtener reservas:', e)
        flash('Error al cargar reservas', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/reservas/eliminar/<int:id>')
@admin_required
def admin_eliminar_reserva(id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        
        # Obtener habitacion_id antes de eliminar
        cursor.execute("SELECT habitacion_id FROM reservas WHERE id = %s", (id,))
        reserva = cursor.fetchone()
        
        if reserva:
            # Eliminar la reserva
            cursor.execute("DELETE FROM reservas WHERE id = %s", (id,))
            
            # Marcar habitación como disponible
            cursor.execute("UPDATE habitaciones SET disponible = TRUE WHERE id = %s", (reserva['habitacion_id'],))
            
            conn.commit()
            flash('Reserva eliminada exitosamente', 'success')
        else:
            flash('Reserva no encontrada', 'warning')
        
        conn.close()
    except Exception as e:
        print('Error al eliminar reserva:', e)
        flash('Error al eliminar reserva', 'danger')
    
    return redirect(url_for('admin_reservas'))

@app.route('/admin/clientes')
@admin_required
def admin_clientes():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.*, COUNT(r.id) as total_reservas
            FROM clientes c
            LEFT JOIN reservas r ON c.id = r.cliente_id
            GROUP BY c.id
            ORDER BY c.id DESC
        """)
        clientes = cursor.fetchall()
        conn.close()
        return render_template('admin_clientes.html', clientes=clientes)
    except Exception as e:
        print('Error al obtener clientes:', e)
        flash('Error al cargar clientes', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/clientes/eliminar/<int:id>')
@admin_required
def admin_eliminar_cliente(id):
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si el cliente tiene reservas
        cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE cliente_id = %s", (id,))
        result = cursor.fetchone()
        
        if result['total'] > 0:
            flash(f'No se puede eliminar el cliente porque tiene {result["total"]} reserva(s) asociada(s). Elimina primero las reservas.', 'warning')
        else:
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
            conn.commit()
            flash('Cliente eliminado exitosamente', 'success')
        
        conn.close()
    except Exception as e:
        print('Error al eliminar cliente:', e)
        flash('Error al eliminar cliente', 'danger')
    
    return redirect(url_for('admin_clientes'))

@app.route('/admin/finanzas')
@admin_required
def admin_finanzas():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        
        # Ingresos totales
        cursor.execute("SELECT SUM(h.precio) as total FROM reservas r JOIN habitaciones h ON r.habitacion_id = h.id")
        ingresos = cursor.fetchone()
        
        # Reservas por mes
        cursor.execute("""
            SELECT DATE_FORMAT(fecha_entrada, '%Y-%m') as mes, 
                   COUNT(*) as cantidad, 
                   SUM(h.precio) as ingresos
            FROM reservas r
            JOIN habitaciones h ON r.habitacion_id = h.id
            GROUP BY mes
            ORDER BY mes DESC
            LIMIT 12
        """)
        reservas_mes = cursor.fetchall()
        
        # Habitaciones más rentables
        cursor.execute("""
            SELECT h.nombre, COUNT(r.id) as reservas, SUM(h.precio) as ingresos
            FROM habitaciones h
            LEFT JOIN reservas r ON h.id = r.habitacion_id
            GROUP BY h.id
            ORDER BY ingresos DESC
        """)
        habitaciones_rentables = cursor.fetchall()
        
        conn.close()
        
        return render_template('admin_finanzas.html', 
                             ingresos_totales=ingresos['total'] if ingresos['total'] else 0,
                             reservas_mes=reservas_mes,
                             habitaciones_rentables=habitaciones_rentables)
    except Exception as e:
        print('Error al obtener finanzas:', e)
        flash('Error al cargar finanzas', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/reportes')
@admin_required
def admin_reportes():
    try:
        conn = conectar_bd()
        cursor = conn.cursor(dictionary=True)
        
        # Estadísticas generales
        cursor.execute("SELECT COUNT(*) as total FROM reservas")
        total_reservas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM clientes")
        total_clientes = cursor.fetchone()['total']
        
        cursor.execute("SELECT AVG(h.precio) as promedio FROM reservas r JOIN habitaciones h ON r.habitacion_id = h.id")
        precio_promedio = cursor.fetchone()['promedio']
        
        # Tasa de ocupación
        cursor.execute("SELECT COUNT(*) as total FROM habitaciones")
        total_habitaciones = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as ocupadas FROM habitaciones WHERE disponible = FALSE")
        habitaciones_ocupadas = cursor.fetchone()['ocupadas']
        
        tasa_ocupacion = (habitaciones_ocupadas / total_habitaciones * 100) if total_habitaciones > 0 else 0
        
        conn.close()
        
        return render_template('admin_reportes.html',
                             total_reservas=total_reservas,
                             total_clientes=total_clientes,
                             precio_promedio=precio_promedio if precio_promedio else 0,
                             tasa_ocupacion=round(tasa_ocupacion, 2))
    except Exception as e:
        print('Error al generar reportes:', e)
        flash('Error al generar reportes', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/configuracion', methods=['GET', 'POST'])
@admin_required
def admin_configuracion():
    if request.method == 'POST':
        # Aquí se pueden guardar configuraciones en la base de datos
        flash('Configuración guardada exitosamente', 'success')
        return redirect(url_for('admin_configuracion'))
    
    return render_template('admin_configuracion.html')

# ==================== RUTAS PÚBLICAS ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/promociones')
def promociones():
    return render_template('promociones.html')

@app.route('/hoteles')
def hoteles():
    return render_template('hoteles.html')

@app.route('/todo-incluido')
def todo_incluido():
    return render_template('todo_incluido.html')

@app.route('/eventos')
def eventos():
    return render_template('eventos.html')

@app.route('/sostenibilidad')
def sostenibilidad():
    return render_template('sostenibilidad.html')

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
