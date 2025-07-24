#!/bin/bash
echo "🌱 Starting seed data insertion..."
echo "=================================================="
echo "############### WAITING FOR TABLES TO BE CREATED ###################"
DB_FILE="${DB_FILE:-./map.db}"
echo "🏷️ Inserting categories..."
sqlite3 "$DB_FILE" << 'EOF'
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
sqlite3 "$DB_FILE" << 'EOF'
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
('Museo de Antioquia', 6.2529600, -75.5664400, 4.2, 'Museo con importante colección de arte y obras de Botero', datetime('now'), datetime('now')),
('Jardín Botánico de Medellín', 6.271100, -75.565100, 4.7, 'Espacio verde con jardines temáticos y mariposario', datetime('now'), datetime('now')),
('Plaza Botero', 6.253800, -75.568400, 4.5, 'Plaza con esculturas del artista Fernando Botero', datetime('now'), datetime('now')),
('Aeropuerto Olaya Herrera', 6.219000, -75.590000, 3.8, 'Aeropuerto regional ubicado en el centro de la ciudad', datetime('now'), datetime('now')),
('Mercado del Río', 6.244500, -75.574000, 4.6, 'Espacio gastronómico con gran variedad de restaurantes', datetime('now'), datetime('now')),
('Cerro Nutibara', 6.237900, -75.580500, 4.3, 'Colina con vistas panorámicas y Pueblito Paisa', datetime('now'), datetime('now')),
('Planetario de Medellín', 6.270350, -75.565200, 4.8, 'Centro astronómico con exhibiciones y proyecciones', datetime('now'), datetime('now')),
('Estación San Antonio', 6.246800, -75.568100, 3.9, 'Estación principal del metro de Medellín', datetime('now'), datetime('now')),
('Museo Casa de la Memoria', 6.250000, -75.556800, 4.5, 'Museo sobre la historia del conflicto colombiano', datetime('now'), datetime('now')),
('Parque de los Deseos', 6.270600, -75.566600, 4.4, 'Parque urbano con cine al aire libre y eventos culturales', datetime('now'), datetime('now')),
('Casa Museo Pedro Nel Gómez', 6.274400, -75.554300, 4.2, 'Museo dedicado al artista y urbanista paisa', datetime('now'), datetime('now'));
EOF
echo "   ✅ Locations inserted"
echo "🔗 Creating relationship location-category..."
# Inserting relationships into location_category_reviewed
sqlite3 "$DB_FILE" << 'EOF'
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
-- Jardín Botánico -> Parque (revisión vieja)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-60 days') FROM locations l, categories c
WHERE l.name = 'Jardín Botánico de Medellín' AND c.name = 'Parque';
-- Plaza Botero -> Museo (nunca revisado)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Plaza Botero' AND c.name = 'Museo';
-- Aeropuerto Olaya -> Restaurante (revisión reciente)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-5 days') FROM locations l, categories c
WHERE l.name = 'Aeropuerto Olaya Herrera' AND c.name = 'Restaurante';
-- Mercado del Río -> Restaurante (nunca revisado)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Mercado del Río' AND c.name = 'Restaurante';
-- Cerro Nutibara -> Parque (revisión vieja)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-90 days') FROM locations l, categories c
WHERE l.name = 'Cerro Nutibara' AND c.name = 'Parque';
-- Planetario -> Museo (revisión reciente)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-2 days') FROM locations l, categories c
WHERE l.name = 'Planetario de Medellín' AND c.name = 'Museo';
-- Estación San Antonio -> Gimnasio (nunca revisado)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Estación San Antonio' AND c.name = 'Gimnasio';

-- Casa de la Memoria -> Museo (revisión vieja)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-35 days') FROM locations l, categories c
WHERE l.name = 'Museo Casa de la Memoria' AND c.name = 'Museo';

-- Parque de los Deseos -> Parque (nunca revisado)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id)
SELECT l.id, c.id FROM locations l, categories c
WHERE l.name = 'Parque de los Deseos' AND c.name = 'Parque';

-- Casa Museo Pedro Nel Gómez -> Museo (revisión reciente)
INSERT OR IGNORE INTO location_category_reviewed (location_id, category_id, was_reviewed, last_reviewed)
SELECT l.id, c.id, 1, datetime('now', '-1 day') FROM locations l, categories c
WHERE l.name = 'Casa Museo Pedro Nel Gómez' AND c.name = 'Museo';
EOF
echo "   ✅ Relationships inserted"
echo "=================================================="
echo "🎉 ¡Data seed inserted successfully!"
echo "   📊 Sumary:"
echo "      • 10 Categories"
echo "      • 20 Locatrions"
echo "      • Relationships between locations and categories"
echo "=================================================="