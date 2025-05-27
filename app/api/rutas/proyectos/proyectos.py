
from fastapi import Path

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
from datetime import datetime
import pymysql

from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.simulacion import DatosSimulacion
from app.api.modelos.simulacionJson import DatosSimulacionJson

router = APIRouter()

from pydantic import BaseModel
from typing import List, Dict, Optional, Any


class DatoValor(BaseModel):
    datos: Dict[str, Any] 

class DatoCampo(BaseModel):
    nombre: str              #  temperatura
    valores: List[DatoValor] # lista de lecturas en distintos momentos

class DatoSensor(BaseModel):
    nombre: str                       # Sensor D HT22
    campos_sensores: List[DatoCampo] # Lista de campos como temperatura, humedad...

class DatosSimulacionJson(BaseModel):
    proyecto: str
    dispositivo: str
    fecha: Optional[str] = ""
    hora: Optional[str] = ""
    id_paquete: int = 1
    sensores: List[DatoSensor] #Lista de sensores relacionados al dispositivo

class ConfiguracionSimulacion(BaseModel):
    url: str
    intervalo: float
    proyecto: str
    dispositivo: str



# Actualizar información de proyectos
@router.put("/ActualizarDatosProyecto/{id}")
async def actualizar_datos_proyecto(id,datos: DatosSimulacionJson):
    
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
