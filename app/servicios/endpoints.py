from fastapi import Path
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
from datetime import datetime
import pymysql

from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json
from app.api.modelos.simulacionJson import DatosSimulacionJson


from app.api.modelos.simulacion import DatosSimulacion


router = APIRouter()

@router.get("/valores/")
async def obtener_valores(
    id: Optional[int] = Query(None, description="Identificacion"),
    campo_id: Optional[int] = Query(None, description="Filtrar por ID del campo"),
    fecha_inicio: Optional[str] = Query(None, description="Fecha inicial en formato YYYY-MM-DD"),
    fecha_fin: Optional[str] = Query(None, description="Fecha final en formato YYYY-MM-DD")
) -> List[Dict]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM valores WHERE 1=1"
        params = []

        if id is not None:
            query += " AND id = %s"
            params.append(id)
        if campo_id is not None:
            query += " AND campo_id = %s"
            params.append(campo_id)
        
        if fecha_inicio:
            query += " AND fecha_hora_lectura >= %s"
            params.append(fecha_inicio)

        if fecha_fin:
            query += " AND fecha_hora_lectura <= %s"
            params.append(fecha_fin)

        cursor.execute(query, params)
        resultados = cursor.fetchall()
        return resultados

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")
    finally:
        conn.close()


@router.delete("/valores/")
async def eliminar_valores(
    id: Optional[int] = Query(None, description="Identificacion"),
    campo_id: Optional[int] = Query(None, description="Eliminar por campo_id"),
    fecha_limite: Optional[str] = Query(None, description="Eliminar datos anteriores a esta fecha (YYYY-MM-DD)")
) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "DELETE FROM valores WHERE 1=1"
        params = []

        if id is not None:
            query += " And id = %s"
            params.append(id)

        if campo_id is not None:
            query += " AND campo_id = %s"
            params.append(campo_id)

        if fecha_limite:
            query += " AND fecha_hora_lectura < %s"
            params.append(fecha_limite)

        resultado = cursor.execute(query, params)
        conn.commit()
        return {"message": f"{resultado} registros eliminados."}

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar datos: {str(e)}")
    finally:
        conn.close()

# Eliminar valor del id del campo correspondiente enviado
@router.delete("/EliminaValoresId/{id}")
async def eliminar_valores(
    id: int = Path(..., description="ID del valor a eliminar (por ruta)"),
    campo_id: Optional[int] = Query(None, description="Eliminar por campo_id"),
    fecha_limite: Optional[str] = Query(None, description="Eliminar datos anteriores a esta fecha (YYYY-MM-DD)")
) -> Dict:
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Comienza con una condición obligatoria por el ID de la ruta
        query = "DELETE FROM valores WHERE campo_id = %s"
        params = [id]

        # Si se agrega campo_id como condición adicional
        if campo_id is not None:
            query += " AND campo_id = %s"
            params.append(campo_id)

        # Si se agrega la fecha límite
        if fecha_limite:
            query += " AND fecha_hora_lectura < %s"
            params.append(fecha_limite)

        resultado = cursor.execute(query, params)
        conn.commit()

        return {"message": f"{resultado} registro(s) eliminado(s)."}

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar datos: {str(e)}")
    finally:
        conn.close()



# Simular datos desde json
@router.post("/simularDatos/")
async def simular_datos(datos: DatosSimulacionJson):
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

