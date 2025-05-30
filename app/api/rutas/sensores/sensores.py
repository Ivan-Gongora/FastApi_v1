from fastapi import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pymysql


from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.sensores import SensorCrear, SensorActualizar, Sensor

router_sensor= APIRouter()

# Crear Proyectos 
@router_sensor.post("/crear_sensor/")
async def crear_sensor(datos: SensorCrear):
    try:
        print(f"Nombre del Sensor: {datos.nombre}")
        print(f"tipo: {datos.tipo}")
        print(f"id del dispositivo: {datos.dispositivo_id}")

   

        resultados = await set_sensor(datos)
        

        return {"message": "Se registro el sensor", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la inserción ", "details": str(e)},
        )
    
#Crear Sensor
async def set_sensor(datos: SensorCrear) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Validar existencia del dispositivo
        cursor.execute("SELECT id FROM dispositivos WHERE id = %s", (datos.dispositivo_id,))
        dispositivo_row = cursor.fetchone()
        if not dispositivo_row:
            return [{
                "status": "error",
                "message": f"El dispositivos con id: '{datos.dispositivo_id}' no existe"
            }]
    


        # Obtener fecha 
        fecha_creacion = datos.fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        


        # Insertar el sensor
        cursor.execute("INSERT INTO sensores (nombre, tipo,habilitado, fecha_creacion, dispositivo_id) VALUES (%s, %s, %s, %s, %s)", (
            datos.nombre,
            datos.tipo,
            datos.habilitado,
            fecha_creacion,
            datos.dispositivo_id
        ))

        conn.commit()
     # Agregar datos procesados
        procesado.append({
            "status": "success",
            "message": "Sensor creado exitosamente",
            "sensor": {
                "nombre": datos.nombre,
                "tipo": datos.tipo,
                "habilitado": datos.habilitado,
                "fecha_creacion": fecha_creacion,
                "dispositivo_id": datos.dispositivo_id
            }
        })


    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"DB Error: {str(e)}"
        })

    except Exception as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"Unexpected Error: {str(e)}"
        })

    finally:
        if conn:
            conn.close()

    return procesado


# Actualizar información del sensor
@router_sensor.put("/actualizar_sensor/")
async def actualizar_datos_sensor(sensor_id: int ,datos: SensorActualizar):
    
    try:
        print(f"id proyecto: {id}")
    

       

        resultados = await actualizar_datos_sensor(sensor_id,datos)
        

        return {"message": "Actualización de datos para actualizar completada.", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la actualización", "details": str(e)},
        )
    
