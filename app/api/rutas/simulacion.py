# app/api/rutas/simulacion.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status # type: ignore
from typing import List, Dict, Any, Optional
import json

# Importaciones de los servicios que necesita este router
from app.servicios import servicio_simulacion as servicio_simulacion
from app.servicios import email_sender
from app.configuracion import configuracion # <-- ¡Aquí se usa ahora!

# Crea una instancia de APIRouter para agrupar las rutas de simulación
router = APIRouter()

# --- Endpoint para la previsualización del CSV ---
@router.post("/csv-preview/")
async def get_csv_preview(file: UploadFile = File(...)):
    """
    Procesa un archivo CSV para extraer encabezados y una previsualización de filas.
    """
    try:
        file_content = await file.read()
        preview_data = await servicio_simulacion.extract_csv_preview(file_content)
        return preview_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al procesar el CSV para previsualización: {e}"
        )

# --- Endpoint para la simulación y registro de datos ---
@router.post("/simular/")
async def simular_datos(
    file: UploadFile = File(...),
    sensor_mappings: str = Form(...), # Viene como un string JSON
    proyecto_id: int = Form(...),
    dispositivo_id: int = Form(...)
):
    """
    Simula la carga de datos desde un archivo CSV a la base de datos,
    aplicando mapeos de sensores y enviando una alerta por correo.
    """
    try:
        parsed_mappings = json.loads(sensor_mappings)
        if not isinstance(parsed_mappings, list):
            raise ValueError("`sensor_mappings` debe ser una lista JSON válida.")

        file_content = await file.read()
        print(f"Archivo recibido: {file.filename}, tamaño: {len(file_content)} bytes")
        print(f"IDs recibidos: Proyecto={proyecto_id}, Dispositivo={dispositivo_id}")
        # print(f"Mapeos recibidos: {parsed_mappings}") # Descomentar para depuración si es necesario

        simulacion_result = await servicio_simulacion.simular_datos_csv(
            file_content=file_content,
            sensor_mappings=parsed_mappings,
            proyecto_id=proyecto_id,
            dispositivo_id=dispositivo_id
        )

        # --- Lógica para el envío de correo electrónico ---
        if simulacion_result and simulacion_result.get("registros_insertados", 0) > 0:
            proyecto = await servicio_simulacion.obtener_proyecto_por_id(proyecto_id)
            dispositivo = await servicio_simulacion.obtener_dispositivo_por_id(dispositivo_id)

            proyecto_nombre = proyecto.get("nombre", "Desconocido") if proyecto else "Desconocido"
            dispositivo_nombre = dispositivo.get("nombre", "Desconocido") if dispositivo else "Desconocido"

            asunto_correo = f"Alerta: Nuevos datos registrados para Proyecto '{proyecto_nombre}'"
            cuerpo_html = f"""
            <html>
            <body>
                <p>Estimado usuario,</p>
                <p>Se han registrado <strong>{simulacion_result.get('registros_insertados', 0)} nuevos datos</strong> en la base de datos a través de la simulación IoT.</p>
                <p><strong>Detalles de la simulación:</strong></p>
                <ul>
                    <li><strong>Proyecto:</strong> {proyecto_nombre} (ID: {proyecto_id})</li>
                    <li><strong>Dispositivo:</strong> {dispositivo_nombre} (ID: {dispositivo_id})</li>
                    <li><strong>Archivo procesado:</strong> {file.filename}</li>
                    <li><strong>Registros insertados:</strong> {simulacion_result.get('registros_insertados', 0)}</li>
                    <li><strong>Errores al insertar:</strong> {simulacion_result.get('errores', 0)}</li>
                </ul>
                <p>Por favor, revisa la plataforma para más detalles.</p>
                <p>Saludos cordiales,</p>
                <p>Tu Sistema de Alertas IoT</p>
            </body>
            </html>
            """

            # Obtener el correo destinatario fijo desde app.configuracion
            # ¡CORREGIDO AQUÍ! Se usa el nombre del atributo en MAYÚSCULAS
            destinatario_fijo = configuracion.EMAIL_DESTINATARIO_ALERTA 
            
            email_enviado_exito = await email_sender.enviar_correo_alerta_registro(
                asunto=asunto_correo,
                cuerpo=cuerpo_html,
                destinatario_correo=destinatario_fijo
            )
            if not email_enviado_exito:
                print("Advertencia: El correo de alerta no pudo ser enviado.")

        return {"message": "Simulación y carga de datos en DB completada.", "resultados": simulacion_result}

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Formato JSON inválido para `sensor_mappings`. Asegúrate de que es un string JSON válido."
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error de validación: {e}"
        )
    except Exception as e:
        print(f"Error inesperado en el endpoint /api/simular/: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor durante la simulación: {e}"
        )