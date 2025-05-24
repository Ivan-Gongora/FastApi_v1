from pydantic import BaseModel
from typing import List, Dict, Optional

class DatoSensor(BaseModel):
    nombre: str
    datos: Dict[str, float]

class DatosSimulacion(BaseModel):
    proyecto: str
    dispositivo: str
    fecha: Optional[str] = ""
    hora: Optional[str] = ""
    id_paquete: int = 1
    sensores: List[DatoSensor]

class ConfiguracionSimulacion(BaseModel):
    url: str
    intervalo: float
    proyecto: str
    dispositivo: str