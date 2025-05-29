from fastapi import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import pymysql
import bcrypt

from app.configuracion import configuracion
from app.servicios.servicio_simulacion import get_db_connection, simular_datos_json

from app.api.modelos.usuarios import UsuarioCrear, UsuarioActualizar,UsuarioLogin


router_usuario = APIRouter()

# Crear Proyectos 
@router_usuario.post("/crear_usuario/")
async def crear_usuario(datos: UsuarioCrear):
    try:
      

   

        resultados = await set_usuario(datos)
        

        return {"message": "Se registro el usuario", "resultados": resultados}

    except ValueError as e:
        return {"message": "Error al regostrar el usuario", "details": str(e)}
    except Exception as e:
        print("Excepción general:", type(e), e)
        return JSONResponse(
            status_code=500,
            content={"message": "Error inesperado durante la inserción ", "details": str(e)},
        )
    
#Crear usuario
async def set_usuario(datos: UsuarioCrear) -> List[Dict[str, Any]]:
    procesado = []
    conn = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

     # Verificar si el nombre_usuario o email ya existe
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s OR email = %s", (datos.nombre_usuario, datos.email))
        if cursor.fetchone():
            return [{
                "status": "error",
                "message": "El nombre de usuario o el correo electrónico ya están en uso"
            }]

        # Obtener fechas
        fecha_registro = datos.fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        hashed_pw = bcrypt.hashpw(datos.contrasena.encode('utf-8'), bcrypt.gensalt())
  

        # Preparar campos y valores
        campos = ["nombre_usuario", "nombre", "apellido", "email", "contrasena", "activo", "fecha_registro"]
        valores = [datos.nombre_usuario, datos.nombre, datos.apellido, datos.email, hashed_pw,datos.activo, fecha_registro]

        if datos.tipo_usuario:
            campos.append("tipo_usuario")
            valores.append(datos.tipo_usuario)

        # Construir consulta dinámicamente
        sql = f"INSERT INTO usuarios ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(valores))})"

        cursor.execute(sql, valores)
        conn.commit()

        procesado.append({
            "status": "success",
            "nombre_usuario": datos.nombre_usuario,
            "email": datos.email,
            "tipo_usuario": datos.tipo_usuario or 'empleado',
            "fecha_registro": fecha_registro
        })

    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"DB Error: {str(e)}"
        })

    except Exception as e:
        if conn:
            conn.rollback()
        procesado.append({
            "status": "error",
            "message": f"Unexpected Error: {str(e)}"
        })

    finally:
        if conn:
            conn.close()

    return procesado



@router_usuario.post("/login")
async def login(datos: UsuarioLogin):
    return await login_usuario(datos)


# Login de usuario
async def login_usuario(datos: UsuarioLogin):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

       
        # Buscar al usuario por nombre de usuario
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (datos.nombre_usuario,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
       # Verificar contraseña
        if not bcrypt.checkpw(datos.contrasena.encode('utf-8'), usuario["contrasena"].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

       
        # Actualizar el último login
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE usuarios SET ultimo_login = %s WHERE id = %s", (ahora, usuario["id"]))
        conn.commit()

        # Eliminar contraseña antes de devolver los datos
        usuario.pop("contrasena", None)

        return {
            "status": "success",
            "message": "Inicio de sesión exitoso",
            "usuario": usuario
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")

    finally:
        if conn:
            conn.close()



    
@router_usuario.get("/obtener_usuario/")
async def obtener_usuario(id: int):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # Buscar el usuario por nombre de usuario
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Eliminar la contraseña antes de devolver los datos
        usuario.pop("contrasena", None)

        return {
            "status": "success",
            "usuario": usuario
        }

    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error en base de datos: {str(e)}")

    finally:
        if conn:
            conn.close()