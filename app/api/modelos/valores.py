from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Modelo base (común a crear y respuesta)
class ValorBase(BaseModel):
    campo_id: int
    valor: float
    fecha_hora_lectura: datetime

# Para crear un nuevo valor (sin ID)
class ValorCrear(ValorBase):
    pass

# Para actualizar parcialmente un valor
class ValorActualizar(BaseModel):
    campo_id: Optional[int] = None
    valor: Optional[float] = None
    fecha_hora_lectura: Optional[datetime] = None

# Para respuestas (incluye ID)
class Valor(ValorBase):
    id: int

    class Config:
        orm_mode = True
