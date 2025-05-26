# app/servicio_simulacion.py

import csv
from datetime import datetime
import io
from typing import List, Dict, Any

from app.configuracion import configuracion
import pymysql
import pymysql.cursors

from app.api.modelos.simulacion import DatosSimulacion, DatoSensor  

# Función para obtener una conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
        host=configuracion.db_host,
        port=configuracion.db_port,
        user=configuracion.db_user,
        password=configuracion.db_password,
        database=configuracion.db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

# La función ahora acepta proyecto_id y dispositivo_id
async def simular_datos_csv(
    file_content: bytes,
    proyecto_id: int,    # Nuevo parámetro
    dispositivo_id: int  # Nuevo parámetro
) -> List[Dict[str, Any]]:
    procesado = []

    csv_file = io.StringIO(file_content.decode('utf-8'))
    reader = csv.reader(csv_file)

    header = next(reader)
    print("Cabecera del CSV:", header)

    expected_headers = ["Fecha", "Hora", "Temperatura", "Humedad"]
    if not all(h in header for h in expected_headers):
        raise ValueError("El archivo CSV debe contener las columnas 'Fecha', 'Hora', 'Temperatura', 'Humedad'.")

    fecha_idx = header.index("Fecha")
    hora_idx = header.index("Hora")
    temperatura_idx = header.index("Temperatura")
    humedad_idx = header.index("Humedad")

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for i, row in enumerate(reader):
            if not row or all(not cell.strip() for cell in row):
                continue

            try:
                fecha_str = row[fecha_idx]
                hora_str = row[hora_idx]
                temp_val = float(row[temperatura_idx])
                hum_val = float(row[humedad_idx])

                fecha_hora_lectura = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M:%S")

                # Aquí podrías usar proyecto_id y dispositivo_id si necesitaras crear sensores/dispositivos
                # en tiempo real, pero para insertar valores, solo necesitas el campo_id.
                # Se asume que los campos y sensores ya están configurados para el dispositivo_id dado.

                # Inserción para Temperatura
                sql_temp = "INSERT INTO valores (valor, fecha_hora_lectura, campo_id) VALUES (%s, %s, %s)"
                cursor.execute(sql_temp, (str(temp_val), fecha_hora_lectura, configuracion.campo_temperatura_id))

                # Inserción para Humedad
                sql_hum = "INSERT INTO valores (valor, fecha_hora_lectura, campo_id) VALUES (%s, %s, %s)"
                cursor.execute(sql_hum, (str(hum_val), fecha_hora_lectura, configuracion.campo_humedad_id))

                conn.commit()
                print(f"Fila {i+1} insertada: Temp={temp_val}, Hum={hum_val} a las {fecha_hora_lectura}")

                procesado.append({
                    "row_number": i+1,
                    "fecha_hora_lectura": fecha_hora_lectura.isoformat(),
                    "temperatura": temp_val,
                    "humedad": hum_val,
                    "status": "success",
                    "proyecto_id_used": proyecto_id, # Para confirmación
                    "dispositivo_id_used": dispositivo_id # Para confirmación
                })

            except (IndexError, ValueError) as e:
                print(f"Error procesando fila {i+1}: Formato de datos inválido. {e}")
                procesado.append({"row_number": i+1, "status": "error", "message": f"Formato de datos inválido: {e}"})
            except pymysql.Error as e:
                conn.rollback()
                print(f"Error de base de datos en fila {i+1}: {e}")
                procesado.append({"row_number": i+1, "status": "error", "message": f"Error de DB: {e}"})
            except Exception as e:
                conn.rollback()
                print(f"Error inesperado en fila {i+1}: {e}")
                procesado.append({"row_number": i+1, "status": "error", "message": f"Error inesperado: {e}"})

    finally:
        if conn:
            conn.close()

    return procesado

#Simular datos a traves de json
async def simular_datos_json(datos: DatosSimulacion) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validar proyecto
        cursor.execute("SELECT id FROM proyectos WHERE nombre = %s", (datos.proyecto,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return [{
                "status": "error",
                "message": f"Proyecto '{datos.proyecto}' no existe"
            }]
        proyecto_id = proyecto_row["id"]

        # Validar dispositivo relacionado al proyecto
        cursor.execute("SELECT id FROM dispositivos WHERE nombre = %s AND proyecto_id = %s", (datos.dispositivo, proyecto_id))
        dispositivo_row = cursor.fetchone()
        if not dispositivo_row:
            return [{
                "status": "error",
                "message": f"Dispositivo '{datos.dispositivo}' no existe en el proyecto '{datos.proyecto}'"
            }]
        dispositivo_id = dispositivo_row["id"]

        # Obtener fecha y hora
        fecha_str = datos.fecha or datetime.now().strftime("%d/%m/%Y")
        hora_str = datos.hora or datetime.now().strftime("%H:%M:%S")
        fecha_hora_lectura = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M:%S")

        # Procesar sensores
        for sensor in datos.sensores:
            for campo, valor in sensor.datos.items():
                try:
                    if campo.lower() == "temperatura":
                        campo_id = configuracion.campo_temperatura_id
                    elif campo.lower() == "humedad":
                        campo_id = configuracion.campo_humedad_id
                    else:
                        raise ValueError(f"Campo desconocido: {campo}")

                    sql = "INSERT INTO valores (valor, fecha_hora_lectura, campo_id) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(valor), fecha_hora_lectura, campo_id))
                    conn.commit()

                    procesado.append({
                        "sensor": sensor.nombre,
                        "campo": campo,
                        "valor": valor,
                        "fecha_hora_lectura": fecha_hora_lectura.isoformat(),
                        "status": "success"
                    })

                except pymysql.Error as e:
                    conn.rollback()
                    print(f"Error de DB al insertar {campo} de {sensor.nombre}: {e}")
                    procesado.append({
                        "sensor": sensor.nombre,
                        "campo": campo,
                        "valor": valor,
                        "status": "error",
                        "message": f"Error DB: {e}"
                    })

                except Exception as e:
                    conn.rollback()
                    print(f"Error inesperado: {e}")
                    procesado.append({
                        "sensor": sensor.nombre,
                        "campo": campo,
                        "valor": valor,
                        "status": "error",
                        "message": f"Error: {e}"
                    })

    finally:
        if conn:
            conn.close()

    return procesado
