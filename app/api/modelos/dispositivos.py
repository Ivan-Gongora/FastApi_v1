from pydantic import BaseModel
from typing import List, Dict, Optional, Any

#clase para los dispositivos
# Modelo base (sin ID)
class DispositivoBase(BaseModel):
    nombre: str
    descripcion: str
    tipo: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    habilitado: bool
    fecha_creacion: Optional[str] = ""
    proyecto_id: int

# Modelo para crear dispositivo
class DispositivoCrear(DispositivoBase):
    pass

# Modelo para actualizar parcialmente
class DispositivoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    habilitado: Optional[bool] = None


# Modelo con ID, por ejemplo, para respuestas
class Dispositivo(DispositivoBase):
    id: int

    class Config:
        orm_mode = True

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