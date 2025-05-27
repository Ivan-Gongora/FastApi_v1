
from fastapi import Path
from typing import List, Dict, Any
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pymysql

from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.simulacion import DatosSimulacion
from app.api.modelos.proyectos import ProyectoCrear, ProyectoActualizar

router_proyecto = APIRouter()




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
@router_proyecto.put("/ActualizarDatosProyecto/{id}")
async def actualizar_datos_proyecto(id,datos: ProyectoActualizar):
    
    try:
        print(f"Proyecto: {datos.proyecto}")
        print(f"Dispositivo: {datos.dispositivo}")
        print(f"Fecha: {datos.fecha}, Hora: {datos.hora}")
        print(f"Sensores recibidos: {len(datos.sensores)}")

        for sensor in datos.sensores:
            print(f"Sensor: {sensor.nombre}")
            for campo in sensor.campos_sensores:
                print(f"  Campo: {campo.nombre}")
                for valor in campo.valores:
                    print(f"    Datos: {valor.datos}")



        resultados = await simular_datos_json(datos)
        

        return {"message": "Simulación completada con JSON.", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error en los datos enviados", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la simulación", "details": str(e)},
        )



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
