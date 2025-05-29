from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional, Any

#clase para los usuarios
# Modelo base (sin ID)
class   UsuarioBase(BaseModel):
    nombre_usuario: str
    nombre: str
    apellido: str 
    email: EmailStr
    contrasena: str
    activo: Optional[bool] = None
    fecha_registro: Optional[str] = ''
    ultimo_login: Optional[str]=''
    tipo_usuario: Optional[str] = None

   
# Modelo para crear usuario
class UsuarioCrear(UsuarioBase):
    pass

# Modelo para actualizar parcialmente
class UsuarioActualizar(BaseModel): 
    nombre_usuario: str
    apellido: str 
    email: EmailStr
    contrasena: str
    fecha_registro: Optional[str] = ''
    ultimo_login: Optional[str]=''

# Modelo para el login
class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str


# Modelo con ID, por ejemplo, para respuestas
class Usuario(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
