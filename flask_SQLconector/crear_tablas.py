import mysql.connector

# Conexión a MySQL
try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hotel_reservas",
        auth_plugin='mysql_native_password'
    )
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    print("\n💡 Intentando sin especificar auth_plugin...")
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            database="hotel_reservas"
        )
    except Exception as e2:
        print(f"❌ Error: {e2}")
        print("\n📝 Verifica:")
        print("   1. MySQL está corriendo")
        print("   2. La base de datos 'hotel_reservas' existe")
        print("   3. El usuario 'root' no requiere contraseña")
        exit(1)

cursor = conexion.cursor()

# Crear tabla clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `cedula` int(10) NOT NULL,
  `telefono` int(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
""")
print("✅ Tabla 'clientes' creada")

# Crear tabla habitaciones
cursor.execute("""
CREATE TABLE IF NOT EXISTS `habitaciones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `capacidad` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `disponible` tinyint(1) DEFAULT 1,
  `imagen_url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
""")
print("✅ Tabla 'habitaciones' creada")

# Crear tabla reservas
cursor.execute("""
CREATE TABLE IF NOT EXISTS `reservas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cliente_id` int(11) NOT NULL,
  `habitacion_id` int(11) NOT NULL,
  `fecha_entrada` date NOT NULL,
  `fecha_salida` date NOT NULL,
  `fecha_reserva` timestamp NOT NULL DEFAULT current_timestamp(),
  `numero_huespedes` int(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cliente_id` (`cliente_id`),
  KEY `habitacion_id` (`habitacion_id`),
  CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`habitacion_id`) REFERENCES `habitaciones` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
""")
print("✅ Tabla 'reservas' creada")

# Crear tabla usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `usuario` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
""")
print("✅ Tabla 'usuarios' creada")

# Insertar datos de ejemplo en habitaciones
cursor.execute("""
INSERT INTO `habitaciones` (`nombre`, `descripcion`, `capacidad`, `precio`, `disponible`) VALUES
('Suite Familiar', 'Habitación amplia con 2 camas dobles', 4, 150.00, 1),
('Habitación Doble', 'Ideal para parejas, con cama doble', 2, 90.00, 1),
('Habitación Individual', 'Para una sola persona, cama sencilla', 1, 60.00, 1);
""")
print("✅ Datos de ejemplo insertados en 'habitaciones'")

# Insertar usuario admin
cursor.execute("""
INSERT INTO `usuarios` (`nombre`, `usuario`, `password`) VALUES
('Administrador Principal', 'admin', 'admin123');
""")
print("✅ Usuario admin creado")

conexion.commit()
cursor.close()
conexion.close()

print("\n🎉 Base de datos configurada exitosamente!")
print("\n📝 Resumen:")
print("   - 4 tablas creadas (clientes, habitaciones, reservas, usuarios)")
print("   - 3 habitaciones de ejemplo agregadas")
print("   - 1 usuario admin creado (usuario: admin, password: admin123)")
