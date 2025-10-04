# CRUD de Usuarios con Flask y PostgreSQL

Esta aplicación Flask implementa un sistema CRUD completo para gestión de usuarios con base de datos PostgreSQL.

## Características

- ✅ **Crear** usuarios nuevos
- ✅ **Listar** todos los usuarios
- ✅ **Ver** detalles de un usuario específico
- ✅ **Editar** información de usuarios existentes
- ✅ **Eliminar** usuarios
- ✅ Validación de email único
- ✅ Interfaz web responsive con Bootstrap
- ✅ Mensajes flash para feedback del usuario

## Requisitos

- Python 3.7+
- PostgreSQL
- pip

## Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd UsuariosCRUD
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar PostgreSQL**
   - Crear una base de datos llamada `usuarios_db`
   - Actualizar las credenciales en `app.py` línea 9:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tu_usuario:tu_password@localhost/usuarios_db'
     ```

5. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

6. **Acceder a la aplicación**
   - Abrir navegador en: http://localhost:5000

## Estructura del Proyecto

```
UsuariosCRUD/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   ├── index.html        # Lista de usuarios
│   ├── crear.html        # Formulario crear usuario
│   ├── editar.html       # Formulario editar usuario
│   └── ver.html          # Ver detalles de usuario
└── README.md             # Este archivo
```

## Modelo de Datos

### Usuario
- **id**: Identificador único (Primary Key)
- **nombre**: Nombre del usuario (String, requerido)
- **email**: Email único (String, requerido)
- **telefono**: Número telefónico (String, opcional)
- **fecha_creacion**: Timestamp de creación automático

## Rutas de la API

- `GET /` - Lista todos los usuarios
- `GET /crear` - Formulario para crear usuario
- `POST /crear` - Procesar creación de usuario
- `GET /ver/<id>` - Ver detalles de usuario
- `GET /editar/<id>` - Formulario para editar usuario
- `POST /editar/<id>` - Procesar edición de usuario
- `POST /eliminar/<id>` - Eliminar usuario

## Configuración de PostgreSQL

1. **Instalar PostgreSQL** en tu sistema
2. **Crear base de datos:**
   ```sql
   CREATE DATABASE usuarios_db;
   ```
3. **Crear usuario (opcional):**
   ```sql
   CREATE USER tu_usuario WITH ENCRYPTED PASSWORD 'tu_password';
   GRANT ALL PRIVILEGES ON DATABASE usuarios_db TO tu_usuario;
   ```

## Notas Importantes

- Las tablas se crean automáticamente al ejecutar la aplicación
- El email debe ser único en el sistema
- La aplicación incluye validación de formularios
- Se utiliza Bootstrap 5 para el diseño responsive
- Los mensajes flash informan sobre éxito/errores de operaciones