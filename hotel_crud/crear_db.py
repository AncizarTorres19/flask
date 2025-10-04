"""
Script para crear la base de datos usuarios_db en MySQL
"""
import pymysql

# Configuración de conexión (sin especificar base de datos)
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '1234',  # Cambia esto por tu contraseña de MySQL
    'charset': 'utf8mb4'
}

try:
    # Conectar a MySQL
    connection = pymysql.connect(**config)
    cursor = connection.cursor()
    
    # Crear la base de datos si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS usuarios_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✅ Base de datos 'usuarios_db' creada correctamente")
    
    # Mostrar bases de datos existentes
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    print("\n📋 Bases de datos disponibles:")
    for db in databases:
        print(f"  - {db[0]}")
    
    cursor.close()
    connection.close()
    
except Exception as e:
    print(f"❌ Error: {e}")