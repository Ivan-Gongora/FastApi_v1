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
