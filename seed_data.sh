#!/bin/bash

echo "🌱 Starting seed data insertion..."
echo "=================================================="


# Wait for the application to be ready and tables to be created
echo "⏳ Esperando que las tablas se creen..."
echo "⏳ Waiting for tables to be created..."
sleep 5

# DB SQLite
# DB_FILE="/app/map.db"
# DB_FILE=${DB_FILE:-"./map.db"}
DB_FILE="${DB_FILE:-./map.db}"


echo "🏷️ Inserting categories..."

# Inserta categoríes
sqlite3 $DB_FILE << 'EOF'
INSERT OR IGNORE INTO categories (name) VALUES
('Restaurante'),
('Parque'),
('Museo'),
('Hospital'),
('Universidad'),
('Centro Comercial'),
('Biblioteca'),
('Teatro'),
('Gimnasio'),
('Café');
EOF

echo " ✅ Categories inserted"

echo "📍 Inserting Locations..."

# Insert locations
sqlite3 $DB_FILE << 'EOF'
INSERT OR IGNORE INTO locations (name, latitude, longitude, rate, description, created_at, updated_at) VALUES
('Parque Explora', 6.2518400, -75.5635900, 4.5, 'Museo interactivo de ciencias con planetario y acuario', datetime('now'), datetime('now')),
('Universidad de Antioquia', 6.2669700, -75.5664300, 4.2, 'Principal universidad pública de Antioquia', datetime('now'), datetime('now')),
('Centro Comercial Santa Fe', 6.2308900, -75.5906100, 4.0, 'Gran centro comercial con múltiples tiendas y restaurantes', datetime('now'), datetime('now')),
('Parque Arví', 6.2794400, -75.4769400, 4.7, 'Parque ecológico y arqueológico en las montañas', datetime('now'), datetime('now')),
('Teatro Metropolitano', 6.2516200, -75.5635900, 4.3, 'Principal teatro de la ciudad con espectáculos culturales', datetime('now'), datetime('now')),
('Hospital Pablo Tobón Uribe', 6.2074500, -75.5755600, 4.1, 'Hospital de alta complejidad reconocido internacionalmente', datetime('now'), datetime('now')),
('Biblioteca EPM', 6.2442800, -75.5815000, 4.6, 'Moderna biblioteca pública con amplios recursos digitales', datetime('now'), datetime('now')),
('Café Pergamino', 6.2077200, -75.5636100, 4.4, 'Café especializado con granos colombianos de alta calidad', datetime('now'), datetime('now')),
('SmartFit Poblado', 6.2093800, -75.5681200, 3.9, 'Gimnasio moderno con equipos de última tecnología', datetime('now'), datetime('now')),
('Museo de Antioquia', 6.2529600, -75.5664400, 4.2, 'Museo con importante colección de arte y obras de Botero', datetime('now'), datetime('now'));
EOF

echo "   ✅ Locations inserted"

echo "🔗 Creating relationship location-category..."

# Inserting relationships into location_category_reviewed
sqlite3 $DB_FILE << 'EOF'
-- Parque Explora -> Museo, Parque
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Parque Explora' AND c.name IN ('Museo', 'Parque');

-- Universidad de Antioquia -> Universidad
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Universidad de Antioquia' AND c.name = 'Universidad';

-- Centro Comercial Santa Fe -> Centro Comercial, Restaurante
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Centro Comercial Santa Fe' AND c.name IN ('Centro Comercial', 'Restaurante');

-- Parque Arví -> Parque
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Parque Arví' AND c.name = 'Parque';

-- Teatro Metropolitano -> Teatro
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Teatro Metropolitano' AND c.name = 'Teatro';

-- Hospital Pablo Tobón Uribe -> Hospital
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Hospital Pablo Tobón Uribe' AND c.name = 'Hospital';

-- Biblioteca EPM -> Biblioteca
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Biblioteca EPM' AND c.name = 'Biblioteca';

-- Café Pergamino -> Café, Restaurante
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Café Pergamino' AND c.name IN ('Café', 'Restaurante');

-- SmartFit Poblado -> Gimnasio
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'SmartFit Poblado' AND c.name = 'Gimnasio';

-- Museo de Antioquia -> Museo
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Museo de Antioquia' AND c.name = 'Museo';
EOF

echo "   ✅ Relationships inserted"

echo "=================================================="
echo "🎉 ¡Data seed inserted successfully!"
echo "   📊 Sumary:"
echo "      • 10 Categories"
echo "      • 10 Locatrions"
echo "      • Relationships between locations and categories"
echo "=================================================="
