# Sistema de Reservas de Hotel

Sistema simple de gestión de reservas de hotel con Flask y MySQL.

## Características

- ✅ Ver habitaciones disponibles
- ✅ Crear reservas con validación de disponibilidad
- ✅ Gestionar habitaciones (admin)
- ✅ Verificar fechas y evitar sobreventas
- ✅ Cancelar reservas
- ✅ Panel de administración

## Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar MySQL:**
   - Abre `crear_db.py` y actualiza la contraseña de MySQL
   - Ejecuta: `python crear_db.py`

3. **Configurar variables de entorno:**
   - Abre `.env` y actualiza `DATABASE_URL` con tu contraseña de MySQL

4. **Ejecutar la aplicación:**
```bash
python app.py
```

5. **Abrir en el navegador:**
   - http://localhost:5000

## Estructura

```
hotel_reservas/
├── app.py                  # Aplicación principal
├── crear_db.py            # Script para crear base de datos
├── requirements.txt       # Dependencias
├── .env                   # Variables de entorno
├── static/
│   └── style.css         # Estilos minimalistas
└── templates/
    ├── base.html         # Plantilla base
    ├── index.html        # Lista de habitaciones
    ├── ver_habitacion.html
    ├── crear_reserva.html
    ├── ver_reserva.html
    ├── mis_reservas.html
    ├── admin.html        # Panel de administración
    ├── nueva_habitacion.html
    └── editar_habitacion.html
```

## Uso

1. **Ver habitaciones:** Página principal muestra todas las habitaciones
2. **Crear reserva:** Selecciona fechas y número de huéspedes
3. **Ver reserva:** Confirmación con todos los detalles
4. **Mis reservas:** Ver historial y cancelar si es necesario
5. **Admin:** Gestionar habitaciones (crear/editar)

## Tecnologías

- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- PyMySQL 1.1.1
- MySQL
- CSS puro (diseño minimalista)
