from pydantic import BaseModel
from typing import List, Dict, Optional, Any
#clase para los proyectos 
# Modelo base (sin ID)
class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    usuario_id: int

# Modelo para crear p
class ProyectoCrear(ProyectoBase):
    pass

# Modelo para actualizar parcialmente
class ProyectoActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    usuario_id: Optional[int] = None

# Modelo con ID, por ejemplo, para respuestas
class Proyecto(ProyectoBase):
    id: int

    class Config:
        orm_mode = True  # Necesario si usas ORMs como SQLAlchemy