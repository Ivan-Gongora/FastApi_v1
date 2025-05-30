from fastapi import Path # type: ignore
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from datetime import datetime
import pymysql # type: ignore


from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.dispositivos import DispositivoCrear, DispositivoActualizar,Dispositivo, Sensor, CampoSensor
from app.servicios import simulacion as servicio_simulacion 

router_dispositivo = APIRouter()

# Crear Proyectos 
@router_dispositivo.post("/dispositivos/")
async def crear_Dispositivo(datos: DispositivoCrear):
    try:
        print(f"Nombre del dispositivo: {datos.nombre}")
        print(f"Descripción: {datos.descripcion}")
        print(f"id del proyecto: {datos.proyecto_id}")

   

        resultados = await set_dispositivo(datos)
        

        return {"message": "Se registro el dispositivo", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la inserción ", "details": str(e)},
        )
    

# Actualizar información de proyectos
@router_dispositivo.put("/actualizar_dispositivo/")
async def actualizar_datos_dispositivo(dispositivo_id: int ,datos: DispositivoActualizar):
    
    try:
        print(f"id proyecto: {id}")
    

       

        resultados = await actualizar_datos_dispositivo(dispositivo_id,datos)
        

        return {"message": "Actualización de datos para actualizar completada.", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la actualización", "details": str(e)},
        )
    
