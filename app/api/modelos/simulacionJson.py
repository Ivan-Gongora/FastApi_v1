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
