"""Script mínimo para crear la base de datos MySQL si no existe (usa pymysql).
Requerimientos: python-dotenv, pymysql
Uso: .venv\Scripts\python create_db.py
"""
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import pymysql

load_dotenv()

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print('No se encontró DATABASE_URL en .env')
    raise SystemExit(1)

# Parsear la URL
parsed = urlparse(db_url)
# expected scheme: mysql+pymysql
path = parsed.path.lstrip('/')
if not path:
    print('No se especificó nombre de base de datos en la URL. Edita .env y agrega /mi_proyecto al final de DATABASE_URL')
    raise SystemExit(1)

db_name = path
user = parsed.username or 'root'
password = parsed.password or ''
host = parsed.hostname or 'localhost'
port = parsed.port or 3306

print(f'Intentando conectar a MySQL en {host}:{port} como {user} para crear la BD "{db_name}"')

conn = pymysql.connect(host=host, user=user, password=password, port=port)
conn.autocommit(True)
try:
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print('Base de datos creada o ya existente.')
finally:
    conn.close()
