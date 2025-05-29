# app/servicio_simulacion.py

import csv
from datetime import datetime
import io
from typing import List, Dict, Any

from app.configuracion import configuracion
import pymysql # type: ignore
import pymysql.cursors # type: ignore

from app.api.modelos.simulacion import DatosSimulacion, DatoSensor  
from app.api.modelos.simulacionJson import DatosSimulacionJson, DatoSensor  # modelo para el json en el body para la simulacion desde el post  

# --- Importa la configuración (pero no la función de conexión) ---
from app.configuracion import configuracion # Solo necesitamos la instancia de configuración

# --- Función de conexión a la base de datos (INTERNA a este módulo) ---
def get_db_connection():
    """Retorna un objeto de conexión a la base de datos usando la configuración global."""
    try:
        return pymysql.connect(
            host=configuracion.db_host,
            port=configuracion.db_port,
            user=configuracion.db_user,
            password=configuracion.db_password,
            database=configuracion.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")



# # --- Funciones de consulta de datos (AHORA LLAMAN A get_db_connection_local) ---
# async def obtener_proyectos() -> List[Dict[str, Any]]:
#     conn = None
#     try:
#         conn = get_db_connection() # ¡Cambio aquí!
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, nombre FROM proyectos")
#         proyectos = cursor.fetchall()
#         return proyectos
#     except Exception as e:
#         print(f"Error al obtener proyectos: {e}")
#         return []
#     finally:
#         if conn:
#             conn.close()



# app/servicios/simulacion.py

# ... (otras importaciones y tu función get_db_connection_local o get_db_connection) ...

async def obtener_proyectos() -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_db_connection() # O get_db_connection()
        cursor = conn.cursor()
        # ¡CAMBIO AQUÍ! ASEGÚRATE DE INCLUIR 'descripcion' Y 'usuario_id'
        cursor.execute("SELECT id, nombre, descripcion, usuario_id FROM proyectos") # <--- ¡CAMBIO CLAVE!
        proyectos = cursor.fetchall()

        # --- AÑADE ESTAS LÍNEAS TEMPORALMENTE PARA DEBUGGING ---
        print("Resultado de la consulta obtener_proyectos:", proyectos)
        if proyectos:
            print("Keys (nombres de columnas) en el primer proyecto:", proyectos[0].keys())
        # --- FIN DE LÍNEAS PARA DEBUGGING ---

        return proyectos
    except Exception as e:
        print(f"Error al obtener proyectos: {e}")
        return []
    finally:
        if conn:
            conn.close()



# --- Funcion para la consulta GET para proyectos por usuario_id
async def obtener_proyectos_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_db_connection() # O get_db_connection() si la centralizaste de nuevo
        cursor = conn.cursor()
        # ¡IMPORTANTE! Asegúrate de seleccionar 'descripcion' y 'usuario_id' también
        cursor.execute("SELECT id, nombre, descripcion, usuario_id FROM proyectos WHERE usuario_id = %s", (usuario_id,))
        # --- Imprime el resultado de la consulta para inspección ---
        result = cursor.fetchall()
        print("Resultado de la consulta:", result) # <--- AÑADIR ESTA LÍNEA TEMPORALMENTE
        return result
    except Exception as e:
        print(f"Error al obtener proyectos por usuario: {e}")
        return []
    finally:
        if conn:
            conn.close()
# # --- Funcion para la consulta GET para proyectos por id
# async def obtener_proyecto_por_id(proyecto_id: int) -> Dict[str, Any] | None:
#     conn = None
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, nombre FROM proyectos WHERE id = %s", (proyecto_id,))
#         return cursor.fetchone()
#     except Exception as e:
#         print(f"Error al obtener proyecto por ID: {e}")
#         return None
#     finally:
#         if conn:
#             conn.close()


# --- Funcion para la consulta GET para proyectos por id
# async def obtener_proyecto_por_id(proyecto_id: int) -> Dict[str, Any] | None:
#     conn = None
#     try:
#         conn = get_db_connection() # O get_db_connection() si la centralizaste de nuevo
#         cursor = conn.cursor()
        
#         # ¡IMPORTANTE! Asegúrate de seleccionar 'descripcion' y 'usuario_id' también
#         # Asegúrate de que los nombres de las columnas aquí coincidan EXACTAMENTE con los de tu DB.
#         # Por ejemplo, si en tu DB es 'usuario_ID' en lugar de 'usuario_id', debes usar 'usuario_ID'.
#         cursor.execute("SELECT id, nombre, descripcion, usuario_id FROM proyectos WHERE id = %s", (proyecto_id,))
        
#         result = cursor.fetchone() #fetchone() para un solo resultado
        
#         # --- NUEVAS LÍNEAS PARA DEBUGGING ---
#         if result:
#             print(f"Resultado completo de la consulta para proyecto ID {proyecto_id}: {result}")
#             print(f"Keys (nombres de columnas) en el resultado: {result.keys()}")
#             # Verifica si las claves esperadas están presentes
#             if 'descripcion' not in result:
#                 print("¡ADVERTENCIA! 'descripcion' no se encontró en el resultado de la consulta.")
#             if 'usuario_id' not in result:
#                 print("¡ADVERTENCIA! 'usuario_id' no se encontró en el resultado de la consulta.")
#         else:
#             print(f"No se encontró ningún proyecto con el ID {proyecto_id}.")
#         # --- FIN DE LÍNEAS PARA DEBUGGING ---
        
#         return result
#     except Exception as e:
#         print(f"Error al obtener proyecto por ID: {e}")
#         # En caso de error, puedes devolver None para que la ruta lance el 404 o 500
#         return None
#     finally:
#         if conn:
#             conn.close()
async def obtener_proyecto_por_id(proyecto_id: int) -> Dict[str, Any] | None:
    
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, usuario_id FROM proyectos WHERE id = %s", (proyecto_id,))
        return cursor.fetchone() # Asume que fetchone() devuelve un diccionario o None
    except Exception as e:
        print(f"Error al obtener proyecto por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()
async def obtener_dispositivo_por_id(dispositivo_id: int) -> Dict[str, Any] | None:
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, proyecto_id FROM dispositivos WHERE id = %s", (dispositivo_id,))
        return cursor.fetchone() # Asume que fetchone() devuelve un diccionario o None
    except Exception as e:
        print(f"Error al obtener dispositivo por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()

async def obtener_dispositivos_por_proyecto(proyecto_id: int) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_db_connection() # ¡Cambio aquí!
        cursor = conn.cursor()
        sql = "SELECT id, nombre, proyecto_id FROM dispositivos WHERE proyecto_id = %s"
        cursor.execute(sql, (proyecto_id,))
        dispositivos = cursor.fetchall()
        return dispositivos
    except Exception as e:
        print(f"Error al obtener dispositivos: {e}")
        return []
    finally:
        if conn:
            conn.close()

async def obtener_sensores_por_dispositivo(dispositivo_id: int) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_db_connection() # ¡Cambio aquí!
        cursor = conn.cursor()
        sql = "SELECT id, nombre, dispositivo_id FROM sensores WHERE dispositivo_id = %s"
        cursor.execute(sql, (dispositivo_id,))
        sensores = cursor.fetchall()
        return sensores
    except Exception as e:
        print(f"Error al obtener sensores: {e}")
        return []
    finally:
        if conn:
            conn.close()

async def obtener_campos_por_sensor(sensor_id: int) -> List[Dict[str, Any]]:
    conn = None
    try:
        conn = get_db_connection() # ¡Cambio aquí!
        cursor = conn.cursor()
        sql = "SELECT id, nombre, sensor_id FROM campos_sensores WHERE sensor_id = %s"
        cursor.execute(sql, (sensor_id,))
        campos = cursor.fetchall()
        return campos
    except Exception as e:
        print(f"Error al obtener campos: {e}")
        return []
    finally:
        if conn:
            conn.close()

# --- extract_csv_preview (sin cambios en su lógica) ---
async def extract_csv_preview(file_content: bytes) -> Dict[str, Any]:
    csv_text = file_content.decode('utf-8')
    csv_file = io.StringIO(csv_text)
    reader = csv.reader(csv_file)

    try:
        header = next(reader)
        header = [h.strip() for h in header]
    except StopIteration:
        return {"header": [], "preview_rows": [], "message": "El archivo CSV está vacío."}

    preview_rows = []
    for i, row in enumerate(reader):
        if i >= 5:
            break
        if row and any(cell.strip() for cell in row):
            preview_rows.append([cell.strip() for cell in row])

    return {"header": header, "preview_rows": preview_rows, "message": "Previsualización generada."}


# app/servicios/simulacion.py

# ... (resto de importaciones y funciones) ...


async def simular_datos_csv(
    file_content: bytes,
    sensor_mappings: List[Dict[str, Any]],
    proyecto_id: int,
    dispositivo_id: int
) -> Dict[str, Any]: # <--- ¡MIRA AQUÍ! DEBE SER Dict[str, Any]
    registros_insertados = 0
    errores_insercion = 0
    
    csv_text = file_content.decode('utf-8')
    csv_file = io.StringIO(csv_text)
    reader = csv.reader(csv_file)

    try:
        header = next(reader)
        header = [h.strip() for h in header]
        print("Cabecera del CSV en backend:", header)
    except StopIteration:
        raise ValueError("El archivo CSV está vacío o solo contiene la cabecera.")

    required_default_headers = ["Fecha", "Hora"]
    for h in required_default_headers:
        if h not in header:
            raise ValueError(f"El archivo CSV debe contener la columna '{h}'.")

    header_indices = {col_name: idx for idx, col_name in enumerate(header)}

    final_data_column_mappings = {}

    for mapping in sensor_mappings:
        campo_id = mapping['campo_id']
        campo_nombre = mapping['campo_nombre']

        csv_column_name_for_field = None
        for col_name in header:
            if col_name.lower() == campo_nombre.lower():
                csv_column_name_for_field = col_name
                break

        if csv_column_name_for_field is None:
            raise ValueError(f"El campo '{campo_nombre}' (Sensor ID: {mapping['sensor_id']}) seleccionado no tiene una columna coincidente en el CSV.")
        
        final_data_column_mappings[campo_id] = header_indices[csv_column_name_for_field]

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        fecha_idx = header_indices["Fecha"]
        hora_idx = header_indices["Hora"]

        for i, row in enumerate(reader):
            if not row or all(not cell.strip() for cell in row):
                continue

            if len(row) <= max(header_indices.values()):
                print(f"Saltando fila {i+1} debido a columnas insuficientes: {row}")
                errores_insercion += 1
                continue

            try:
                fecha_str = row[fecha_idx]
                hora_str = row[hora_idx]
                fecha_hora_lectura = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M:%S")

                for campo_id, value_idx in final_data_column_mappings.items():
                    valor = row[value_idx]

                    try:
                        valor = float(valor)
                    except ValueError:
                        pass # Si no se puede convertir a float, lo mantenemos como string

                    sql = "INSERT INTO valores (valor, fecha_hora_lectura, campo_id) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (str(valor), fecha_hora_lectura, campo_id))
                
                conn.commit()
                registros_insertados += 1
                
            except (IndexError, ValueError) as e:
                conn.rollback()
                print(f"Error procesando fila {i+1} (datos): {e}")
                errores_insercion += 1
            except Exception as e:
                conn.rollback()
                print(f"Error inesperado en fila {i+1}: {e}")
                errores_insercion += 1

    finally:
        if conn:
            conn.close()

    # <--- ¡MIRA AQUÍ! DEBE RETORNAR UN DICCIONARIO
    return {
        "message": "Proceso de simulación completado.",
        "registros_insertados": registros_insertados,
        "errores": errores_insercion
    }


    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, descripcion, proyecto_id FROM dispositivos WHERE id = %s", (dispositivo_id,))
        return cursor.fetchone() # Asume que fetchone() devuelve un diccionario o None
    except Exception as e:
        print(f"Error al obtener dispositivo por ID: {e}")
        return None
    finally:
        if conn:
            conn.close()
async def simular_datos_json(datos: DatosSimulacionJson) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Validar proyecto
        cursor.execute("SELECT id FROM proyectos WHERE nombre = %s", (datos.proyecto,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return [{
                "status": "error",
                "message": f"Proyecto '{datos.proyecto}' no existe"
            }]
        proyecto_id = proyecto_row["id"]

        # Validar dispositivo
        cursor.execute("SELECT id FROM dispositivos WHERE nombre = %s AND proyecto_id = %s", (datos.dispositivo, proyecto_id))
        dispositivo_row = cursor.fetchone()
        if not dispositivo_row:
            return [{
                "status": "error",
                "message": f"Dispositivo '{datos.dispositivo}' no existe en el proyecto '{datos.proyecto}'"
            }]
        dispositivo_id = dispositivo_row["id"]

        # Obtener fecha y hora
        fecha_str = datos.fecha or datetime.now().strftime("%d-%m-%Y")
        hora_str = datos.hora or datetime.now().strftime("%H:%M:%S")
        


        # Procesar sensores
        for sensor in datos.sensores:
            # Validar sensor
            cursor.execute("SELECT id FROM sensores WHERE nombre = %s AND dispositivo_id = %s", (sensor.nombre, dispositivo_id))
            sensor_row = cursor.fetchone()
            if not sensor_row:
                procesado.append({
                    "sensor": sensor.nombre,
                    "status": "error",
                    "message": f"Sensor '{sensor.nombre}' no existe en el dispositivo '{datos.dispositivo}'"
                })
                continue
            sensor_id = sensor_row["id"]

            for campo in sensor.campos_sensores:
                # Validar campo
                cursor.execute("SELECT id FROM campos_sensores WHERE nombre = %s AND sensor_id = %s", (campo.nombre, sensor_id))
                campo_row = cursor.fetchone()
                if not campo_row:
                    procesado.append({
                        "sensor": sensor.nombre,
                        "campo": campo.nombre,
                        "status": "error",
                        "message": f"Campo '{campo.nombre}' no existe en el sensor '{sensor.nombre}'"
                    })
                    continue
                campo_id = campo_row["id"]

                for valor in campo.valores:
                    for  fecha_lectura, medicion in valor.datos.items():
                        try:
                            fecha_lectura = datetime.strptime(f"{fecha_str} {hora_str}", "%d-%m-%Y %H:%M:%S")
                            cursor.execute(
                                "INSERT INTO valores (valor, fecha_hora_lectura, campo_id) VALUES (%s, %s, %s)",
                                (medicion, fecha_lectura, campo_id)
                            )
                            conn.commit()
                            procesado.append({
                                "sensor": sensor.nombre,
                                "campo": campo.nombre,
                                "valor": medicion,
                                "fecha_hora_lectura": fecha_lectura.isoformat(),
                                "status": "success"
                            })
                        except pymysql.MySQLError as e:
                            conn.rollback()
                            procesado.append({
                                "sensor": sensor.nombre,
                                "campo": campo.nombre,
                                "valor": medicion,
                                "status": "error",
                                "message": f"DB Error: {str(e)}"
                            })
                        except Exception as e:
                            conn.rollback()
                            procesado.append({
                                "sensor": sensor.nombre,
                                "campo": campo.nombre,
                                "valor": medicion,
                                "status": "error",
                                "message": f"Unexpected Error: {str(e)}"
                            })

    finally:
        if conn:
            conn.close()

    return procesado
