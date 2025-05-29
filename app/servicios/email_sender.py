# app/servicios/email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# --- CAMBIO CLAVE AQUÍ ---
# Debes importar la INSTANCIA 'configuracion', no la CLASE 'ConfiguracionSimulacion'
from app.configuracion import configuracion # <-- ¡CORREGIDO!

async def enviar_correo_alerta_registro(
    asunto: str,
    cuerpo: str,
    destinatario_correo: str,
    # Ahora accedemos a los atributos de la instancia 'configuracion'
    remitente_correo: str = configuracion.EMAIL_REMITENTE,
    remitente_password: str = configuracion.EMAIL_PASSWORD,
    smtp_server: str = configuracion.EMAIL_SMTP_SERVER,
    smtp_port: int = configuracion.EMAIL_SMTP_PORT
):
    """
    Envía un correo electrónico de alerta utilizando las credenciales y configuración
    definidas en app/configuracion.py.

    Args:
        asunto (str): El asunto del correo.
        cuerpo (str): El cuerpo del correo (puede ser HTML).
        destinatario_correo (str): La dirección de correo del destinatario.
        remitente_correo (str): Opcional. La dirección de correo del remitente. Si no se provee, usa configuracion.EMAIL_REMITENTE.
        remitente_password (str): Opcional. La contraseña del remitente. Si no se provee, usa configuracion.EMAIL_PASSWORD.
        smtp_server (str): Opcional. El servidor SMTP. Si no se provee, usa configuracion.EMAIL_SMTP_SERVER.
        smtp_port (int): Opcional. El puerto SMTP. Si no se provee, usa configuracion.EMAIL_SMTP_PORT.
    """
    
    # Validar que las credenciales estén presentes
    if not remitente_correo or not remitente_password:
        print("Error: El correo remitente o la contraseña de aplicación no están configurados.")
        print("Asegúrate de que EMAIL_REMITENTE_CORREO y EMAIL_PASSWORD estén definidos como variables de entorno.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = remitente_correo
        msg["To"] = destinatario_correo
        msg["Subject"] = asunto

        # Versiones de texto plano y HTML del cuerpo del correo
        part1 = MIMEText(cuerpo, "plain")
        part2 = MIMEText(cuerpo, "html")
        msg.attach(part1)
        msg.attach(part2)

        print(f"Intentando conectar al servidor SMTP: {smtp_server}:{smtp_port}")

        # Crear un contexto SSL/TLS por defecto para mayor seguridad
        context = ssl.create_default_context()

        # Conectar al servidor SMTP usando STARTTLS (puerto 587)
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context) # Usar el contexto SSL aquí
            server.login(remitente_correo, remitente_password)
            server.send_message(msg)

        print(f"Correo enviado con éxito a {destinatario_correo}")
        return True

    except smtplib.SMTPAuthenticationError:
        print(f"Error de autenticación SMTP. Revisa el correo y la contraseña del remitente.")
        print("Asegúrate de que estás usando la 'Contraseña de aplicación' correcta para Gmail y no tu contraseña principal.")
        print("Revisa también: https://accounts.google.com/DisplayUnlockCaptcha si es un entorno nuevo.")
        return False
    except smtplib.SMTPConnectError as e:
        print(f"Error de conexión SMTP: {e}. Revisa el servidor ({smtp_server}) y el puerto ({smtp_port}).")
        print("Podría ser un problema de firewall o de red.")
        return False
    except Exception as e:
        print(f"Error inesperado al enviar correo: {e}")
        return False

# El bloque if __name__ == "__main__": si lo tienes, no necesita cambios.