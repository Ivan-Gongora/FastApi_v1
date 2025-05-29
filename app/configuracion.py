# app/configuracion.py (CORREGIDO)

import os

class ConfiguracionSimulacion:
    # --- Configuración de Base de Datos MySQL (XAMPP) ---
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", 3306))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "sistema_iot")

    campo_temperatura_id: int = 2
    campo_humedad_id: int = 3

    # --- Configuración para envío de correos ---
    # ¡NOMBRES DE ATRIBUTOS CAMBIADOS A MAYÚSCULAS AQUÍ!
    EMAIL_SMTP_SERVER: str = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", 587))
    
    EMAIL_REMITENTE: str = os.getenv("EMAIL_REMITENTE_CORREO") # <-- ¡Cambio aquí!
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")         # <-- ¡Cambio aquí!
    
    EMAIL_DESTINATARIO_ALERTA: str = os.getenv("EMAIL_DESTINATARIO_ALERTA", "ivangongora1092@gmail.com")


configuracion = ConfiguracionSimulacion()