# Eliminar dispositivo por id en espesifico o todos los proyectos pertenecientes al proyecto  
@router_dispositivo.delete("/eliminar_dispositivo/")
async def eliminar_dispositivo(
    id: Optional[int] = Query(None, description="Eliminar por ID"),
    proyecto_id: int = Query(..., description="ID del proeyecto")
) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validar existencia del proyecto
        cursor.execute("SELECT * FROM proyectos WHERE id = %s", (proyecto_id,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return {
                "status": "error",
                "message": f"El proyecto con id: '{proyecto_id}' no existe"
            }

        # Obtener lista de dispositivos a eliminar
        if id is not None:
        # Validar que el dispositivo pertenezca al poyecto
            cursor.execute("SELECT * FROM dispositivos WHERE id = %s AND proyecto_id = %s", (id, proyecto_id))
            dispositivo_valido = cursor.fetchone()
            if not dispositivo_valido:
                return {
                    "status": "error",
                    "message": f"El dispositivo con id '{id}' no pertenece al proyecto con id '{proyecto_id}'"
                }

            cursor.execute("SELECT id FROM dispositivos WHERE id = %s AND proyecto_id = %s", (id, proyecto_id))
        else:
            cursor.execute("SELECT id FROM dispositivos WHERE proyecto_id = %s", (proyecto_id,))

        dispositivos = cursor.fetchall()
        if not dispositivos:
            return {
                "status": "error",
                "message": "No se encontraron dispositivos para eliminar"
            }


        for dispositivo in dispositivos:
            dispositivo_id = dispositivo["id"]

            # Eliminar valores → campos → sensores del dispositivo
            cursor.execute("SELECT id FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))
            sensores = cursor.fetchall()

            for sensor in sensores:
                sensor_id = sensor["id"]

                cursor.execute("SELECT id FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))
                campos = cursor.fetchall()

                for campo in campos:
                    campo_id = campo["id"]
                    cursor.execute("DELETE FROM valores WHERE campo_id = %s", (campo_id,))

                cursor.execute("DELETE FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))

            cursor.execute("DELETE FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))
            cursor.execute("DELETE FROM dispositivos WHERE id = %s", (dispositivo_id,))

 

        conn.commit()
        return {
            "status": "success",
            "message": f"{len(dispositivos)} dispositivo(s) eliminado(s) correctamente del proyecto con ID '{proyecto_id}'."
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar dispositivo(s): {str(e)}")

    finally:
        if conn:
            conn.close()

#Crear dispositivo
async def set_dispositivo(datos: DispositivoCrear) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Validar existencia del proyecto
        cursor.execute("SELECT id FROM proyectos WHERE id = %s", (datos.proyecto_id,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return [{
                "status": "error",
                "message": f"El proyecto con id: '{datos.proyecto_id}' no existe"
            }]
        # Obtener fecha 
        fecha_creacion = datos.fecha_creacion or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        


        # Insertar el dispositivo
        cursor.execute("INSERT INTO dispositivos (nombre, descripcion, tipo, latitud, longitud, habilitado, fecha_creacion, proyecto_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
            datos.nombre,
            datos.descripcion,
            datos.tipo,
            datos.latitud,
            datos.longitud,
            datos.habilitado,
            fecha_creacion,
            datos.proyecto_id
        ))

        conn.commit()
        procesado.append({
            "nombre": datos.nombre,
            "descripcion": datos.descripcion,
            "tipo": datos.tipo,
            "latitud": datos.latitud,
            "longitud": datos.longitud,
            "habilitado": datos.habilitado,
            "fecha_creacion": fecha_creacion,
            "proyecto_id": datos.proyecto_id,
            "status": "success"
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

# Función para actualizar datos del dispositivo
async def actualizar_datos_dispositivo(dispositivo_id: int, datos: DispositivoActualizar) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Validar existencia del dispositivo
        cursor.execute("SELECT * FROM dispositivos WHERE id = %s", (dispositivo_id,))
        dispositivo_row = cursor.fetchone()
        if not dispositivo_row:
            return [{
                "status": "error",
                "message": f"El dispositivo con id: '{dispositivo_id}' no existe"
            }]

        # Construir lista de campos a actualizar dinámicamente
        campos = []
        valores = []

        if datos.nombre is not None:
            campos.append("nombre = %s")
            valores.append(datos.nombre)

        if datos.descripcion is not None:
            campos.append("descripcion = %s")
            valores.append(datos.descripcion)

        if datos.tipo is not None:
            campos.append("tipo = %s")
            valores.append(datos.tipo)

        if datos.latitud is not None:
            campos.append("latitud = %s")
            valores.append(datos.latitud)

        if datos.longitud is not None:
            campos.append("longitud = %s")
            valores.append(datos.longitud)

        if datos.habilitado is not None:
            campos.append("habilitado = %s")
            valores.append(datos.habilitado)

        # Agregar ID para el WHERE
        valores.append(dispositivo_id)

        # Ejecutar el UPDATE solo si hay campos que actualizar
        if campos:
            sql = f"UPDATE dispositivos SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(sql, valores)
            conn.commit()

            procesado.append({
                "status": "success",
                "message": f"Dispositivo con id '{dispositivo_id}' actualizado correctamente",
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


@router_dispositivo.get("/proyectos/{proyecto_id}/dispositivos", response_model=List[Dispositivo])
async def get_dispositivos_por_proyecto(proyecto_id: int):
    dispositivos = await servicio_simulacion.obtener_dispositivos_por_proyecto(proyecto_id)
    if not dispositivos:
        # Aunque no es un error de servidor, un 404 es una respuesta apropiada si no hay dispositivos
        raise HTTPException(status_code=404, detail="No se encontraron dispositivos para este proyecto.")
    return dispositivos

@router_dispositivo.get("/dispositivos/{dispositivo_id}/sensores", response_model=List[Sensor])
async def get_sensores_por_dispositivo(dispositivo_id: int):
    sensores = await servicio_simulacion.obtener_sensores_por_dispositivo(dispositivo_id)
    if not sensores:
        raise HTTPException(status_code=404, detail="No se encontraron sensores para este dispositivo.")
    return sensores

@router_dispositivo.get("/sensores/{sensor_id}/campos", response_model=List[CampoSensor])
async def get_campos_por_sensor(sensor_id: int):
    campos = await servicio_simulacion.obtener_campos_por_sensor(sensor_id)
    if not campos:
        raise HTTPException(status_code=404, detail="No se encontraron campos para este sensor.")
    return campos

#Peticiones GET con filtrado individual
@router_dispositivo.get("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
async def get_dispositivo_por_id(dispositivo_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM dispositivos WHERE id = %s", (dispositivo_id,))
        dispositivo = cursor.fetchone()

        if not dispositivo:
            raise HTTPException(status_code=404, detail=f"Dispositivo con ID '{dispositivo_id}' no encontrado.")

        return dispositivo

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar el dispositivo: {str(e)}")

    finally:
        if conn:
            conn.close()

#Peticiones GET con filtrado general
@router_dispositivo.get("/dispositivos", response_model=List[Dispositivo])
async def get_todos_los_dispositivos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM dispositivos")
        dispositivos = cursor.fetchall()

        if not dispositivos:
            raise HTTPException(status_code=404, detail="No se encontraron dispositivos en la base de datos.")

        return dispositivos

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar los dispositivos: {str(e)}")

    finally:
        if conn:
            conn.close()
