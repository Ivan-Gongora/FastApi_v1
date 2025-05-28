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
class Proyecto(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class Dispositivo(BaseModel):
    id: int
    nombre: str
    proyecto_id: int

    class Config:
        from_attributes = True

class Sensor(BaseModel):
    id: int
    nombre: str
    dispositivo_id: int

    class Config:
        from_attributes = True

class CampoSensor(BaseModel):
    id: int
    nombre: str
    sensor_id: int

    class Config:
        from_attributes = True

# Si necesitas un modelo para los datos que vienen del CSV/simulación
class ValorSimuladoResponse(BaseModel):
    row_number: int
    fecha_hora_lectura: str
    status: str
    inserted_mappings: int
    dispositivo_id: int
    proyecto_id: int
    message: Optional[str] = None
