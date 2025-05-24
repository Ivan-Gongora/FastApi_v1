INSERT INTO usuarios (nombre_usuario, nombre, apellido, email, contrasena, activo, fecha_registro)
VALUES (
  'juan_perez', 
  'Juan', 
  'Pérez', 
  'juan@example.com', 
  'hashed_password_123',  -- En la práctica usa un hash real
  TRUE, 
  NOW()
);

INSERT INTO proyectos (nombre, descripcion, usuario_id)
VALUES (
  'Monitoreo Ambiental', 
  'Proyecto para monitorear condiciones ambientales en la ciudad', 
  (SELECT id FROM usuarios WHERE nombre_usuario = 'juan_perez')
);


INSERT INTO unidades_medida (nombre, simbolo, descripcion)
VALUES 
  ('Grados Celsius', '°C', 'Temperatura en escala Celsius'),
  ('Porcentaje', '%', 'Porcentaje de humedad relativa'),
  ('Hectopascales', 'hPa', 'Unidad de presión atmosférica');



  INSERT INTO dispositivos (
  nombre, 
  descripcion, 
  tipo, 
  latitud, 
  longitud, 
  habilitado, 
  fecha_creacion, 
  proyecto_id
)
VALUES (
  'Estación Meteorológica Central', 
  'Dispositivo principal para mediciones climáticas', 
  'Estación Meteorológica', 
  19.432607, 
  -99.133208, 
  TRUE, 
  NOW(), 
  (SELECT id FROM proyectos WHERE nombre = 'Monitoreo Ambiental')
);


INSERT INTO sensores (
  nombre, 
  tipo, 
  fecha_creacion, 
  habilitado, 
  dispositivo_id, 
  unidad_medida_id
)
VALUES (
  'Sensor de Temperatura', 
  'Temperatura Ambiente', 
  NOW(), 
  TRUE, 
  (SELECT id FROM dispositivos WHERE nombre = 'Estación Meteorológica Central'),
  (SELECT id FROM unidades_medida WHERE simbolo = '°C')
);


INSERT INTO campos_sensores (nombre, tipo_valor, sensor_id)
VALUES 
  ('Temperatura', 'decimal', (SELECT id FROM sensores WHERE nombre = 'Sensor de Temperatura')),
  ('Precisión', 'entero', (SELECT id FROM sensores WHERE nombre = 'Sensor de Temperatura'));


  INSERT INTO valores (valor, fecha_hora_lectura, campo_id)
VALUES 
  ('23.5', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Temperatura' LIMIT 1)),
  ('95', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Precisión' LIMIT 1));







  -- Insertar sensor de Temperatura (versión actualizada)
INSERT INTO sensores (
  nombre, 
  tipo, 
  fecha_creacion, 
  habilitado, 
  dispositivo_id, 
  unidad_medida_id
)
VALUES (
  'STM-01', 
  'Temperatura Ambiente', 
  NOW(), 
  TRUE, 
  (SELECT id FROM dispositivos WHERE nombre = 'Estación Meteorológica Central'),
  (SELECT id FROM unidades_medida WHERE simbolo = '°C')
);

-- Campos para sensor de Temperatura
INSERT INTO campos_sensores (nombre, tipo_valor, sensor_id)
VALUES 
  ('Temperatura', 'decimal', (SELECT id FROM sensores WHERE nombre = 'STM-01')),
  ('Precisión', 'entero', (SELECT id FROM sensores WHERE nombre = 'STM-01')),
  ('Estado', 'texto', (SELECT id FROM sensores WHERE nombre = 'STM-01'));

-- Valores de ejemplo para Temperatura
INSERT INTO valores (valor, fecha_hora_lectura, campo_id)
VALUES 
  ('22.7', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Temperatura' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'STM-01'))),
  ('98', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Precisión' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'STM-01'))),
  ('Activo', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Estado' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'STM-01')));

-- Insertar sensor de Humedad
INSERT INTO sensores (
  nombre, 
  tipo, 
  fecha_creacion, 
  habilitado, 
  dispositivo_id, 
  unidad_medida_id
)
VALUES (
  'SHM-01', 
  'Humedad Ambiente', 
  NOW(), 
  TRUE, 
  (SELECT id FROM dispositivos WHERE nombre = 'Estación Meteorológica Central'),
  (SELECT id FROM unidades_medida WHERE simbolo = '%')
);

-- Campos para sensor de Humedad
INSERT INTO campos_sensores (nombre, tipo_valor, sensor_id)
VALUES 
  ('Humedad', 'decimal', (SELECT id FROM sensores WHERE nombre = 'SHM-01')),
  ('Precisión', 'entero', (SELECT id FROM sensores WHERE nombre = 'SHM-01')),
  ('Estado', 'texto', (SELECT id FROM sensores WHERE nombre = 'SHM-01'));

-- Valores de ejemplo para Humedad
INSERT INTO valores (valor, fecha_hora_lectura, campo_id)
VALUES 
  ('65.5', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Humedad' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'SHM-01'))),
  ('97', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Precisión' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'SHM-01'))),
  ('Activo', NOW(), (SELECT id FROM campos_sensores WHERE nombre = 'Estado' AND sensor_id = (SELECT id FROM sensores WHERE nombre = 'SHM-01')));