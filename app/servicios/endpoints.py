from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict
from datetime import datetime
import pymysql

from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection

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