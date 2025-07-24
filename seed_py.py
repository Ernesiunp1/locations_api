#!/usr/bin/env python3
"""
Script para insertar datos semilla en la base de datos SQLite
Compatible con Windows, Linux y macOS
"""

import sqlite3
import time
import os
from datetime import datetime, timedelta


def get_db_path():
    """Obtiene la ruta de la base de datos desde variable de entorno o usa default"""
    return os.getenv('DB_FILE', './map.db')


def print_progress(message, emoji=""):
    """Imprime mensajes de progreso con formato"""
    print(f"{emoji} {message}")


def wait_for_tables(db_path, max_attempts=10):
    """Espera a que las tablas estén creadas antes de insertar datos"""
    print_progress("Esperando a que las tablas sean creadas...", "⏳")

    for attempt in range(max_attempts):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Verificar si las tablas principales existen
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('categories', 'locations', 'location_category_reviewed')
            """)
            tables = cursor.fetchall()
            conn.close()

            if len(tables) >= 3:
                print_progress("Tablas encontradas, continuando...", "✅")
                return True

            print(f"Intento {attempt + 1}/{max_attempts}: Esperando tablas...")
            time.sleep(1)

        except sqlite3.Error as e:
            print(f"Error verificando tablas: {e}")
            time.sleep(1)

    print_progress("Advertencia: No se pudieron verificar todas las tablas", "⚠️")
    return False


def insert_categories(conn):
    """Inserta las categorías en la base de datos"""
    print_progress("Insertando categorías...", "🏷️")

    categories = [
        'Restaurante', 'Parque', 'Museo', 'Hospital', 'Universidad',
        'Centro Comercial', 'Biblioteca', 'Teatro', 'Gimnasio', 'Café'
    ]

    cursor = conn.cursor()

    for category in categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category,))

    conn.commit()
    print_progress("Categorías insertadas", "✅")


def insert_locations(conn):
    """Inserta las ubicaciones en la base de datos"""
    print_progress("Insertando ubicaciones...", "📍")

    locations = [
        ('Parque Explora', 6.2518400, -75.5635900, 4.5, 'Museo interactivo de ciencias con planetario y acuario'),
        ('Universidad de Antioquia', 6.2669700, -75.5664300, 4.2, 'Principal universidad pública de Antioquia'),
        ('Centro Comercial Santa Fe', 6.2308900, -75.5906100, 4.0,
         'Gran centro comercial con múltiples tiendas y restaurantes'),
        ('Parque Arví', 6.2794400, -75.4769400, 4.7, 'Parque ecológico y arqueológico en las montañas'),
        ('Teatro Metropolitano', 6.2516200, -75.5635900, 4.3,
         'Principal teatro de la ciudad con espectáculos culturales'),
        ('Hospital Pablo Tobón Uribe', 6.2074500, -75.5755600, 4.1,
         'Hospital de alta complejidad reconocido internacionalmente'),
        ('Biblioteca EPM', 6.2442800, -75.5815000, 4.6, 'Moderna biblioteca pública con amplios recursos digitales'),
        ('Café Pergamino', 6.2077200, -75.5636100, 4.4, 'Café especializado con granos colombianos de alta calidad'),
        ('SmartFit Poblado', 6.2093800, -75.5681200, 3.9, 'Gimnasio moderno con equipos de última tecnología'),
        ('Museo de Antioquia', 6.2529600, -75.5664400, 4.2, 'Museo con importante colección de arte y obras de Botero'),
        (
        'Jardín Botánico de Medellín', 6.271100, -75.565100, 4.7, 'Espacio verde con jardines temáticos y mariposario'),
        ('Plaza Botero', 6.253800, -75.568400, 4.5, 'Plaza con esculturas del artista Fernando Botero'),
        (
        'Aeropuerto Olaya Herrera', 6.219000, -75.590000, 3.8, 'Aeropuerto regional ubicado en el centro de la ciudad'),
        ('Mercado del Río', 6.244500, -75.574000, 4.6, 'Espacio gastronómico con gran variedad de restaurantes'),
        ('Cerro Nutibara', 6.237900, -75.580500, 4.3, 'Colina con vistas panorámicas y Pueblito Paisa'),
        ('Planetario de Medellín', 6.270350, -75.565200, 4.8, 'Centro astronómico con exhibiciones y proyecciones'),
        ('Estación San Antonio', 6.246800, -75.568100, 3.9, 'Estación principal del metro de Medellín'),
        ('Museo Casa de la Memoria', 6.250000, -75.556800, 4.5, 'Museo sobre la historia del conflicto colombiano'),
        (
        'Parque de los Deseos', 6.270600, -75.566600, 4.4, 'Parque urbano con cine al aire libre y eventos culturales'),
        ('Casa Museo Pedro Nel Gómez', 6.274400, -75.554300, 4.2, 'Museo dedicado al artista y urbanista paisa')
    ]

    cursor = conn.cursor()
    now = datetime.now().isoformat()

    for location in locations:
        cursor.execute("""
            INSERT OR IGNORE INTO locations 
            (name, latitude, longitude, rate, description, created_at, updated_at) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, location + (now, now))

    conn.commit()
    time.sleep(2)
    print_progress("Ubicaciones insertadas", "✅")


