"""
Script para actualizar los precios de las habitaciones a valores realistas en COP
"""
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        password="root123",
        database="hotel_reservas",
        charset='utf8mb4',
        collation='utf8mb4_unicode_ci',
        use_unicode=True
    )

def actualizar_precios():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        
        # Actualizar precios de habitaciones existentes
        actualizaciones = [
            ("UPDATE habitaciones SET precio = 120000 WHERE nombre LIKE '%Individual%'", "Habitaciones Individuales"),
            ("UPDATE habitaciones SET precio = 180000 WHERE nombre LIKE '%Doble%' AND nombre NOT LIKE '%Ejecutiva%'", "Habitaciones Dobles"),
            ("UPDATE habitaciones SET precio = 250000 WHERE nombre LIKE '%Ejecutiva%'", "Habitaciones Ejecutivas"),
            ("UPDATE habitaciones SET precio = 350000 WHERE nombre LIKE '%Familiar%'", "Habitaciones Familiares"),
            ("UPDATE habitaciones SET precio = 580000 WHERE nombre LIKE '%Presidencial%'", "Suites Presidenciales"),
        ]
        
        total_actualizados = 0
        for query, tipo in actualizaciones:
            cursor.execute(query)
            rows = cursor.rowcount
            if rows > 0:
                print(f"✓ Actualizados {rows} registro(s) de {tipo}")
                total_actualizados += rows
        
        conn.commit()
        print(f"\n✅ Total de habitaciones actualizadas: {total_actualizados}")
        
        # Mostrar precios actuales
        cursor.execute("SELECT nombre, precio FROM habitaciones ORDER BY precio DESC")
        habitaciones = cursor.fetchall()
        
        print("\n📋 Precios actuales de habitaciones:")
        print("-" * 60)
        for hab in habitaciones:
            print(f"  {hab[0]:<40} ${hab[1]:>15,.0f} COP")
        print("-" * 60)
        
        conn.close()
        print("\n✅ Actualización completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error al actualizar precios: {e}")

if __name__ == "__main__":
    print("🔄 Actualizando precios de habitaciones a valores en COP...")
    print("=" * 60)
    actualizar_precios()
