from pydantic import BaseModel
from typing import List, Dict, Optional, Any

#clase para los dispositivos
# Modelo base (sin ID)
class   SensorBase(BaseModel):
    nombre: str
    tipo: str
    fecha_creacion: Optional[str] = ""
    habilitado: bool
    dispositivo_id: int
    unidad_medida_id: Optional[int] = ""
   
# Modelo para crear dispositivo
class SensorCrear(SensorBase):
    pass

# Modelo para actualizar parcialmente
class SensorActualizar(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    habilitado: Optional[bool] = None
  


# Modelo con ID, por ejemplo, para respuestas
class Sensor(SensorBase):
    id: int

    class Config:
        orm_mode = True
