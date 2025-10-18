"""Script para crear la base de datos MySQL si no existe."""
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import pymysql

load_dotenv()

db_url = os.getenv('DATABASE_URL')
if not db_url:
    print('No se encontró DATABASE_URL en .env')
    raise SystemExit(1)

parsed = urlparse(db_url)
path = parsed.path.lstrip('/')
if not path:
    print('No se especificó nombre de base de datos en la URL')
    raise SystemExit(1)

db_name = path
user = parsed.username or 'root'
password = parsed.password or ''
host = parsed.hostname or 'localhost'
port = parsed.port or 3306

print(f'Conectando a MySQL en {host}:{port} como {user}')
print(f'Creando base de datos: {db_name}')

conn = pymysql.connect(host=host, user=user, password=password, port=port)
conn.autocommit(True)

try:
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f'✅ Base de datos "{db_name}" creada o ya existente')
finally:
    conn.close()
