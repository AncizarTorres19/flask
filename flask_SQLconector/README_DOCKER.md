# 🐳 Instrucciones para usar MySQL con Docker

## Paso 1: Instalar Docker Desktop (si no lo tienes)
Descarga de: https://www.docker.com/products/docker-desktop/

## Paso 2: Levantar el contenedor MySQL

Abre PowerShell en esta carpeta y ejecuta:

```powershell
docker-compose up -d
```

Esto creará:
- ✅ Un contenedor MySQL en el puerto 3307
- ✅ Base de datos `hotel_reservas` 
- ✅ Todas las tablas automáticamente
- ✅ Datos de ejemplo (3 habitaciones + 1 usuario admin)
- ✅ Usuario: root / Contraseña: root123

## Paso 3: Verificar que funciona

```powershell
docker ps
```

Deberías ver el contenedor `hotel_mysql` corriendo.

## Paso 4: Ejecutar tu aplicación Flask

```powershell
python app.py
```

## Comandos útiles:

```powershell
# Ver logs del contenedor
docker logs hotel_mysql

# Detener el contenedor
docker-compose down

# Reiniciar el contenedor
docker-compose restart

# Conectarte al MySQL desde la terminal
docker exec -it hotel_mysql mysql -uroot -proot123 hotel_reservas

# Ver las tablas
docker exec -it hotel_mysql mysql -uroot -proot123 -e "USE hotel_reservas; SHOW TABLES;"
```

## 📊 Credenciales configuradas:

- **Host:** localhost
- **Puerto:** 3307 (para no conflictuar con tu MySQL actual en 3306)
- **Usuario:** root
- **Contraseña:** root123
- **Base de datos:** hotel_reservas

## ⚡ Ventajas de usar Docker:

- No necesitas la contraseña de tu MySQL actual
- Base de datos aislada solo para este proyecto
- Fácil de resetear si algo sale mal: `docker-compose down -v && docker-compose up -d`
- No interfiere con tu XAMPP/MySQL existente