def insert_location_category_relationships(conn):
    """Inserta las relaciones entre ubicaciones y categorías"""
    print_progress("Creando relaciones ubicación-categoría...", "🔗")

    cursor = conn.cursor()
    now = datetime.now()

    # Relaciones con diferentes estados de revisión
    relationships = [
        # location_name, categories, reviewed_status, days_ago
        ('Parque Explora', ['Museo', 'Parque'], None, None),
        ('Universidad de Antioquia', ['Universidad'], None, None),
        ('Centro Comercial Santa Fe', ['Centro Comercial', 'Restaurante'], None, None),
        ('Parque Arví', ['Parque'], None, None),
        ('Teatro Metropolitano', ['Teatro'], None, None),
        ('Hospital Pablo Tobón Uribe', ['Hospital'], None, None),
        ('Biblioteca EPM', ['Biblioteca'], None, None),
        ('Café Pergamino', ['Café', 'Restaurante'], None, None),
        ('SmartFit Poblado', ['Gimnasio'], None, None),
        ('Museo de Antioquia', ['Museo'], None, None),
        ('Jardín Botánico de Medellín', ['Parque'], True, 60),  # revisión vieja
        ('Plaza Botero', ['Museo'], None, None),  # nunca revisado
        ('Aeropuerto Olaya Herrera', ['Restaurante'], True, 5),  # revisión reciente
        ('Mercado del Río', ['Restaurante'], None, None),  # nunca revisado
        ('Cerro Nutibara', ['Parque'], True, 90),  # revisión vieja
        ('Planetario de Medellín', ['Museo'], True, 2),  # revisión reciente
        ('Estación San Antonio', ['Gimnasio'], None, None),  # nunca revisado
        ('Museo Casa de la Memoria', ['Museo'], True, 35),  # revisión vieja
        ('Parque de los Deseos', ['Parque'], None, None),  # nunca revisado
        ('Casa Museo Pedro Nel Gómez', ['Museo'], True, 1)  # revisión reciente
    ]

    for location_name, categories, was_reviewed, days_ago in relationships:
        for category_name in categories:
            if was_reviewed is None:
                # Nunca revisado
                cursor.execute("""
                    INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
                    SELECT l.id, c.id FROM locations l, categories c
                    WHERE l.name = ? AND c.name = ?
                """, (location_name, category_name))
            else:
                # Con revisión
                last_reviewed = (now - timedelta(days=days_ago)).isoformat()
                cursor.execute("""
                    INSERT OR IGNORE INTO location_category_reviewed 
                    (location_id, category_id, was_reviewed, last_reviewed)
                    SELECT l.id, c.id, ?, ? FROM locations l, categories c
                    WHERE l.name = ? AND c.name = ?
                """, (was_reviewed, last_reviewed, location_name, category_name))

    conn.commit()
    print_progress("Relaciones insertadas", "✅")


def print_summary():
    """Imprime un resumen de los datos insertados"""
    print("=" * 50)
    print_progress("¡Datos semilla insertados exitosamente!", "🎉")
    print_progress("Resumen:", "📊")
    print("      • 10 Categorías")
    print("      • 20 Ubicaciones")
    print("      • Relaciones entre ubicaciones y categorías")
    print("=" * 50)


def main():
    """Función principal"""
    print_progress("Iniciando inserción de datos semilla...", "🌱")
    print("=" * 50)
    print_progress("ESPERANDO A QUE LAS TABLAS SEAN CREADAS", "###############")

    db_path = get_db_path()

    # Esperar a que las tablas estén creadas
    wait_for_tables(db_path)
    time.sleep(5)  # Espera adicional por seguridad

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)

        # Insertar datos
        insert_categories(conn)
        insert_locations(conn)
        insert_location_category_relationships(conn)

        # Cerrar conexión
        conn.close()

        # Mostrar resumen
        print_summary()

    except sqlite3.Error as e:
        print_progress(f"Error de base de datos: {e}", "❌")
        return 1
    except Exception as e:
        print_progress(f"Error inesperado: {e}", "❌")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())