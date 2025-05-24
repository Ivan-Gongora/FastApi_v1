-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS sistema_iot;

-- Usar la base de datos recién creada
USE sistema_iot;

-- Tabla de usuarios
CREATE TABLE usuarios (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre_usuario VARCHAR(150) NOT NULL UNIQUE,
  nombre VARCHAR(30) NOT NULL,
  apellido VARCHAR(30) NOT NULL,
  email VARCHAR(254) NOT NULL,
  contrasena VARCHAR(128) NOT NULL,
  activo BOOLEAN NOT NULL DEFAULT TRUE,
  fecha_registro DATETIME NOT NULL,
  ultimo_login DATETIME
);

-- Tabla de proyectos
CREATE TABLE proyectos (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  descripcion TEXT NOT NULL,
  usuario_id INT NOT NULL,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tabla de unidades de medida
CREATE TABLE unidades_medida (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(20) NOT NULL,
  simbolo VARCHAR(10) NOT NULL,
  descripcion VARCHAR(100)
);

-- Tabla de dispositivos
CREATE TABLE dispositivos (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  descripcion TEXT NOT NULL,
  tipo VARCHAR(40) NOT NULL,
  latitud DOUBLE,
  longitud DOUBLE,
  habilitado BOOLEAN NOT NULL,
  fecha_creacion DATETIME NOT NULL,
  proyecto_id INT NOT NULL,
  FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
);

-- Tabla de sensores
CREATE TABLE sensores (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(40) NOT NULL,
  tipo VARCHAR(40) NOT NULL,
  fecha_creacion DATETIME NOT NULL,
  habilitado BOOLEAN NOT NULL,
  dispositivo_id INT NOT NULL,
  unidad_medida_id INT,
  FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id),
  FOREIGN KEY (unidad_medida_id) REFERENCES unidades_medida(id)
);

-- Tabla de campos de sensores
CREATE TABLE campos_sensores (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(30) NOT NULL,
  tipo_valor VARCHAR(40) NOT NULL,
  sensor_id INT NOT NULL,
  FOREIGN KEY (sensor_id) REFERENCES sensores(id)
);

-- Tabla de valores registrados
CREATE TABLE valores (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  valor VARCHAR(100) NOT NULL,
  fecha_hora_lectura DATETIME NOT NULL,
  campo_id INT NOT NULL,
  FOREIGN KEY (campo_id) REFERENCES campos_sensores(id)
);
