


ALTER TABLE usuarios
ADD COLUMN tipo_usuario VARCHAR(50) NOT NULL DEFAULT 'empleado' AFTER ultimo_login;


