
from fastapi import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pymysql


from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.simulacion import DatosSimulacion
from app.api.modelos.proyectos import ProyectoCrear, ProyectoActualizar,Proyecto
from app.servicios import simulacion as servicio_simulacion

router_proyecto = APIRouter()


@router_proyecto.get("/proyectos", response_model=List[Proyecto])
async def get_proyectos():
    proyectos = await servicio_simulacion.obtener_proyectos()
    return proyectos


# Crear Proyectos 
@router_proyecto.post("/crear_proyecto/")
async def crear_proyecto(datos: ProyectoCrear):
    try:
        print(f"Nombre proyecto: {datos.nombre}")
        print(f"Descripción: {datos.descripcion}")
        print(f"usuario_id: {datos.usuario_id}")

   

        resultados = await set_proyecto(datos)
        

        return {"message": "Se registro el proyecto", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la inserción ", "details": str(e)},
        )
    



# Actualizar información de proyectos
@router_proyecto.put("/actualizar_proyecto/{id}")
async def actualizar_datos_proyecto(id,datos: ProyectoActualizar):
    
    try:
        print(f"id proyecto: {id}")
        print(f"usuario_id: {datos.usuario_id}")

       

        resultados = await actualizar_datos_proyecto(id,datos)
        

        return {"message": "Actualización de datos para actualizar completada.", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la actualización", "details": str(e)},
        )

# Eliminar proyecto por id en espesifico o todos los proyectos pertenecientes al usuario
@router_proyecto.delete("/eliminar_proyecto/")
async def eliminar_proyecto(
    id: Optional[int] = Query(None, description="Eliminar por ID"),
    usuario_id: int = Query(..., description="ID del usuario") 
) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validar que el usuario exista
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
        usuario_row = cursor.fetchone()
        if not usuario_row:
            return {
                "status": "error",
                "message": f"El usuario con ID '{usuario_id}' no existe"
            }
        # Validar existencia del proyecto
        cursor.execute("SELECT * FROM proyectos WHERE id = %s", (id,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return {
                "status": "error",
                "message": f"El proyecto con id: '{id}' no existe"
            }

        
        #Validar que el proyecto le corresponda al usuario id 
        cursor.execute("SELECT * FROM proyectos WHERE id = %s AND  usuario_id = %s", (id,usuario_id))
        proyecto_valido = cursor.fetchone()
        if not proyecto_valido:
            return {
                "status": "error",
                "message": f"El proyecto con id '{id}' no le pertenece al usuario con id '{usuario_id}'"
            }


        # Obtener proyectos a eliminar
        if id is not None:
         

            cursor.execute("SELECT id FROM proyectos WHERE id = %s AND usuario_id = %s", (id, usuario_id))
        else:
            cursor.execute("SELECT id FROM proyectos WHERE usuario_id = %s", (usuario_id))

        proyectos = cursor.fetchall()
        if not proyectos:
            return {
                "status": "error",
                "message": "No se encontraron proyectos para eliminar"
            }

        for proyecto in proyectos:
            proyecto_id = proyecto["id"]

            #Obtener dispositivos del proyecto
            cursor.execute("SELECT id FROM dispositivos WHERE proyecto_id = %s", (proyecto_id,))
            dispositivos = cursor.fetchall()

            for dispositivo in dispositivos:
                dispositivo_id = dispositivo["id"]

                # Obtener sensores del dispositivo
                cursor.execute("SELECT id FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))
                sensores = cursor.fetchall()

                for sensor in sensores:
                    sensor_id = sensor["id"]

                    # Obtener campos del sensor
                    cursor.execute("SELECT id FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))
                    campos = cursor.fetchall()

                    for campo in campos:
                        campo_id = campo["id"]

                        # Eliminar valores registrados del campo
                        cursor.execute("DELETE FROM valores WHERE campo_id = %s", (campo_id,))

                    # Eliminar campos del sensor
                    cursor.execute("DELETE FROM campos_sensores WHERE sensor_id = %s", (sensor_id,))

                # Eliminar sensores del dispositivo
                cursor.execute("DELETE FROM sensores WHERE dispositivo_id = %s", (dispositivo_id,))

            # Eliminar dispositivos del proyecto
            cursor.execute("DELETE FROM dispositivos WHERE proyecto_id = %s", (proyecto_id,))

            # Eliminar el proyecto
            cursor.execute("DELETE FROM proyectos WHERE id = %s", (proyecto_id,))

        conn.commit()
        return {
            "status": "success",
            "message": f"{len(proyectos)} proyecto(s) eliminado(s) correctamente para el usuario con ID '{usuario_id}'."
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar proyecto(s): {str(e)}")
    finally:
        if conn:
            conn.close()




#Crear proyectos
async def set_proyecto(datos: ProyectoCrear) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
       # Validar existencia del usuario
        cursor.execute("SELECT id FROM usuarios WHERE id = %s", (datos.usuario_id))
        usuario_row = cursor.fetchone()
        if not usuario_row:
            return [{
                "status": "error",
                "message": f"El usuario con id: '{datos.usuario_id}' no existe"
            }]
 
    
        # Insertar el proyecto
        cursor.execute(
            "INSERT INTO proyectos (nombre, descripcion, usuario_id) VALUES (%s, %s, %s)",
            (datos.nombre, datos.descripcion, datos.usuario_id)
        )

        conn.commit()

        procesado.append({
            "nombre": datos.nombre,
            "descripcion": datos.descripcion,
            "usuario_id": datos.usuario_id,
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

#Función para ctualizar datos del proyecto
async def actualizar_datos_proyecto(id: int, datos: ProyectoActualizar) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)


        # Validar existencia del proyecto
        cursor.execute("SELECT * FROM proyectos WHERE id = %s", (id,))
        proyecto_row = cursor.fetchone()
        if not proyecto_row:
            return [{
                "status": "error",
                "message": f"El proyecto con id: '{id}' no existe"
            }]


         # Validar que el usuario id exista 
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (datos.usuario_id))

        usuario_row = cursor.fetchone()
        if not usuario_row:
            return [{
                "status": "error",
                "message": f"El usuario con id: '{datos.usuario_id}' no existe"
            }]
        
        #Validar que el proyecto le corresponda al usuario id 
        cursor.execute("SELECT * FROM proyectos WHERE id = %s AND  usuario_id = %s", (id, datos.usuario_id))
        proyecto_valido = cursor.fetchone()
        if not proyecto_valido:
            return [{
                "status": "error",
                "message": f"El proyecto con id '{id}' no le pertenece al usuario con id '{datos.usuario_id}'"
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




        valores.append(id)  # Para el WHERE

        # Ejecutar el UPDATE solo si hay algo que actualizar
        if campos:
            sql = f"UPDATE proyectos SET {', '.join(campos)} WHERE id = %s"
            cursor.execute(sql, valores)
            conn.commit()

            procesado.append({
                "status": "success",
                "message": f"Proyecto con id '{id}'con el id de usuario '{datos.usuario_id}' actualizado correctamente",
                "actualizado": {
                    "nombre": datos.nombre,
                    "descripcion": datos.descripcion
                }
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