# Eliminar sensor por id en espesifico o todos los sensores que pertenecientes al dispositivo
@router_sensor.delete("/eliminar_sensor/")
async def eliminar_sensor(
    id: Optional[int] = Query(None, description="Eliminar por ID"),
    dispositivo_id: int = Query(..., description="ID del dispositivo al que pertenece")
) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

      # Validar existencia del dispositivo
        cursor.execute("SELECT * FROM dispositivos WHERE id = %s", (dispositivo_id,))
        dispositivo = cursor.fetchone()
        if not dispositivo:
            return {
                "status": "error",
                "message": f"El dispositivo con id: '{dispositivo_id}' no existe"
            }

        # Obtener sensores a eliminar
        if id is not None:
            # Verificar que el sensor pertenezca al dispositivo
            cursor.execute("SELECT id FROM sensores WHERE id = %s AND dispositivo_id = %s", (id, dispositivo_id))
        else:
            cursor.execute("SELECT id FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))

        sensores = cursor.fetchall()
        if not sensores:
            return {
                "status": "error",
                "message": "No se encontraron sensores para eliminar"
            }

        # Eliminar sensores y datos relacionados
        for sensor in sensores:
            sensor_id = sensor["id"]

            # Obtener campos del sensor
            cursor.execute("SELECT id FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))
            campos = cursor.fetchall()

            # Eliminar valores registrados
            for campo in campos:
                campo_id = campo["id"]
                cursor.execute("DELETE FROM valores WHERE campo_id = %s", (campo_id,))

            # Eliminar campos del sensor
            cursor.execute("DELETE FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))

            # Eliminar el sensor
            cursor.execute("DELETE FROM sensores WHERE id = %s", (sensor_id,))

        conn.commit()
        return {
            "status": "success",
            "message": f"{len(sensores)} sensor(es) eliminado(s) correctamente del dispositivo con ID '{dispositivo_id}'."
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar sensores: {str(e)}")

    finally:
        if conn:
            conn.close()
        
# Obtener los sensores por el dispositivo al que pertenece o la lista completa 
@router_sensor.get("/sensores/", response_model=List[Sensor])
async def obtener_sensores(
    id: Optional[int] = Query(None, description="ID del sensor específico"),
    dispositivo_id: Optional[int] = Query(None, description="ID del dispositivo para filtrar sensores")
):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        if id is not None:
                if dispositivo_id is not None:
                    # Verificar si el sensor con ese ID pertenece al dispositivo
                    cursor.execute("SELECT * FROM sensores WHERE id = %s AND dispositivo_id = %s", (id, dispositivo_id))
                else:
                    # Buscar el sensor solo por ID
                    cursor.execute("SELECT * FROM sensores WHERE id = %s", (id,))
                
                sensor = cursor.fetchone()
                if not sensor:
                    raise HTTPException(status_code=404, detail="Sensor no encontrado")
                
                # Convertir fecha_creacion a string
                if isinstance(sensor.get("fecha_creacion"), datetime):
                    sensor["fecha_creacion"] = sensor["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")
                return [sensor]

        elif dispositivo_id is not None:
                # Verificar si el dispositivo existe
                cursor.execute("SELECT id FROM dispositivos WHERE id = %s", (dispositivo_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail=f"Dispositivo con ID {dispositivo_id} no encontrado")

                # Sensores del dispositivo
                cursor.execute("SELECT * FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))
                sensores = cursor.fetchall()

                # Convertir fechas
                for row in sensores:
                    if isinstance(row.get("fecha_creacion"), datetime):
                        row["fecha_creacion"] = row["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")
                return sensores

        else:
                # Todos los sensores
                cursor.execute("SELECT * FROM sensores")
                sensores = cursor.fetchall()

                # Convertir fechas
                for row in sensores:
                    if isinstance(row.get("fecha_creacion"), datetime):
                        row["fecha_creacion"] = row["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")
                return sensores

    except pymysql.MySQLError as e:
            raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    finally:
            if conn:
                conn.close()

# Función para actualizar datos del sensor
async def actualizar_datos_sensor(sensor_id: int, datos: SensorActualizar) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Validar existencia del sensor
        cursor.execute("SELECT * FROM sensores WHERE id = %s", (sensor_id,))
        sensor_row = cursor.fetchone()
        if not sensor_row:
            return [{
                "status": "error",
                "message": f"El sensor con id: '{sensor_id}' no existe"
            }]

        # Construir lista de campos a actualizar dinámicamente
        campos = []
        valores = []

        if datos.nombre is not None:
            campos.append("nombre = %s")
            valores.append(datos.nombre)

        if datos.tipo is not None:
            campos.append("tipo = %s")
            valores.append(datos.tipo)

        if datos.habilitado is not None:
            campos.append("habilitado = %s")
            valores.append(datos.habilitado)

        # Agregar ID para el WHERE
        valores.append(sensor_id)

        # Ejecutar el UPDATE solo si hay campos que actualizar
        if campos:
            sql = f"UPDATE sensores SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(sql, valores)
            conn.commit()

            procesado.append({
                "status": "success",
                "message": f"Sensor con id '{sensor_id}' actualizado correctamente",
                "actualizado": datos.dict(exclude_none=True)
            })
        else:
            procesado.append({
                "status": "warning",
                "message": "No se proporcionaron datos para actualizar"
            })

    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"DB Error: {str(e)}"
        })

    except Exception as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"Unexpected Error: {str(e)}"
        })

    finally:
        if conn:
            conn.close()

    return procesado

